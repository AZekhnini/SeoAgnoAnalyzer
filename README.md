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

Create `config.py`:

```python
class Config:
    OPENAI_API_KEY = "your-openai-api-key"
    PAGESPEED_API_KEY = "optional-pagespeed-key"
```

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
- [API Examples](API_EXAMPLES.md) - REST API usage
- [Installation](INSTALLATION.md) - Detailed setup instructions

## Cost Estimates

Approximate cost per full URL analysis: **$0.02-0.03**

- SEO: ~$0.001
- Performance: ~$0.001
- UI/UX (vision): ~$0.015-0.025
- Summary: ~$0.001

## License

MIT License
