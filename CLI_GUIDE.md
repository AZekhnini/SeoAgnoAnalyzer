# CLI Guide

Complete guide for using the Website Analyzer command-line interface.

---

## Quick Start

```bash
# Show all commands
python cli.py --help

# Analyze a website
python cli.py analyze --url https://example.com

# Check configuration
python cli.py config

# Test system
python cli.py test

# Start REST API
python cli.py api
```

---

## Commands

### 1. `analyze` - Analyze Websites

Perform comprehensive analysis on URLs, HTML, or screenshots.

#### Basic Usage

```bash
# Analyze a URL (full analysis: SEO + Performance + UI/UX)
python cli.py analyze --url https://nightwatch.io

# Analyze with output file
python cli.py analyze --url https://example.com --output report.md

# Non-streaming mode (wait for complete results)
python cli.py analyze --url https://example.com --no-stream
```

#### HTML Analysis

```bash
# Analyze HTML from file (SEO only)
python cli.py analyze --html-file index.html

# Analyze inline HTML
python cli.py analyze --html "<html><head><title>Test</title></head><body>Hello</body></html>"
```

#### Screenshot Analysis

```bash
# Single screenshot (UI/UX only)
python cli.py analyze --screenshot path/to/screenshot.png

# Multiple screenshots for responsive analysis
python cli.py analyze --screenshots '{"desktop": "desktop.png", "mobile": "mobile.png"}'
```

#### Options

| Option | Description |
|--------|-------------|
| `--url URL` | Website URL to analyze |
| `--html HTML` | Raw HTML content |
| `--html-file FILE` | Path to HTML file |
| `--screenshot PATH` | Single screenshot path |
| `--screenshots JSON` | Multiple screenshots as JSON |
| `--output FILE` | Save results to file |
| `--no-stream` | Disable streaming output |
| `--verbose` | Show detailed error messages |

---

### 2. `config` - Show Configuration

Display API key configuration status.

```bash
python cli.py config
```

**Output:**
```
API Configuration Status:
✓ OpenAI API Key: Configured
✓ PageSpeed API Key: Configured (optional)
```

---

### 3. `test` - Test System

Verify API connections and system requirements.

```bash
python cli.py test
```

**Checks:**
1. API keys configured
2. OpenAI API connection
3. Playwright installation

**Output:**
```
1. Checking API keys...
   ✅ OpenAI API key configured

2. Testing OpenAI connection...
   ✅ OpenAI API connection successful

3. Checking Playwright installation...
   ✅ Playwright and Chromium installed

✅ All tests passed! System is ready.
```

---

### 4. `api` - Start REST API Server

Launch the FastAPI REST API server.

```bash
# Default (http://0.0.0.0:8000)
python cli.py api

# Custom host and port
python cli.py api --host 127.0.0.1 --port 3000

# With auto-reload (development)
python cli.py api --reload
```

#### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | 0.0.0.0 | Host to bind |
| `--port` | 8000 | Port to bind |
| `--reload` | False | Enable auto-reload on code changes |

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 5. `examples` - Show Examples

Display usage examples for all commands.

```bash
python cli.py examples
```

---

## Complete Examples

### Example 1: Analyze URL and Save Report

```bash
python cli.py analyze \
  --url https://nightwatch.io \
  --output nightwatch_report.md
```

### Example 2: HTML File Analysis

```bash
python cli.py analyze \
  --html-file ~/websites/index.html \
  --output seo_report.md
```

### Example 3: Screenshot Analysis

```bash
python cli.py analyze \
  --screenshot ~/screenshots/homepage.png \
  --output uiux_report.md
```

### Example 4: Responsive Design Analysis

```bash
python cli.py analyze \
  --screenshots '{"desktop": "desktop.png", "tablet": "tablet.png", "mobile": "mobile.png"}' \
  --output responsive_report.md
```

### Example 5: Quick URL Check (No Streaming)

```bash
python cli.py analyze \
  --url https://example.com \
  --no-stream \
  --output report.md
```

---

## Input Types

### URLs
Full analysis including SEO, Performance, and UI/UX (with screenshot capture).

```bash
python cli.py analyze --url https://example.com
```

### HTML Content
SEO analysis only (no performance or UI/UX).

```bash
# From file
python cli.py analyze --html-file page.html

# Inline
python cli.py analyze --html "<html>...</html>"
```

### Screenshots
UI/UX analysis only (visual design and accessibility).

```bash
# Single
python cli.py analyze --screenshot image.png

# Multiple
python cli.py analyze --screenshots '{"desktop": "d.png", "mobile": "m.png"}'
```

---

## Output Formats

### Streaming Output (Default)

Results appear in real-time as analysis progresses:

```bash
python cli.py analyze --url https://example.com
```

**Output:**
```
🚀 WEBSITE ANALYZER CLI
======================================================================

📊 Analyzing URL: https://example.com

[Classifier] Analyzing input type...
[Classifier] ✓ Classification complete

# SEO Analysis
...

# Performance Analysis
...

# UI/UX Analysis
...

✅ Analysis complete!
```

### Non-Streaming Output

Wait for complete results before displaying:

```bash
python cli.py analyze --url https://example.com --no-stream
```

### Save to File

```bash
python cli.py analyze --url https://example.com --output report.md
```

**Files created:**
- `report.md` - Full markdown report

---

## Error Handling

### Verbose Mode

Enable detailed error messages for debugging:

```bash
python cli.py analyze --url https://example.com --verbose
```

### Common Errors

#### 1. API Key Not Configured

```
❌ Error: API keys not configured
Please configure your OpenAI API key in config.py
```

**Solution:** Edit `config.py` and add your OpenAI API key.

#### 2. Playwright Not Installed

```
❌ Playwright check failed
Run: playwright install chromium
```

**Solution:** Run `playwright install chromium`

#### 3. Invalid Input

```
❌ Error: No input provided
Use --url, --html, --html-file, --screenshot, or --screenshots
```

**Solution:** Provide one input option.

---

## Tips & Best Practices

### 1. Use Streaming for Long Analysis

For URLs (which include all analysis types), use streaming to see progress:

```bash
python cli.py analyze --url https://example.com
```

### 2. Save Reports for Later

Always save reports for documentation:

```bash
python cli.py analyze --url https://example.com --output reports/$(date +%Y%m%d)_report.md
```

### 3. Test Configuration First

Before running analysis, verify configuration:

```bash
python cli.py test
```

### 4. Use Non-Streaming for Automation

When piping or scripting, use `--no-stream`:

```bash
python cli.py analyze --url https://example.com --no-stream > output.txt
```

### 5. Batch Analysis Script

Create a bash script for multiple URLs:

```bash
#!/bin/bash
urls=(
  "https://example1.com"
  "https://example2.com"
  "https://example3.com"
)

for url in "${urls[@]}"; do
  domain=$(echo $url | sed 's|https\?://||' | sed 's|/.*||')
  python cli.py analyze --url "$url" --output "reports/${domain}_report.md"
done
```

---

## Integration Examples

### Cron Job (Daily Analysis)

```bash
# Edit crontab
crontab -e

# Add daily analysis at 2 AM
0 2 * * * cd /path/to/project && python cli.py analyze --url https://example.com --output /path/to/reports/$(date +\%Y\%m\%d).md
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Website Analysis

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium

      - name: Run analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python cli.py analyze --url https://example.com --output report.md

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: analysis-report
          path: report.md
```

---

## Comparison with API and agent.py

| Feature | CLI (`cli.py`) | API (`api.py`) | Direct (`agent.py`) |
|---------|---------------|---------------|-------------------|
| **Interface** | Command-line | REST API | Python code |
| **Use Case** | Scripts, automation | Web apps, integrations | Development |
| **Multiple commands** | ✅ Yes | N/A | N/A |
| **Config check** | ✅ Yes | Via `/health` | No |
| **System test** | ✅ Yes | No | No |
| **Start API** | ✅ Yes | Direct | No |
| **Output file** | ✅ Yes | Via code | Via code |
| **Examples** | ✅ Built-in | In docs | Separate file |

---

## Troubleshooting

### Issue: Command not found

```bash
python: command not found
```

**Solution:** Use `python3` or `py` depending on your system:

```bash
python3 cli.py --help
# or
py cli.py --help
```

### Issue: Module not found

```bash
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Issue: Permission denied

```bash
Permission denied: ./cli.py
```

**Solution (Linux/Mac):** Make executable:

```bash
chmod +x cli.py
./cli.py --help
```

---

## Getting Help

```bash
# General help
python cli.py --help

# Command-specific help
python cli.py analyze --help
python cli.py api --help

# Show examples
python cli.py examples

# Check version
python cli.py --version
```

---

**Happy Analyzing! 🚀**
