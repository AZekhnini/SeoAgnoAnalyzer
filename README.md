# Website Analyzer

AI-powered website analysis for SEO, Performance, and UI/UX evaluation using Agno workflows and vision models.

## Features

- **SEO Analysis**: Meta tags, headings, content structure, schema markup
- **Performance Analysis**: Core Web Vitals, load times, resource optimization
- **UI/UX Analysis**: Visual design, accessibility (WCAG), responsive design with GPT-4o vision
- **Smart Input Detection**: Automatically detects URL, HTML, or screenshots
- **Flexible Interface**: CLI, REST API, or Python module

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install browser for screenshots
playwright install chromium
```

### Configuration

**Option 1: Using config.py (Recommended for development)**

Copy the example config and add your API keys:
```bash
cp config.example.py config.py
# Edit config.py and add your API keys
```

**Option 2: Using environment variables (Recommended for production)**

```bash
export OPENAI_API_KEY="your-openai-api-key"
export PAGESPEED_API_KEY="optional-pagespeed-key"  # Optional
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-openai-api-key
PAGESPEED_API_KEY=optional-pagespeed-key
```

**Get API Keys:**
- OpenAI API Key (required): https://platform.openai.com/api-keys
- PageSpeed API Key (optional): https://developers.google.com/speed/docs/insights/v5/get-started

### Usage

**CLI (Recommended):**
```bash
python cli.py analyze --url https://example.com
python cli.py test
python cli.py config
```

**Python:**
```python
from src.workflows.unified_workflow import analyze
analyze("https://example.com", stream=True)
```

**REST API:**
```bash
python api.py
# Open http://localhost:8000/docs
```

**Playground (Interactive UI):**
```bash
python playground_app.py
# Open http://localhost:7777
```

## Project Structure

```
├── src/
│   ├── agents/          # AI agents (SEO, Performance, UI/UX, Summary)
│   ├── extractors/      # Feature extraction modules
│   ├── instructions/    # Agent prompts
│   └── workflows/       # Workflow definitions
├── cli.py               # Command-line interface
├── api.py               # REST API server
├── playground_app.py    # Interactive playground UI
└── config.py            # Configuration
```

## Input Options

- **URL**: Full analysis (SEO + Performance + UI/UX)
- **HTML**: SEO analysis only
- **Screenshot(s)**: UI/UX analysis only

## Documentation

- [CLI Guide](CLI_GUIDE.md) - CLI commands and options