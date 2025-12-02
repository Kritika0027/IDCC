# How to Access the Application

## ✅ Correct URLs

Once the app is running, use one of these URLs:

- **http://localhost:8000** ← **Use this one!**
- **http://127.0.0.1:8000** ← Alternative

## ❌ Don't Use

- ~~http://0.0.0.0:8000~~ ← This won't work in a browser!

## Why?

- `0.0.0.0` is a **bind address** - it tells the server to listen on all network interfaces
- For accessing from your browser, you need `localhost` or `127.0.0.1`
- `localhost` and `127.0.0.1` both refer to your local machine

## Quick Start

1. **Run the app**:
   ```cmd
   py run.py
   ```

2. **You should see**:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

## If You Want Network Access

If you want to access the app from other devices on your network:

1. Change `host="127.0.0.1"` to `host="0.0.0.0"` in `run.py`
2. Find your computer's IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)
3. Access from other devices using: `http://192.168.1.100:8000`

## Troubleshooting

**Can't connect?**
- Make sure the app is running (check the terminal)
- Try `http://127.0.0.1:8000` instead
- Check if port 8000 is already in use

**Port already in use?**
- Change port in `run.py`: `port=8001`
- Then access at: `http://localhost:8001`

