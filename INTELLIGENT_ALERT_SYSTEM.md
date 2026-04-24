# 🚨 Intelligent Consent-Aware Alert System

## Overview

This is a **patent-worthy** intelligent alert system that adapts alert messages and specificity based on user consent level, stress conditions, and time context.

---

## 🔹 Inputs to Alert Engine

1. **Current stress score** - The predicted stress score from the model
2. **Stress trajectory prediction** - increasing / stable / recovering
3. **Time-of-day context** - morning / afternoon / evening / night
4. **Consent level** - full / limited / minimal
5. **Alert history** - Tracks previous alerts to avoid spamming

---

## 🔹 Alert Trigger Conditions

| Condition | Alert Type | Severity |
|-----------|-----------|----------|
| High stress + increasing trend | **Immediate Alert** | High |
| Moderate stress + rising trend | **Early Warning Alert** | Low |
| High stress during night hours | **Digital Disengagement Alert** | Medium |
| Repeated stress spikes (3+ high scores) | **Escalated Alert** | Critical |

### Trigger Logic Priority:
1. **Repeated stress spikes** → Escalated (highest priority)
2. **High stress + increasing** → Immediate
3. **High stress at night** → Digital Disengagement
4. **Moderate/High + increasing** → Early Warning
5. **High stress alone** → Immediate (fallback)

---

## 🔹 Consent-Aware Alert Adaptation

### Full Consent
- **Specific cause** + **detailed action recommendations**
- Example: "High stress detected (Score: 55.2). Please reduce phone usage in the next 5 minutes. Consider: taking a break, deep breathing, or stepping away from your device."

### Limited Consent
- **General stress alert** with basic recommendations
- Example: "High stress level detected. Consider taking a short break from your device."

### Minimal Consent
- **Minimal alert only** - basic notification
- Example: "High stress detected. Please take a break."

---

## 🔹 Alert Types & Messages

### 1. Immediate Alert
**Trigger:** High stress + increasing trend OR High stress alone

**Full Consent:**
> "High stress detected (Score: 55.2). Please reduce phone usage in the next 5 minutes. Consider: taking a break, deep breathing, or stepping away from your device."

**Limited Consent:**
> "High stress level detected. Consider taking a short break from your device."

**Minimal Consent:**
> "High stress detected. Please take a break."

---

### 2. Early Warning Alert
**Trigger:** Moderate/High stress + rising trend

**Full Consent:**
> "Your stress level is rising (Trajectory: increasing). Current score: 45.3. Consider: reducing screen time, increasing physical activity, or improving sleep."

**Limited Consent:**
> "Stress level is increasing. Consider taking preventive measures."

**Minimal Consent:**
> "Stress level rising. Take care."

---

### 3. Digital Disengagement Alert
**Trigger:** High stress during night hours (10 PM - 6 AM)

**Full Consent:**
> "Late-night phone usage detected (night hours). High stress (55.2) during night hours may impact sleep quality. Enable focus mode or reduce usage?"

**Limited Consent:**
> "High stress during night hours. Consider reducing device usage."

**Minimal Consent:**
> "High stress at night. Reduce usage."

---

### 4. Escalated Alert
**Trigger:** Repeated stress spikes (3+ consecutive high stress scores > 40)

**Full Consent:**
> "Repeated stress spikes detected. Your stress has been increasing over multiple readings. Current: 55.2. Strongly recommend: digital detox, consultation with healthcare provider, or stress management techniques."

**Limited Consent:**
> "Repeated high stress detected. Consider professional help or stress management."

**Minimal Consent:**
> "Repeated high stress. Seek help if needed."

---

## 🔹 Anti-Spam Protection

### Alert Cooldown System
- **Cooldown period:** 30 minutes between same-type alerts
- **History tracking:** Last 10 alerts per user
- **Automatic dismissal:** Non-critical alerts auto-dismiss after 10 seconds

### How It Works:
1. System checks if same alert type was sent in last 30 minutes
2. If yes → Alert suppressed (prevents spamming)
3. If no → Alert triggered and recorded
4. Critical alerts (escalated) never auto-dismiss

---

## 🔹 Time-of-Day Context

The system automatically detects time context:

- **Night:** 10 PM - 6 AM
- **Morning:** 6 AM - 12 PM
- **Afternoon:** 12 PM - 6 PM
- **Evening:** 6 PM - 10 PM

Time context influences:
- Alert type selection (night → digital disengagement)
- Alert message wording
- Alert severity

---

## 🔹 Frontend Display

### Alert Card Features:
- **Color-coded by severity:**
  - 🔴 Critical (Red) - Escalated alerts
  - 🟠 High (Orange) - Immediate alerts
  - 🔵 Medium (Blue) - Digital disengagement
  - 🟢 Low (Green) - Early warning

- **Interactive:**
  - Close button to dismiss
  - Auto-dismiss for non-critical alerts (10 seconds)
  - Pulse animation for critical alerts

- **Information Display:**
  - Alert icon (🚨 ⚠️ ℹ️ 💡)
  - Alert message
  - Context info (type, time, consent level)

---

## 🔹 Patent-Worthy Elements

### 1. Consent-Aware Alert Adaptation
- **Novel:** Dynamic alert specificity based on privacy consent
- **Claimable:** "A system that adapts alert message detail level based on user consent preferences"

### 2. Multi-Condition Alert Logic
- **Novel:** Complex trigger conditions combining multiple factors
- **Claimable:** "Alert generation based on stress score, trajectory, time context, and history"

### 3. Anti-Spam Alert System
- **Novel:** Intelligent cooldown preventing alert fatigue
- **Claimable:** "Alert history tracking and cooldown mechanism to prevent notification spamming"

### 4. Time-Context Aware Alerts
- **Novel:** Different alert types based on time of day
- **Claimable:** "Time-of-day context integration for digital wellness alerts"

---

## 🔹 Technical Implementation

### Backend Functions:
- `get_time_context()` - Determines time-of-day context
- `should_trigger_alert()` - Checks cooldown/spam prevention
- `record_alert()` - Records alert in history
- `generate_alert()` - Generates consent-adaptive message
- `determine_alert_type()` - Multi-condition trigger logic
- `generate_consent_aware_alert()` - Main alert generation function

### Data Structures:
- `ALERT_HISTORY` - Dictionary storing alert history per user
- `ALERT_COOLDOWN_MINUTES` - 30 minutes cooldown
- `ALERT_WINDOW_SIZE` - Last 10 alerts tracked

---

## 🔹 Usage Examples

### Example 1: High Stress + Increasing Trend
```
Input: Stress = 55, Level = High, Trajectory = increasing, Time = afternoon
Result: Immediate Alert (High severity)
Message: "High stress detected (Score: 55.0). Please reduce phone usage..."
```

### Example 2: Night-Time High Stress
```
Input: Stress = 50, Level = High, Time = night (11 PM)
Result: Digital Disengagement Alert (Medium severity)
Message: "Late-night phone usage detected (night hours)..."
```

### Example 3: Repeated Stress Spikes
```
Input: 3 consecutive predictions with stress > 40
Result: Escalated Alert (Critical severity)
Message: "Repeated stress spikes detected..."
```

---

## 🔹 Testing

To test the alert system:

1. **High Stress Test:**
   - Enter: High screen time (10h), Low sleep (5h)
   - Expected: Immediate alert

2. **Night-Time Test:**
   - Use app during night hours (10 PM - 6 AM)
   - Enter high stress values
   - Expected: Digital disengagement alert

3. **Repeated Spikes Test:**
   - Make 3+ predictions with high stress
   - Expected: Escalated alert

4. **Consent Level Test:**
   - Change consent level (Full/Limited/Minimal)
   - Same stress conditions
   - Expected: Different message detail levels

---

## 🔹 Future Enhancements

Potential improvements:
- User-configurable alert preferences
- Alert frequency customization
- Integration with device notifications
- Alert analytics and insights
- Machine learning for optimal alert timing

