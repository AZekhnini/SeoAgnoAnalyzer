# CLI Guide

## Commands

### analyze
Analyze a website, HTML, or screenshots.

```bash
# Analyze URL
python cli.py analyze --url https://example.com

# Analyze HTML file
python cli.py analyze --html-file index.html

# Analyze raw HTML
python cli.py analyze --html "<html>...</html>"

# Analyze screenshot
python cli.py analyze --screenshot screenshot.png

# Analyze multiple screenshots
python cli.py analyze --screenshots '{"desktop": "d.png", "mobile": "m.png"}'

# Disable streaming
python cli.py analyze --url https://example.com --no-stream
```

### config
Show API configuration status.

```bash
python cli.py config
```

### test
Test system configuration and API connections.

```bash
python cli.py test
```

### examples
Show usage examples.

```bash
python cli.py examples
```

### api
Start REST API server.

```bash
python cli.py api
python cli.py api --host 0.0.0.0 --port 8080 --reload
```

## Options

### analyze Command

- `--url URL` - Website URL to analyze
- `--html HTML` - Raw HTML content
- `--html-file FILE` - Path to HTML file
- `--screenshot PATH` - Path to screenshot image
- `--screenshots JSON` - JSON with multiple screenshots
- `--no-stream` - Wait for complete results
- `--verbose` - Show detailed errors

### api Command

- `--host HOST` - Bind host (default: 0.0.0.0)
- `--port PORT` - Bind port (default: 8000)
- `--reload` - Auto-reload on code changes

## Examples

**Basic URL analysis:**
```bash
python cli.py analyze --url https://nightwatch.io
```

**SEO-only analysis (HTML):**
```bash
python cli.py analyze --html-file landing-page.html
```

**UI/UX analysis (screenshots):**
```bash
python cli.py analyze --screenshots '{"desktop": "desktop.png", "mobile": "mobile.png"}'
```

**Non-streaming output:**
```bash
python cli.py analyze --url https://example.com --no-stream
```
