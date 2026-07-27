# 📊 How to Get 3 Historical Readings for Trajectory Prediction

## Method 1: **Make 3 Real Predictions** (Recommended)

Simply use the app **3 times** with different input values:

### Step-by-Step:

1. **First Prediction** (Day 1):
   - Enter your smartphone usage data
   - Click "Predict Stress"
   - Note: Will show "Insufficient data" message

2. **Second Prediction** (Day 2):
   - Enter different values (simulate next day's data)
   - Click "Predict Stress"
   - Note: Still shows "Insufficient data" (need 3 total)

3. **Third Prediction** (Day 3):
   - Enter values again
   - Click "Predict Stress"
   - ✅ **Now trajectory prediction will work!**

### Example Scenario:
```
Day 1: Screen Time = 8h, Sleep = 6h → Stress = 40
Day 2: Screen Time = 9h, Sleep = 5h → Stress = 50  
Day 3: Screen Time = 10h, Sleep = 4h → Stress = 60
→ Result: "INCREASING" trajectory detected!
```

---

## Method 2: **Use Test History Button** (For Testing/Demo)

I've added a **"🧪 Add Test History"** button for quick testing:

1. Click the **"🧪 Add Test History (3 readings)"** button
2. This automatically adds 3 simulated readings
3. Then make **one prediction** to see the trajectory analysis

**Note:** This is for testing only. For real use, use Method 1.

---

## Method 3: **Use Same Browser** (Automatic)

The app now uses **localStorage** to remember your user ID:

- ✅ **Same browser** = Same user = History accumulates automatically
- ✅ **Different browser** = New user = Fresh start
- ✅ **Clear browser data** = Resets history

**How it works:**
- First prediction: Creates user ID and stores in browser
- Subsequent predictions: Uses same user ID
- History accumulates automatically!

---

## Understanding the History Storage

### What Gets Stored:
- **User ID**: Unique identifier (stored in browser localStorage)
- **Stress Scores**: Your predicted stress scores
- **Timestamps**: When each prediction was made
- **Window Size**: Last 7 predictions (sliding window)

### How It Works:
```
Prediction 1: Stress = 30 → Stored
Prediction 2: Stress = 35 → Stored  
Prediction 3: Stress = 40 → Stored → ✅ Trajectory analysis starts!
Prediction 4: Stress = 45 → Stored (oldest removed if > 7)
...
```

---

## Troubleshooting

### Problem: "Insufficient data" message always shows

**Solutions:**
1. ✅ Make sure you're using the **same browser** (localStorage)
2. ✅ Make at least **3 predictions** total
3. ✅ Use the **Test History button** for quick testing
4. ✅ Check browser console for errors

### Problem: History resets every time

**Solution:**
- Make sure **localStorage is enabled** in your browser
- Don't use **incognito/private mode** (localStorage may be disabled)
- Don't **clear browser data** between sessions

---

## Quick Test Example

To quickly see trajectory prediction in action:

1. Click **"🧪 Add Test History"** button
2. Enter any values in the form
3. Click **"Predict Stress"**
4. ✅ You'll see trajectory analysis with "INCREASING" trend!

---

## Real-World Usage

For **real-world use**, make predictions:
- **Daily**: Once per day to track your stress trend
- **Weekly**: See 7-day trajectory patterns
- **As needed**: When you want to check your stress level

The system automatically:
- ✅ Tracks your history
- ✅ Calculates trends
- ✅ Shows trajectory predictions
- ✅ Removes old data (> 7 days)

