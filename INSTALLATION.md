# Installation Guide

## Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** (Python package manager)
- **OpenAI API Key** (required)
- **PageSpeed API Key** (optional, for higher rate limits)

---

## Quick Install

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

Playwright needs browser binaries to capture screenshots:

```bash
playwright install chromium
```

Or install with system dependencies (Linux):

```bash
playwright install chromium --with-deps
```

### 3. Configure API Keys

Edit `config.py` and add your API keys:

```python
class Config:
    # Required
    OPENAI_API_KEY = "sk-your-openai-api-key-here"

    # Optional (for higher PageSpeed API rate limits)
    PAGESPEED_API_KEY = "your-pagespeed-api-key-here"
```

**Getting API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **PageSpeed** (optional): https://console.cloud.google.com/

---

## Verify Installation

Run the configuration check:

```bash
python -c "from config import Config; Config.print_status()"
```

You should see:
```
API Configuration Status:
✓ OpenAI API Key: Configured
✓ PageSpeed API Key: Configured (optional)
```

---

## Running the Application

### Option 1: Command Line Interface

```bash
python agent.py
```

Analyzes the default URL (https://nightwatch.io) with comprehensive analysis.

### Option 2: Simple Web UI (Recommended)

```bash
python webapp.py
```

Opens ChatGPT-like interface at http://localhost:7860

### Option 3: REST API (AgentOS)

```bash
python playground_app.py
```

Starts REST API at http://localhost:7777
- API docs: http://localhost:7777/docs

---

## Package Details

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `agno` | >=0.1.0 | AI agent framework |
| `openai` | >=1.0.0 | OpenAI API client |
| `gradio` | >=4.0.0 | Web UI framework |
| `playwright` | >=1.40.0 | Browser automation (screenshots) |
| `requests` | >=2.31.0 | HTTP requests |
| `beautifulsoup4` | >=4.12.0 | HTML parsing |
| `uvicorn` | >=0.24.0 | ASGI server (for AgentOS) |

### Optional Dependencies

| Package | Purpose |
|---------|---------|
| `python-dotenv` | Load environment variables from .env |
| `httpx` | Enhanced HTTP client |
| `lxml` | Fast XML/HTML processing |

---

## Platform-Specific Notes

### Windows

```bash
# Install requirements
pip install -r requirements.txt

# Install Playwright
playwright install chromium
```

### macOS

```bash
# Install requirements
pip install -r requirements.txt

# Install Playwright with system dependencies
playwright install chromium --with-deps
```

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install -y python3-pip

# Install Python packages
pip install -r requirements.txt

# Install Playwright with dependencies
playwright install chromium --with-deps
```

### Linux (CentOS/RHEL)

```bash
# Install system dependencies
sudo yum install -y python3-pip

# Install Python packages
pip install -r requirements.txt

# Install Playwright
playwright install chromium --with-deps
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'agno'`

**Solution**: Install agno
```bash
pip install agno
```

### Issue: `Playwright executable doesn't exist`

**Solution**: Install Playwright browsers
```bash
playwright install chromium
```

### Issue: `OpenAI API Key not configured`

**Solution**: Add your API key to `config.py`
```python
OPENAI_API_KEY = "sk-your-key-here"
```

### Issue: `PageSpeed API timeout`

**Solutions**:
1. Timeout increased to 90 seconds (already done)
2. Get a PageSpeed API key for priority access
3. System falls back to local analysis automatically

### Issue: Port already in use (7860 or 7777)

**Solution**: Change port in the app file or kill existing process

Windows:
```bash
netstat -ano | findstr :7860
taskkill /PID <process_id> /F
```

Linux/Mac:
```bash
lsof -ti:7860 | xargs kill -9
```

---

## Development Setup

For development with hot-reload:

```bash
# Web UI with auto-reload
gradio webapp.py

# AgentOS with reload
python playground_app.py  # Already has reload=True
```

---

## Updating Dependencies

To update all packages to latest versions:

```bash
pip install --upgrade -r requirements.txt
playwright install chromium
```

---

## Virtual Environment (Recommended)

### Create Virtual Environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install in Virtual Environment

```bash
pip install -r requirements.txt
playwright install chromium
```

### Deactivate

```bash
deactivate
```

---

## Minimal Installation (No UI)

If you only need the CLI (no web UI):

```bash
# Minimal dependencies
pip install agno openai requests beautifulsoup4 playwright

# Install browser
playwright install chromium
```

---

## Docker (Optional)

Coming soon: Dockerfile for containerized deployment

---

## Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed
- [ ] All pip packages installed
- [ ] Playwright chromium installed
- [ ] OpenAI API key configured
- [ ] PageSpeed API key configured (optional)
- [ ] Can run `python agent.py` without errors
- [ ] Can access webapp at http://localhost:7860

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Verify all dependencies installed: `pip list`
3. Check Playwright: `playwright --version`
4. Review error messages carefully
5. Check [docs/](docs/) for detailed documentation

---

## Next Steps

After installation:

1. **Test the CLI**: `python agent.py`
2. **Try the Web UI**: `python webapp.py`
3. **Read the docs**: Check [README.md](README.md)
4. **Explore examples**: See [examples.py](examples.py)

---

**Happy Analyzing! 🚀**
