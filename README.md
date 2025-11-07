# Website Analyzer 🚀

> Comprehensive AI-powered website analysis system for SEO, Performance, and UI/UX evaluation using Agno workflows and vision models.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Agno](https://img.shields.io/badge/Agno-Latest-green.svg)](https://docs.agno.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

This project provides an intelligent website analysis system that evaluates websites across three critical dimensions:

- **SEO Analysis**: Meta tags, headings, content structure, schema markup, social media optimization
- **Performance Analysis**: PageSpeed Insights, Core Web Vitals, load times, resource optimization
- **UI/UX Analysis**: Visual design, accessibility compliance (WCAG), responsive design (with vision AI)

The system uses **Agno workflows** with AI agents to provide comprehensive, actionable insights and recommendations.

---

## Key Features

### 🎯 Unified Workflow
- **Smart Input Detection**: Automatically determines analysis type based on input (URL, HTML, or screenshots)
- **Conditional Execution**: Runs only relevant analyses based on available data
- **Comprehensive Reports**: Executive summary with prioritized recommendations

### 🤖 AI-Powered Analysis
- **Input Classifier**: Intelligently detects input type and extracts content from natural language prompts
- **SEO Analyst**: Evaluates search engine optimization and content quality
- **Performance Analyst**: Analyzes load times, Core Web Vitals, and bottlenecks
- **UI/UX Analyst**: Vision-enabled agent (GPT-4o) for visual design and accessibility analysis
- **Summary Analyst**: Synthesizes all findings into actionable recommendations

### 👁️ Vision Model Integration
- **Screenshot Analysis**: Automatically captures website screenshots at 3 viewports (desktop, tablet, mobile)
- **Visual Design Evaluation**: Color schemes, typography, layout, white space
- **Responsive Design**: Cross-device consistency analysis
- **Accessibility**: Visual contrast checks combined with automated WCAG audits

### 📊 Flexible Input Options
Accepts natural language prompts or direct input:
1. **URL**: `https://example.com` or `"Analyze the website: https://example.com"`
2. **HTML**: Raw HTML code or `"Check this HTML: <div>...</div>"`
3. **Screenshot(s)**: File paths or JSON with image references

The intelligent classifier automatically detects the input type and extracts the content!

---

## Project Structure

```
website-analyzer/
├── src/
│   ├── agents/                    # AI agent definitions
│   │   ├── seo_agent.py          # SEO analyst
│   │   ├── performance_agent.py  # Performance analyst
│   │   ├── uiux_agent.py         # UI/UX analyst (vision-enabled)
│   │   └── summary_agent.py      # Executive summary analyst
│   ├── extractors/                # Feature extraction modules
│   │   ├── html_extractor.py     # SEO feature extraction
│   │   ├── performance_extractor.py  # Performance metrics extraction
│   │   └── uiux_extractor.py     # Screenshot capture & accessibility audit
│   ├── instructions/              # Agent instructions & prompts
│   │   ├── classifier_instructions.py  # Input classification rules
│   │   ├── seo_instructions.py   # SEO analysis guidelines
│   │   ├── performance_instructions.py  # Performance evaluation criteria
│   │   ├── uiux_instructions.py  # UI/UX analysis framework
│   │   └── summary_instructions.py  # Executive summary structure
│   └── workflows/                 # Workflow definitions
│       ├── unified_workflow.py   # Main unified workflow
│       ├── workflow.py           # SEO-only workflow
│       └── performance_workflow.py  # Performance-only workflow
├── cli.py                         # Command-line interface (main entry point)
├── api.py                         # REST API server
├── webapp.py                      # Simple web interface
├── examples.py                    # Usage examples
├── config.py                      # Configuration & API keys
└── README.md                      # This file
```

---

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key (required)
- PageSpeed Insights API key (optional, for higher rate limits)

### 1. Clone & Install Dependencies

```bash
# Install Python packages
pip install agno requests playwright beautifulsoup4

# Install Playwright browsers (required for UI/UX analysis)
playwright install chromium
```

### 2. Configure API Keys

Edit `config.py` and add your API keys:

```python
class Config:
    OPENAI_API_KEY = "your-openai-api-key-here"
    PAGESPEED_API_KEY = "your-pagespeed-api-key-here"  # Optional
```

---

## Usage

### Command-Line Interface (Recommended)

The CLI provides the easiest way to use the analyzer:

```bash
# Analyze a website
python cli.py analyze --url https://example.com

# Check configuration
python cli.py config

# Test system
python cli.py test

# Show all commands
python cli.py --help
```

See [CLI_GUIDE.md](CLI_GUIDE.md) for complete CLI documentation.

### Python Module Usage

You can also use the analyzer programmatically in your Python code:

```python
from src.workflows.unified_workflow import analyze

# Run comprehensive analysis on a URL
analyze("https://example.com", stream=True)
```

See [examples.py](examples.py) for more usage examples.

### Input Options

#### Option 1: Comprehensive Analysis (URL)
```python
analyze("https://example.com", stream=True)
```
**Runs**: SEO + Performance + UI/UX

#### Option 2: SEO Only (HTML)
```python
html = "<html><head><title>Test</title></head><body>...</body></html>"
analyze(html, stream=True)
```
**Runs**: SEO analysis only

#### Option 3: UI/UX Only (Single Screenshot)
```python
analyze({"screenshot": "path/to/screenshot.png"}, stream=True)
```
**Runs**: UI/UX analysis only

#### Option 4: UI/UX Only (Multiple Screenshots)
```python
analyze({
    "screenshots": {
        "desktop": "desktop.png",
        "tablet": "tablet.png",
        "mobile": "mobile.png"
    }
}, stream=True)
```
**Runs**: UI/UX responsive design analysis

#### Option 5: URL with Custom Screenshots
```python
analyze({
    "url": "https://example.com",
    "screenshots": {
        "desktop": "custom_desktop.png",
        "mobile": "custom_mobile.png"
    }
}, stream=True)
```
**Runs**: All analyses but uses your screenshots instead of capturing new ones

---

## REST API

Launch the REST API:

```bash
python api.py
```

### API Endpoints

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Key Endpoints

- `POST /analyze` - Synchronous analysis (waits for completion)
- `POST /analyze/async` - Asynchronous analysis (returns immediately)
- `GET /analyze/{id}` - Check analysis status and retrieve results
- `GET /health` - API health check

See [API_EXAMPLES.md](API_EXAMPLES.md) for usage examples with cURL, Python, and JavaScript.

---

## Analysis Output

### Executive Summary Structure

The unified workflow produces:

1. **SEO Analysis**
   - Overall score (0-100)
   - Meta tags evaluation
   - Content structure assessment
   - Schema markup review
   - Actionable recommendations

2. **Performance Analysis**
   - Overall score (0-100)
   - Core Web Vitals (LCP, FID, CLS)
   - Load time metrics
   - Resource optimization opportunities
   - Performance bottlenecks

3. **UI/UX Analysis** *(Vision-powered)*
   - Visual Design (25 pts): Color, typography, layout, white space
   - Accessibility (25 pts): WCAG compliance, contrast, focus indicators
   - Responsive Design (25 pts): Cross-device consistency
   - User Experience (25 pts): Navigation, CTAs, content hierarchy

4. **Executive Summary**
   - Overall website grade (A-F)
   - Top 5 critical issues
   - Prioritized recommendations (4 tiers)
   - Quick wins (< 2 hours each)
   - Clear action plan

---

## Cost Estimates

### Per Full Analysis (URL)

| Component | Cost |
|-----------|------|
| SEO Analysis | ~$0.001-0.003 |
| Performance Analysis | ~$0.001-0.003 |
| UI/UX Analysis (3 screenshots) | ~$0.015-0.025 |
| Executive Summary | ~$0.001-0.002 |
| **Total** | **~$0.018-0.033** |

### Notes
- Screenshot capture: Free (local Playwright)
- Accessibility audit: Free (local JavaScript)
- Vision model (GPT-4o): Most expensive component
- PageSpeed API: Free (with optional API key for higher limits)

---

## Architecture Highlights

### Conditional Workflow Execution

The unified workflow intelligently determines what to analyze:

```python
# URL input → All 3 analyses
analyze("https://example.com")

# HTML input → SEO only
analyze("<html>...</html>")

# Screenshot input → UI/UX only
analyze({"screenshot": "image.png"})
```

### Vision Model Integration

UI/UX analysis uses **GPT-4o vision** to analyze screenshots:

1. Playwright captures screenshots at 3 viewports
2. Screenshots encoded as base64
3. Converted to `agno.media.Image` objects
4. Passed to vision agent with context
5. Agent analyzes visual design, layout, colors, typography

See [docs/VISION_IMPLEMENTATION.md](docs/VISION_IMPLEMENTATION.md) for technical details.

### Agno Workflow Steps

Each analysis follows a 2-step pattern:

1. **Feature Extraction** (free/low-cost): Scrape HTML, capture screenshots, run audits
2. **AI Analysis** (costs tokens): Agent analyzes extracted data and provides insights

This minimizes LLM usage and costs.

---

## Configuration

### API Keys

**Required:**
- `OPENAI_API_KEY`: For AI agents (GPT-4o, GPT-4o-mini)

**Optional:**
- `PAGESPEED_API_KEY`: Increases PageSpeed Insights rate limits

### Model Selection

- **SEO Agent**: `gpt-4o-mini` (text analysis)
- **Performance Agent**: `gpt-4o-mini` (text analysis)
- **UI/UX Agent**: `gpt-4o` (vision capabilities required)
- **Summary Agent**: `gpt-4o-mini` (text synthesis)

---

## Documentation

- [Unified Workflow Architecture](docs/UNIFIED_WORKFLOW.md)
- [Vision Model Implementation](docs/VISION_IMPLEMENTATION.md)
- [UI/UX Phase Details](docs/UIUX_PHASE.md)
- [SEO Enhancements](docs/PHASE1_ENHANCEMENTS.md)
- [Performance Enhancements](docs/PHASE2_ENHANCEMENTS.md)
- [Playground Deployment](docs/PLAYGROUND_DEPLOYMENT.md)
- [Playwright Installation](docs/INSTALL_PLAYWRIGHT.md)

---

## Troubleshooting

### Playwright Installation Issues

If screenshot capture fails:
```bash
playwright install chromium --with-deps
```

See [docs/INSTALL_PLAYWRIGHT.md](docs/INSTALL_PLAYWRIGHT.md) for OS-specific instructions.

### PageSpeed API Timeout

If you get timeout errors, the timeout has been increased to 90 seconds. For slower sites:
- Use local fallback (automatic when API fails)
- Get a PageSpeed API key for priority access

### Import Errors

Ensure you're running from the project root:
```bash
cd "path/to/Test app v2"
python cli.py analyze --url https://example.com
```

---

## Future Enhancements

- [ ] A/B testing comparison
- [ ] Multi-page crawling and analysis
- [ ] Design system consistency checks
- [ ] Video analysis for animations
- [ ] Accessibility overlay visualizations
- [ ] Historical tracking and trends

---

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License - see LICENSE file for details.

---

## Credits

Built with:
- [Agno](https://docs.agno.com/) - AI agent framework
- [Playwright](https://playwright.dev/) - Browser automation
- [OpenAI](https://openai.com/) - GPT-4o vision model
- [PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about) - Performance metrics

---

## Contact

For questions or support, please open an issue or contact the maintainers.

---

**Happy Analyzing! 🚀**
