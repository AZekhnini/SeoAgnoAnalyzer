# Installation Guide

## Requirements

- Python 3.8+
- OpenAI API key
- PageSpeed API key (optional)

## Installation Steps

### 1. Install Python Packages

```bash
pip install agno requests playwright beautifulsoup4
```

### 2. Install Playwright Browser

```bash
playwright install chromium
```

**Troubleshooting:** If you encounter issues, install with dependencies:
```bash
playwright install chromium --with-deps
```

### 3. Configure API Keys

Create `config.py`:

```python
import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
    PAGESPEED_API_KEY = os.getenv("PAGESPEED_API_KEY", None)

    @classmethod
    def get_openai_key(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        return cls.OPENAI_API_KEY

    @classmethod
    def validate_required_keys(cls):
        return bool(cls.OPENAI_API_KEY)

    @classmethod
    def print_status(cls):
        print("\nAPI Configuration Status:")
        print(f"{'[OK]' if cls.OPENAI_API_KEY else '[ERROR]'} OpenAI API Key: {'Configured' if cls.OPENAI_API_KEY else 'Not configured'}")
        print(f"{'[OK]' if cls.PAGESPEED_API_KEY else '[SKIP]'} PageSpeed API Key: {'Configured' if cls.PAGESPEED_API_KEY else 'Not configured (optional)'}")

if __name__ == "__main__":
    Config.print_status()
```

### 4. Verify Installation

```bash
python cli.py test
```

## Getting API Keys

### OpenAI API Key (Required)
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Create new API key
4. Add to `config.py`

### PageSpeed API Key (Optional)
1. Go to https://developers.google.com/speed/docs/insights/v5/get-started
2. Click "Get a Key"
3. Follow setup instructions
4. Add to `config.py`

## Platform-Specific Notes

### Windows
- Use PowerShell or CMD
- No additional setup required

### macOS
- May need to install system dependencies:
```bash
brew install python3
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip
playwright install-deps chromium
```

## Troubleshooting

**Import Errors:**
Ensure you're in the project root directory:
```bash
cd "path/to/Test app v2"
python cli.py test
```

**Playwright Issues:**
```bash
playwright install chromium --with-deps
```

**Permission Errors (Linux):**
```bash
sudo playwright install-deps
```

**API Connection Issues:**
Verify your API key is correct in `config.py` and run:
```bash
python cli.py config
```
