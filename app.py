from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error
from imblearn.over_sampling import SMOTE
import matplotlib
matplotlib.use("Agg")  # Non-GUI backend for Flask
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import os
from datetime import datetime, timedelta
from collections import deque
from scipy import stats

app = Flask(__name__)

# ---------------- CREATE STATIC FOLDER IF MISSING ----------------
if not os.path.exists("static"):
    os.makedirs("static")

# ---------------- GLOBAL STORAGE FOR PDF ---------------- 
last_prediction = {}

# ---------------- FEATURE 1: STRESS TRAJECTORY PREDICTION (Sliding Window) ----------------
# Store historical stress scores with timestamps (sliding window of N days)
STRESS_HISTORY = {}  # user_id -> deque of (timestamp, stress_score)
WINDOW_SIZE = 7  # 7 days sliding window

# ---------------- FEATURE 4: INTELLIGENT ALERT ENGINE ----------------
# Alert history to avoid spamming
ALERT_HISTORY = {}  # user_id -> deque of (timestamp, alert_type)
ALERT_COOLDOWN_MINUTES = 30  # Minimum minutes between same-type alerts
ALERT_WINDOW_SIZE = 10  # Store last 10 alerts per user
ALERT_DISPLAY_DURATION_MINUTES = 7  # Alert remains visible for 7 minutes

# ---------------- LOAD DATASET ----------------
csv_path = r"C:\Users\vijai\Downloads\mobile_addiction_data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dataset not found at {csv_path}")

df = pd.read_csv(csv_path)
df.dropna(inplace=True)

# ---------------- FEATURES ----------------
features = [
    'Daily_Screen_Time_Hours',
    'Phone_Unlocks_Per_Day',
    'Social_Media_Usage_Hours',
    'Gaming_Usage_Hours',
    'Streaming_Usage_Hours',
    'Messaging_Usage_Hours',
    'Work_Related_Usage_Hours',
    'Sleep_Hours',
    'Physical_Activity_Hours',
    'Time_Spent_With_Family_Hours',
    'Online_Shopping_Hours',
    'Push_Notifications_Per_Day'
]

df = df[features]

# ---------------- FEATURE 3: CONSENT-AWARE FEATURE SELECTION ----------------
# Define feature groups based on consent levels (after features are defined)
CONSENT_LEVELS = {
    "full": features,  # All features
    "limited": [  # Coarse features only
        'Daily_Screen_Time_Hours',
        'Phone_Unlocks_Per_Day',
        'Sleep_Hours',
        'Physical_Activity_Hours'
    ],
    "minimal": [  # Minimal features
        'Daily_Screen_Time_Hours',
        'Sleep_Hours'
    ]
}

# ---------------- STRESS SCORE ----------------
df['Stress_Score'] = (
    df['Daily_Screen_Time_Hours'] * 2 +
    df['Phone_Unlocks_Per_Day'] * 0.3 +
    df['Social_Media_Usage_Hours'] * 1.5 +
    df['Gaming_Usage_Hours'] * 1.5 +
    df['Streaming_Usage_Hours'] * 1.2 +
    df['Work_Related_Usage_Hours'] * 1.3 +
    df['Push_Notifications_Per_Day'] * 0.2 -
    df['Sleep_Hours'] * 4 -
    df['Physical_Activity_Hours'] * 3 -
    df['Time_Spent_With_Family_Hours'] * 2
)

# ---------------- STRESS CLASS ----------------
low = df['Stress_Score'].quantile(0.33)
high = df['Stress_Score'].quantile(0.66)

def label_stress(x):
    if x <= low:
        return 0
    elif x <= high:
        return 1
    else:
        return 2

df['Stress_Class'] = df['Stress_Score'].apply(label_stress)

X = df[features]
y_class = df['Stress_Class']
y_reg = df['Stress_Score']

# ---------------- BALANCE DATA ----------------
sm = SMOTE(random_state=42)
X_res, y_class_res = sm.fit_resample(X, y_class)

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X_res, y_class_res, test_size=0.2, random_state=42
)

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

# ---------------- TRAIN MODELS ----------------
clf = RandomForestClassifier(n_estimators=300, max_depth=12, random_state=42)
clf.fit(X_train, y_train)

reg = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
reg.fit(X_train_r, y_train_r)

# ---------------- EVALUATION ----------------
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

# ---------------- SAVE CONFUSION MATRIX ----------------
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Low", "Medium", "High"],
            yticklabels=["Low", "Medium", "High"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("static/confusion_matrix.png")
plt.close()

# ---------------- REGRESSION METRICS ----------------
y_pred_r = reg.predict(X_test_r)
rmse = mean_squared_error(y_test_r, y_pred_r) ** 0.5

mae = mean_absolute_error(y_test_r, y_pred_r)

# ---------------- STRESS SCORE NORMALIZATION (for gauge display) ----------------
# Calculate min/max stress scores for normalization
STRESS_SCORE_MIN = df['Stress_Score'].min()
STRESS_SCORE_MAX = df['Stress_Score'].max()
STRESS_SCORE_RANGE = STRESS_SCORE_MAX - STRESS_SCORE_MIN

def normalize_stress_score(score):
    """Normalize stress score to 0-100% for gauge display"""
    if STRESS_SCORE_RANGE == 0:
        return 50.0  # Default if no range
    normalized = ((score - STRESS_SCORE_MIN) / STRESS_SCORE_RANGE) * 100
    return max(0, min(100, normalized))  # Clamp between 0 and 100

# ---------------- FEATURE IMPORTANCE ----------------
importances = clf.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(features, importances, color="#4caf50")
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.tight_layout()
plt.savefig("static/feature_importance.png")
plt.close()

# ---------------- FEATURE 1: STRESS TRAJECTORY PREDICTION FUNCTIONS ----------------
def predict_stress_trajectory(user_id, current_score):
    """
    Predicts stress trajectory: "increasing", "stable", or "recovering"
    Uses sliding window and trend slope calculation
    """
    if user_id not in STRESS_HISTORY:
        STRESS_HISTORY[user_id] = deque(maxlen=WINDOW_SIZE)
    
    history = STRESS_HISTORY[user_id]
    now = datetime.now()
    
    # Add current prediction to history
    history.append((now, current_score))
    
    # Need at least 3 data points for trend analysis
    if len(history) < 3:
        return {
            "trajectory": "stable",
            "trend_slope": 0.0,
            "confidence": "low",
            "message": "Insufficient data for trajectory prediction. Need at least 3 historical readings."
        }
    
    # Extract scores and timestamps
    scores = [item[1] for item in history]
    timestamps = [item[0] for item in history]
    
    # Convert timestamps to numeric (hours since first reading)
    time_numeric = [(ts - timestamps[0]).total_seconds() / 3600 for ts in timestamps]
    
    # Calculate linear regression slope
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_numeric, scores)
    
    # Determine trajectory based on slope
    if slope > 2.0:  # Significant increase
        trajectory = "increasing"
        confidence = "high" if abs(r_value) > 0.7 else "medium"
        message = f"Stress is increasing (slope: +{slope:.2f} per hour). Consider preventive measures."
    elif slope < -2.0:  # Significant decrease
        trajectory = "recovering"
        confidence = "high" if abs(r_value) > 0.7 else "medium"
        message = f"Stress is recovering (slope: {slope:.2f} per hour). Positive trend detected."
    else:  # Stable
        trajectory = "stable"
        confidence = "high" if abs(r_value) < 0.3 else "medium"
        message = f"Stress level is stable (slope: {slope:.2f} per hour)."
    
    return {
        "trajectory": trajectory,
        "trend_slope": round(float(slope), 3),
        "r_squared": round(float(r_value ** 2), 3),
        "confidence": confidence,
        "message": message,
        "data_points": len(history)
    }

# ---------------- FEATURE 2: EXPLAINABLE STRESS REASONING ENGINE ----------------
def generate_explanation(input_df, clf_model, reg_model, stress_level, stress_score):
    """
    Generates human-readable explanations for stress predictions
    Uses feature attribution and rule-based reasoning
    """
    # Get feature importances
    feature_importances = clf_model.feature_importances_
    
    # Get input values
    input_values = input_df.iloc[0].to_dict()
    
    # Calculate feature contributions (simplified SHAP-like approach)
    feature_contributions = {}
    for i, feature in enumerate(features):
        importance = feature_importances[i]
        value = input_values[feature]
        
        # Normalize contribution based on feature importance and value
        # For stress-inducing features (high values = more stress)
        if feature in ['Daily_Screen_Time_Hours', 'Phone_Unlocks_Per_Day', 
                       'Social_Media_Usage_Hours', 'Gaming_Usage_Hours',
                       'Streaming_Usage_Hours', 'Push_Notifications_Per_Day']:
            contribution = importance * value
        else:  # Stress-reducing features (high values = less stress)
            contribution = importance * (1 / (value + 0.1))  # Inverse relationship
        
        feature_contributions[feature] = contribution
    
    # Sort by contribution
    sorted_features = sorted(feature_contributions.items(), key=lambda x: x[1], reverse=True)
    
    # Generate rule-based explanations
    explanations = []
    reasons = []
    
    # Top contributing factors
    top_3 = sorted_features[:3]
    
    for feature, contribution in top_3:
        value = input_values[feature]
        feature_name = feature.replace('_', ' ').title()
        
        # Generate contextual explanation
        if 'Screen Time' in feature_name:
            if value > 8:
                reasons.append(f"High screen time ({value:.1f} hours)")
                explanations.append(f"Excessive daily screen time of {value:.1f} hours significantly contributes to stress.")
        elif 'Unlocks' in feature_name:
            if value > 100:
                reasons.append(f"Frequent phone unlocks ({value:.0f} times/day)")
                explanations.append(f"Very frequent phone usage ({value:.0f} unlocks per day) indicates compulsive behavior.")
        elif 'Social Media' in feature_name:
            if value > 3:
                reasons.append(f"High social media usage ({value:.1f} hours)")
                explanations.append(f"Extended social media usage ({value:.1f} hours) may increase stress levels.")
        elif 'Sleep' in feature_name:
            if value < 6:
                reasons.append(f"Insufficient sleep ({value:.1f} hours)")
                explanations.append(f"Inadequate sleep duration ({value:.1f} hours) is a major stress contributor.")
        elif 'Physical Activity' in feature_name:
            if value < 1:
                reasons.append(f"Low physical activity ({value:.1f} hours)")
                explanations.append(f"Limited physical activity ({value:.1f} hours) reduces stress resilience.")
        elif 'Family Time' in feature_name:
            if value < 1:
                reasons.append(f"Minimal family time ({value:.1f} hours)")
                explanations.append(f"Low family interaction time ({value:.1f} hours) may increase stress.")
        else:
            reasons.append(f"{feature_name}: {value:.1f}")
            explanations.append(f"{feature_name} value of {value:.1f} contributes to stress prediction.")
    
    # Combine explanations
    main_explanation = "Stress detected due to: " + " + ".join(reasons[:2]) + "."
    
    return {
        "main_explanation": main_explanation,
        "detailed_reasons": explanations,
        "top_contributors": [
            {
                "feature": feat.replace('_', ' ').title(),
                "value": round(input_values[feat], 2),
                "contribution": round(contrib, 3)
            }
            for feat, contrib in top_3
        ],
        "feature_rankings": [
            {
                "feature": feat.replace('_', ' ').title(),
                "importance": round(contrib, 3)
            }
            for feat, contrib in sorted_features
        ]
    }

# ---------------- FEATURE 3: CONSENT-AWARE FEATURE SELECTION ----------------
def get_consent_features(consent_level):
    """Returns feature list based on consent level"""
    return CONSENT_LEVELS.get(consent_level, CONSENT_LEVELS["full"])

def adapt_model_for_consent(consent_level, input_data):
    """
    Adapts model input based on consent level
    For limited/minimal consent, uses only coarse features
    """
    allowed_features = get_consent_features(consent_level)
    
    # Filter input data to only include allowed features
    filtered_data = {f: input_data.get(f, 0) for f in allowed_features}
    
    # For missing features in limited consent, use defaults or averages
    if consent_level != "full":
        # Use dataset averages for missing features
        for feature in features:
            if feature not in allowed_features:
                filtered_data[feature] = df[feature].mean()
    
    return filtered_data, allowed_features

# ---------------- FEATURE 4: INTELLIGENT ALERT ENGINE ----------------
def get_time_context():
    """Determine time-of-day context for alerts"""
    now = datetime.now()
    hour = now.hour
    
    if 22 <= hour or hour < 6:  # 10 PM - 6 AM
        return "night"
    elif 6 <= hour < 12:  # 6 AM - 12 PM
        return "morning"
    elif 12 <= hour < 18:  # 12 PM - 6 PM
        return "afternoon"
    else:  # 6 PM - 10 PM
        return "evening"

def should_trigger_alert(user_id, alert_type):
    """Check if alert should be triggered (avoid spamming)"""
    if user_id not in ALERT_HISTORY:
        ALERT_HISTORY[user_id] = deque(maxlen=ALERT_WINDOW_SIZE)
        return True
    
    history = ALERT_HISTORY[user_id]
    now = datetime.now()
    
    # Check if same alert type was sent recently
    for timestamp, prev_type in history:
        if prev_type == alert_type:
            time_diff = (now - timestamp).total_seconds() / 60  # minutes
            if time_diff < ALERT_COOLDOWN_MINUTES:
                return False  # Too soon, don't spam
    
    return True

def record_alert(user_id, alert_type):
    """Record that an alert was sent"""
    if user_id not in ALERT_HISTORY:
        ALERT_HISTORY[user_id] = deque(maxlen=ALERT_WINDOW_SIZE)
    
    ALERT_HISTORY[user_id].append((datetime.now(), alert_type))

def generate_alert(stress_score, stress_level, trajectory, time_context, consent_level, alert_type):
    """
    Generate adaptive alert message based on consent level and context
    Patent-worthy: Consent-aware alert adaptation
    """
    # Base alert messages (patent claims the logic, not wording)
    alerts = {
        "immediate": {
            "full": f"High stress detected (Score: {stress_score:.1f}). Please reduce phone usage in the next 5 minutes. Consider: taking a break, deep breathing, or stepping away from your device.",
            "limited": f"High stress level detected. Consider taking a short break from your device.",
            "minimal": f"High stress detected. Please take a break."
        },
        "early_warning": {
            "full": f"Your stress level is rising (Trajectory: {trajectory}). Current score: {stress_score:.1f}. Consider: reducing screen time, increasing physical activity, or improving sleep.",
            "limited": f"Stress level is increasing. Consider taking preventive measures.",
            "minimal": f"Stress level rising. Take care."
        },
        "digital_disengagement": {
            "full": f"Late-night phone usage detected ({time_context} hours). High stress ({stress_score:.1f}) during night hours may impact sleep quality. Enable focus mode or reduce usage?",
            "limited": f"High stress during night hours. Consider reducing device usage.",
            "minimal": f"High stress at night. Reduce usage."
        },
        "escalated": {
            "full": f"Repeated stress spikes detected. Your stress has been {trajectory} over multiple readings. Current: {stress_score:.1f}. Strongly recommend: digital detox, consultation with healthcare provider, or stress management techniques.",
            "limited": f"Repeated high stress detected. Consider professional help or stress management.",
            "minimal": f"Repeated high stress. Seek help if needed."
        }
    }
    
    return alerts.get(alert_type, {}).get(consent_level, "Alert triggered.")

def determine_alert_type(stress_score, stress_level, trajectory, time_context, user_id):
    """
    Determine alert type based on trigger conditions
    Patent-worthy: Multi-condition alert logic
    """
    # Check for repeated stress spikes (escalated alert)
    if user_id in STRESS_HISTORY:
        history = STRESS_HISTORY[user_id]
        if len(history) >= 3:
            recent_scores = [item[1] for item in list(history)[-3:]]
            if all(score > 40 for score in recent_scores):  # All recent scores high
                if should_trigger_alert(user_id, "escalated"):
                    return "escalated"
    
    # High stress + increasing trend = Immediate alert
    if stress_level == "High" and trajectory == "increasing":
        if should_trigger_alert(user_id, "immediate"):
            return "immediate"
    
    # High stress during night = Digital disengagement alert
    if stress_level == "High" and time_context == "night":
        if should_trigger_alert(user_id, "digital_disengagement"):
            return "digital_disengagement"
    
    # Moderate stress + rising trend = Early warning
    if stress_level in ["Medium", "High"] and trajectory == "increasing":
        if should_trigger_alert(user_id, "early_warning"):
            return "early_warning"
    
    # High stress alone = Immediate alert (if not already triggered)
    if stress_level == "High":
        if should_trigger_alert(user_id, "immediate"):
            return "immediate"
    
    return None  # No alert needed

def generate_consent_aware_alert(stress_score, stress_level, trajectory_result, consent_level, user_id):
    """
    Main alert generation function - Patent-worthy feature
    Adapts alert specificity based on consent level
    """
    trajectory = trajectory_result.get("trajectory", "stable")
    time_context = get_time_context()
    
    # Determine alert type based on conditions
    alert_type = determine_alert_type(stress_score, stress_level, trajectory, time_context, user_id)
    
    if alert_type is None:
        return None  # No alert needed
    
    # Generate adaptive message based on consent
    alert_message = generate_alert(stress_score, stress_level, trajectory, time_context, consent_level, alert_type)
    
    # Record alert to prevent spamming
    record_alert(user_id, alert_type)
    
    # Determine alert severity/priority
    severity_map = {
        "immediate": "high",
        "escalated": "critical",
        "digital_disengagement": "medium",
        "early_warning": "low"
    }
    
    return {
        "type": alert_type,
        "message": alert_message,
        "severity": severity_map.get(alert_type, "medium"),
        "time_context": time_context,
        "consent_level": consent_level,
        "triggered_at": datetime.now().isoformat()
    }

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html",
                           accuracy=round(accuracy * 100, 2),
                           rmse=round(rmse, 2),
                           mae=round(mae, 2))

@app.route("/add_test_history", methods=["POST"])
def add_test_history():
    """
    Helper endpoint to add test historical data for trajectory prediction
    Useful for testing/demo purposes
    """
    data = request.get_json(force=True)
    user_id = data.get("user_id", "test_user")
    test_scores = data.get("scores", [])
    
    if user_id not in STRESS_HISTORY:
        STRESS_HISTORY[user_id] = deque(maxlen=WINDOW_SIZE)
    
    history = STRESS_HISTORY[user_id]
    base_time = datetime.now()
    
    # Add test scores with timestamps (spread over hours)
    for i, score in enumerate(test_scores):
        timestamp = base_time - timedelta(hours=len(test_scores) - i - 1)
        history.append((timestamp, float(score)))
    
    return jsonify({
        "status": "success",
        "user_id": user_id,
        "data_points": len(history),
        "scores": [item[1] for item in history]
    })

@app.route("/predict", methods=["POST"])
def predict():
    global last_prediction

    data = request.get_json(force=True)
    
    # FEATURE 3: Get consent level (default to "full")
    consent_level = data.get("consent_level", "full")
    user_id = data.get("user_id", "default_user")
    
    # Adapt features based on consent
    adapted_data, used_features = adapt_model_for_consent(consent_level, data)
    
    # Create input dataframe
    input_df = pd.DataFrame([{f: float(adapted_data.get(f, 0)) for f in features}])
    
    # Make predictions
    class_pred = clf.predict(input_df)[0]
    probs = clf.predict_proba(input_df)[0]
    score = reg.predict(input_df)[0]

    stress_map = {0: "Low", 1: "Medium", 2: "High"}

    # FEATURE 1: Predict stress trajectory
    trajectory_result = predict_stress_trajectory(user_id, float(score))
    
    # FEATURE 2: Generate explainable reasoning
    explanation_result = generate_explanation(input_df, clf, reg, stress_map[class_pred], score)
    
    # FEATURE 4: Generate consent-aware intelligent alert
    alert_result = generate_consent_aware_alert(
        float(score), 
        stress_map[class_pred], 
        trajectory_result, 
        consent_level, 
        user_id
    )
    
    # Normalize stress score for gauge display (0-100%)
    normalized_stress_percentage = normalize_stress_score(float(score))

    last_prediction = {
        "stress_level": stress_map[class_pred],
        "stress_score": round(float(score), 2),
        "stress_percentage": round(normalized_stress_percentage, 1),  # For gauge display
        "probabilities": {
            "Low": round(probs[0] * 100, 2),
            "Medium": round(probs[1] * 100, 2),
            "High": round(probs[2] * 100, 2)
        },
        # FEATURE 1: Stress Trajectory
        "trajectory": trajectory_result,
        # FEATURE 2: Explainable Reasoning
        "explanation": explanation_result,
        # FEATURE 3: Consent Info
        "consent_level": consent_level,
        "features_used": used_features,
        # FEATURE 4: Intelligent Alert
        "alert": alert_result
    }

    return jsonify(last_prediction)

# ---------------- PDF REPORT ----------------
@app.route("/download_report")
def download_report():
    if not last_prediction:
        return "No prediction available", 400

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Advanced Stress Detection Report")

    c.setFont("Helvetica", 12)
    y = 760
    c.drawString(100, y, f"Stress Level: {last_prediction['stress_level']}")
    y -= 20
    c.drawString(100, y, f"Stress Score: {last_prediction['stress_score']}")
    y -= 30

    # Prediction Probabilities
    c.drawString(100, y, "Prediction Probabilities:")
    y -= 20
    for k, v in last_prediction["probabilities"].items():
        c.drawString(120, y, f"{k}: {v}%")
        y -= 20
    y -= 20

    # FEATURE 1: Stress Trajectory
    if "trajectory" in last_prediction:
        traj = last_prediction["trajectory"]
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Stress Trajectory Prediction:")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(100, y, f"Trend: {traj['trajectory'].upper()}")
        y -= 15
        c.drawString(100, y, f"Message: {traj['message']}")
        y -= 15
        c.drawString(100, y, f"Slope: {traj['trend_slope']} | Confidence: {traj['confidence']}")
        y -= 20

    # FEATURE 2: Explainable Reasoning
    if "explanation" in last_prediction:
        exp = last_prediction["explanation"]
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, "Explanation:")
        y -= 20
        c.setFont("Helvetica", 10)
        # Wrap long text
        explanation_text = exp["main_explanation"]
        words = explanation_text.split()
        line = ""
        for word in words:
            if len(line + word) < 70:
                line += word + " "
            else:
                c.drawString(100, y, line)
                y -= 15
                line = word + " "
        if line:
            c.drawString(100, y, line)
            y -= 20
        
        c.setFont("Helvetica-Bold", 11)
        c.drawString(100, y, "Top Contributing Factors:")
        y -= 15
        c.setFont("Helvetica", 9)
        for i, contrib in enumerate(exp["top_contributors"][:3], 1):
            c.drawString(120, y, f"{i}. {contrib['feature']}: {contrib['value']}")
            y -= 15
        y -= 10

    # FEATURE 3: Consent Level
    if "consent_level" in last_prediction:
        c.setFont("Helvetica", 9)
        c.drawString(100, y, f"Privacy Consent Level: {last_prediction['consent_level']}")
        y -= 15

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="stress_report.pdf",
        mimetype="application/pdf"
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("Server running at http://127.0.0.1:5000/")
    app.run(debug=True)
