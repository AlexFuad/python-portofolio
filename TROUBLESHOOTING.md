# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Import "customtkinter" could not be resolved

**Problem:**
IDE shows warning: `Import "customtkinter" could not be resolved`

**Solutions:**

#### Solution A: Select the Correct Python Interpreter (Recommended)
1. Press `Ctrl+Shift+P` in VSCode
2. Type `Python: Select Interpreter`
3. Choose the interpreter from `.venv` folder:
   - `./.venv/Scripts/python.exe` (Windows)
4. Wait a few seconds for IntelliSense to update

#### Solution B: Install in User Site Packages
```bash
pip install --user customtkinter
```

#### Solution C: Use # type: ignore Comment
Add this comment to the import line:
```python
import customtkinter as ctk  # type: ignore
```

#### Solution D: Disable the Warning
Add to `.vscode/settings.json`:
```json
{
    "python.analysis.ignoreImports": ["customtkinter"]
}
```

### 2. ModuleNotFoundError: No module named 'customtkinter'

**Problem:**
Runtime error when running the application

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install customtkinter requests Pillow
```

### 3. tkinter.TclError: cannot use geometry manager pack inside ...

**Problem:**
Mixing `pack()` and `grid()` in the same container

**Solution:**
- Use `pack()` OR `grid()` consistently within the same parent container
- Use inner frames to separate different geometry managers

### 4. Application Window Not Appearing

**Problem:**
Script runs but no window shows

**Solutions:**
- Ensure `app.mainloop()` is at the end of the script
- Check if window is hidden behind other windows
- Try increasing window size in `geometry()` setting

### 5. API Connection Errors

**Weather Checker:**
- Check internet connection
- Verify API key in `config.py`
- API key might need 2 hours to activate after creation

**Recipe Finder:**
- Check internet connection
- TheMealDB is free and doesn't require API key
- API might be temporarily down (rare)

### 6. Slow Performance

**Solutions:**
- Close unused applications
- Check system resources (RAM, CPU)
- Applications use multi-threading to prevent UI freezing

### 7. Virtual Environment Issues

**Problem:**
Dependencies installed but not recognized

**Solution:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## IDE-Specific Fixes

### VSCode

1. **Reload Window:** `Ctrl+Shift+P` → `Developer: Reload Window`
2. **Clear Cache:** Delete `.vscode` folder and reopen VSCode
3. **Update Extensions:** Ensure Python extension is up to date

### PyCharm

1. Go to `File` → `Settings` → `Project` → `Python Interpreter`
2. Select the correct interpreter (`.venv/Scripts/python.exe`)
3. Click refresh button

### Other IDEs

- Ensure IDE is using the correct Python interpreter
- Restart IDE after installing new packages
- Check IDE documentation for configuring Python paths

## Quick Fixes Checklist

- [ ] Run `pip install -r requirements.txt`
- [ ] Select correct Python interpreter in IDE
- [ ] Restart IDE
- [ ] Run application from terminal to verify it works
- [ ] Check Python version (need 3.7+): `python --version`

## Still Having Issues?

1. **Check Python Version:**
   ```bash
   python --version
   ```
   Should be 3.7 or higher

2. **Verify Installation:**
   ```bash
   pip list | findstr customtkinter  # Windows
   pip list | grep customtkinter     # Mac/Linux
   ```

3. **Test Individual Module:**
   ```bash
   python -c "import customtkinter; print(customtkinter.__version__)"
   ```

4. **Clean Reinstall:**
   ```bash
   pip uninstall customtkinter -y
   pip install customtkinter
   ```

## Contact & Support

If issues persist:
- Check project GitHub issues
- Search for error messages online
- Review Python and package documentation

---

*Last updated: 2026-04-06*
