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

# Non-streaming mode (wait for complete results)
python cli.py analyze --url https://nightwatch.io --no-stream
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


---

### 3. `test` - Test System

Verify API connections and system requirements.

```bash
python cli.py test
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

## Complete Examples

### Example 1: Analyze URL and Save Report

```bash
python cli.py analyze \
  --url https://nightwatch.io
```

### Example 2: HTML File Analysis

```bash
python cli.py analyze \
  --html-file ~/websites/index.html
```

### Example 3: Screenshot Analysis

```bash
python cli.py analyze \
  --screenshot ~/screenshots/homepage.png
```

### Example 4: Responsive Design Analysis

```bash
python cli.py analyze \
  --screenshots '{"desktop": "desktop.png", "tablet": "tablet.png", "mobile": "mobile.png"}'
```

### Example 5: Quick URL Check (No Streaming)

```bash
python cli.py analyze \
  --url https://example.com \
  --no-stream \
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
