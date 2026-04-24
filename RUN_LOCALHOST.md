# 🚀 Running the Flask App on Localhost

## Quick Start

### Method 1: Run Directly (Recommended)

1. **Open Terminal/PowerShell** in the project directory:
   ```powershell
   cd "C:\Users\vijai\Desktop\pervasive project"
   ```

2. **Run the Flask app**:
   ```powershell
   python app.py
   ```

3. **Open your browser** and go to:
   - http://127.0.0.1:5000/
   - OR http://localhost:5000/

4. **To stop the server**: Press `Ctrl+C` in the terminal

---

## Method 2: Using Flask Command

```powershell
flask run
```

Then access: http://127.0.0.1:5000/

---

## What You'll See

When the server starts, you'll see:
```
Server running at http://127.0.0.1:5000/
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

## Troubleshooting

### Port 5000 Already in Use

If you get an error that port 5000 is busy:

1. **Find what's using port 5000**:
   ```powershell
   netstat -ano | findstr :5000
   ```

2. **Kill the process** (replace PID with the number from above):
   ```powershell
   taskkill /PID <PID> /F
   ```

3. **Or use a different port**:
   Edit `app.py` and change:
   ```python
   app.run(debug=True, port=5001)
   ```
   Then access: http://127.0.0.1:5001/

---

## Features Available

Once running, you can access:

- ✅ **Stress Prediction** - Main prediction interface
- ✅ **Stress History** - View trajectory over time
- ✅ **Intelligent Alerts** - Consent-aware alerts
- ✅ **Model Dashboard** - Model performance metrics

---

## Default Configuration

- **Host**: 127.0.0.1 (localhost)
- **Port**: 5000
- **Debug Mode**: Enabled (auto-reloads on code changes)

---

## Notes

- The app runs on **localhost only** (127.0.0.1) - not accessible from other devices
- **Debug mode** is enabled, so code changes will auto-reload
- All data is stored in browser **localStorage** (history, user ID)
- CSV dataset is loaded from: `C:\Users\vijai\Downloads\mobile_addiction_data.csv`

