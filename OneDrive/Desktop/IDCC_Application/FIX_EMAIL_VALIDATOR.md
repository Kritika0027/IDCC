# Fix: email-validator not installed

## Quick Fix

Run this command:

```cmd
py -m pip install email-validator
```

Or use the batch file:

```cmd
install_email_validator.bat
```

## Alternative: Install with pydantic[email]

On Windows Command Prompt, use double quotes:

```cmd
py -m pip install "pydantic[email]"
```

Or without quotes (if it works):

```cmd
py -m pip install pydantic[email]
```

## Verify Installation

After installing, verify it's installed:

```cmd
py -m pip show email-validator
```

You should see package information.

## Then Run the App

```cmd
py run.py
```

## If Still Not Working

1. **Check if it's installed**:
   ```cmd
   py -m pip list | findstr email
   ```

2. **Try reinstalling**:
   ```cmd
   py -m pip uninstall email-validator
   py -m pip install email-validator
   ```

3. **Use virtual environment** (recommended):
   ```cmd
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

## Note

The package name is `email-validator` (with a hyphen), but the Python module is `email_validator` (with an underscore). This is normal.

