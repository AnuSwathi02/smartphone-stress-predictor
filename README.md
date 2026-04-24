# 📱 Smartphone Stress Detection System

A web app that predicts your stress level based on your daily smartphone usage habits — and tells you whether your stress is getting better, worse, or staying the same over time.

---

## 🤔 What Is This?

Most stress apps just tell you "you're stressed right now." This one goes further — it tracks your stress over time and predicts the **direction** it's heading. Are things getting worse? Are you recovering? It'll tell you, and it'll alert you before things get critical.

Built as part of a pervasive computing project, this app uses a **Random Forest** model trained on real mobile usage data to predict stress levels from your daily phone habits like screen time, sleep, social media usage, and more.

---

## ✨ Features

### 1. 🔮 Stress Trajectory Prediction
Not just "your stress is HIGH" — but "your stress has been **increasing for 3 days**, take action now." Uses a 7-day sliding window and linear regression to detect trends.

### 2. 🧠 Explainable Predictions
Tells you *why* the model made that prediction — which factors contributed the most (e.g., "High screen time and low sleep are your biggest stress drivers").

### 3. 🔒 Consent-Aware Privacy
You choose how much data to share:
- **Full consent** → All 12 features used, detailed results
- **Limited consent** → Only broad features (screen time, sleep, activity)
- **Minimal consent** → Just screen time and sleep

### 4. 🚨 Intelligent Alert System
Smart alerts that don't spam you. Alerts adapt based on:
- Your consent level (more detail = more specific alert)
- Time of day (night-time high stress triggers a "digital detox" alert)
- Repeated stress spikes (escalates to critical alert after 3+ high readings)
- 30-minute cooldown between same-type alerts

### 5. 📄 PDF Report Download
Download a full report of your prediction including trajectory, explanation, contributing factors, and consent level used.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| ML Models | Random Forest (Classifier + Regressor) |
| Data Balancing | SMOTE (imbalanced-learn) |
| Trend Analysis | Linear Regression (scipy) |
| Visualizations | Matplotlib, Seaborn |
| PDF Generation | ReportLab |
| Frontend Storage | Browser localStorage (for user history) |

---

## 📂 Project Structure

```
stress-detection-app/
│
├── app.py                          # Main Flask app + all ML logic
├── stress_model.pkl                # Pre-trained model
├── requirements.txt                # Python dependencies
│
├── static/
│   ├── confusion_matrix.png        # Auto-generated on startup
│   └── feature_importance.png      # Auto-generated on startup
│
├── templates/
│   └── index.html                  # Frontend UI
│
├── STRESS_TRAJECTORY_EXPLANATION.md
├── INTELLIGENT_ALERT_SYSTEM.md
├── HOW_TO_GET_3_HISTORICAL_READINGS.md
└── RUN_LOCALHOST.md
```

---

## 🚀 How to Run Locally

### Step 1: Clone the repo
```bash
git clone https://github.com/SUBASHREE15S/Stress-Detection.git
cd Stress-Detection
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Add your dataset
Place your `mobile_addiction_data.csv` file somewhere on your system and update this line in `app.py`:

```python
csv_path = r"C:\path\to\your\mobile_addiction_data.csv"
```

### Step 4: Run the app
```bash
python app.py
```

### Step 5: Open in browser
```
http://127.0.0.1:5000/
```

---

## 📊 Input Features

The model uses these 12 features from your daily phone usage:

| Feature | Description |
|---------|-------------|
| Daily Screen Time (hrs) | Total hours phone screen was on |
| Phone Unlocks Per Day | How many times you picked up your phone |
| Social Media Usage (hrs) | Time on Instagram, Twitter, etc. |
| Gaming Usage (hrs) | Time spent on mobile games |
| Streaming Usage (hrs) | YouTube, Netflix, etc. |
| Messaging Usage (hrs) | WhatsApp, SMS, etc. |
| Work-Related Usage (hrs) | Emails, work apps |
| Sleep Hours | Hours of sleep per night |
| Physical Activity (hrs) | Exercise or movement |
| Time With Family (hrs) | Offline social time |
| Online Shopping (hrs) | Time on shopping apps |
| Push Notifications/Day | Number of notifications received |

---

## 🎯 How Stress Is Calculated

```
Stress Score =
  (Screen Time × 2) + (Unlocks × 0.3) + (Social Media × 1.5)
  + (Gaming × 1.5) + (Streaming × 1.2) + (Work Usage × 1.3)
  + (Notifications × 0.2)
  − (Sleep × 4) − (Physical Activity × 3) − (Family Time × 2)
```

The score is then classified into **Low / Medium / High** using the 33rd and 66th percentiles.

---

## 📈 Trajectory Prediction — How It Works

1. Every prediction you make is saved with a timestamp
2. After **3 or more predictions**, linear regression calculates the trend
3. Based on the slope:
   - **Slope > +2.0** → INCREASING ⚠️
   - **Slope < −2.0** → RECOVERING ✅
   - **In between** → STABLE 📊

> To quickly test this, click the **"🧪 Add Test History"** button in the app — it loads 3 sample readings instantly.

---

## 🚨 Alert Types

| Alert | Trigger | Severity |
|-------|---------|----------|
| Immediate | High stress + increasing trend | 🟠 High |
| Early Warning | Moderate stress + rising trend | 🟢 Low |
| Digital Detox | High stress during night hours (10PM–6AM) | 🔵 Medium |
| Escalated | 3+ consecutive high stress readings | 🔴 Critical |

Alerts have a **30-minute cooldown** — no spam. Critical alerts never auto-dismiss.

---

## 📋 Requirements

```
Flask==3.0.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
imbalanced-learn==0.11.0
matplotlib==3.8.2
seaborn==0.13.0
reportlab==4.0.7
scipy==1.11.4
```

---

## 🔮 Future Improvements

- Connect to real phone usage APIs (Android Digital Wellbeing, iOS Screen Time)
- Push notifications to mobile
- Persistent user accounts across devices
- Integration with wearables for heart rate and sleep data

---

## 👩‍💻 Built By

**ANU SWATHI V.R** 
**SUBASHREE S**
**LAHARI K.R**
