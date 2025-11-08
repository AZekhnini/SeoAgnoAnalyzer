#!/usr/bin/env python3
"""
Agno Playground App for Website Analyzer
Interactive web interface for testing the unified workflow
"""

import os
from config import Config
from src.workflows.unified_workflow import unified_workflow

# Set API keys
os.environ["OPENAI_API_KEY"] = Config.get_openai_key()
if Config.PAGESPEED_API_KEY:
    os.environ["PAGESPEED_API_KEY"] = Config.PAGESPEED_API_KEY


if __name__ == "__main__":
    # Validate configuration
    print("\n" + "="*70)
    print("WEBSITE ANALYZER PLAYGROUND")
    print("="*70 + "\n")

    Config.print_status()

    if not Config.validate_required_keys():
        print("\n[ERROR] API keys not configured")
        print("Please configure your OpenAI API key in config.py")
        exit(1)

    print("\n" + "="*70)
    print("Starting Agno Playground...")
    print("="*70 + "\n")

    # Serve the playground
    unified_workflow.serve(
        host="0.0.0.0",
        port=7777,
        reload=True
    )
