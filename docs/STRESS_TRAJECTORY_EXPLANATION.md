# 📈 Stress Trajectory Prediction - How It Works

## What It Does

**Stress Trajectory Prediction** doesn't just tell you "You have HIGH stress RIGHT NOW" - it predicts the **TREND**:
- Is your stress **INCREASING**? ⬆️
- Is your stress **STABLE**? ➡️  
- Is your stress **RECOVERING**? ⬇️

## The Problem It Solves

Traditional stress detection only tells you the **current state**:
- ❌ "You have HIGH stress" (but is it getting worse or better?)

Trajectory prediction tells you the **direction**:
- ✅ "Your stress is INCREASING - take preventive action now!"
- ✅ "Your stress is RECOVERING - keep up the good habits!"

---

## How It Works (Step by Step)

### Step 1: **Sliding Window Storage**
- Stores your last **7 stress predictions** with timestamps
- Each time you make a prediction, it's added to your history
- Old predictions (older than 7 days) are automatically removed

### Step 2: **Trend Analysis**
- Uses **linear regression** to calculate a trend line through your stress scores
- Calculates the **slope** (rate of change) of your stress over time

### Step 3: **Trajectory Classification**
Based on the slope:
- **Slope > +2.0** → "INCREASING" (stress going up)
- **Slope < -2.0** → "RECOVERING" (stress going down)
- **-2.0 ≤ Slope ≤ +2.0** → "STABLE" (stress staying steady)

---

## Real Examples

### Example 1: Stress INCREASING ⚠️
```
Day 1: Stress Score = 20
Day 2: Stress Score = 35  
Day 3: Stress Score = 50
```
**Result:** 
- Trend Slope: +5.0 per hour
- Prediction: **"INCREASING"**
- Message: "Stress is increasing. Consider preventive measures."

### Example 2: Stress RECOVERING ✅
```
Day 1: Stress Score = 60
Day 2: Stress Score = 45
Day 3: Stress Score = 30
```
**Result:**
- Trend Slope: -5.0 per hour  
- Prediction: **"RECOVERING"**
- Message: "Stress is recovering. Positive trend detected."

### Example 3: Stress STABLE 📊
```
Day 1: Stress Score = 40
Day 2: Stress Score = 42
Day 3: Stress Score = 41
```
**Result:**
- Trend Slope: +0.3 per hour
- Prediction: **"STABLE"**
- Message: "Stress level is stable."

---

## Key Benefits

### 🎯 **Early Warning System**
- Detects stress trends **BEFORE** they become critical
- Gives you time to take preventive action

### 🔮 **Predictive, Not Just Diagnostic**
- Shifts from "diagnosis" (what is it now?) to "forecasting" (where is it going?)
- This is the **patentable novelty** - preventive computing!

### 📊 **Personalized Tracking**
- Tracks **YOUR** specific stress pattern over time
- Adapts to your individual stress trajectory

### ⚡ **Actionable Insights**
- "INCREASING" → Take action now to prevent escalation
- "RECOVERING" → Keep doing what you're doing
- "STABLE" → Maintain current habits

---

## Technical Details

### Algorithm Used
- **Linear Regression** (from scipy.stats)
- Calculates: `slope`, `intercept`, `r_value` (correlation coefficient)

### Confidence Levels
- **High confidence**: Strong correlation (|r| > 0.7)
- **Medium confidence**: Moderate correlation (0.3 < |r| ≤ 0.7)
- **Low confidence**: Weak correlation or insufficient data (< 3 points)

### Data Requirements
- **Minimum**: 3 historical predictions needed
- **Optimal**: 7 days of data (sliding window)
- **Storage**: Uses Python `deque` (double-ended queue) for efficient sliding window

---

## Why This Is Patentable

1. **Novel Approach**: Shift from detection to **early trajectory prediction**
2. **Preventive Computing**: Helps prevent stress escalation, not just detect it
3. **Temporal ML**: Uses time-series analysis for mental health prediction
4. **Unique Combination**: Sliding window + trend analysis + preventive alerts

---

## In Your App

When you make predictions:
1. **First prediction**: Shows "STABLE" (insufficient data)
2. **After 3+ predictions**: Shows actual trajectory (INCREASING/STABLE/RECOVERING)
3. **Display shows**:
   - Trajectory status (color-coded alert)
   - Trend slope (rate of change)
   - Confidence level
   - Actionable message

