#!/usr/bin/env python3
"""
Website Analyzer CLI
Command-line interface for website analysis
"""

import os
import sys
import argparse
import json
from pathlib import Path
from config import Config
from src.workflows.unified_workflow import analyze

# Set API keys
os.environ["OPENAI_API_KEY"] = Config.get_openai_key()
if Config.PAGESPEED_API_KEY:
    os.environ["PAGESPEED_API_KEY"] = Config.PAGESPEED_API_KEY


def print_banner():
    """Print CLI banner"""
    print("\n" + "="*70)
    print("WEBSITE ANALYZER CLI")
    print("="*70 + "\n")


def cmd_analyze(args):
    """Analyze a website, HTML, or screenshots"""
    print_banner()

    # Validate configuration
    if not Config.validate_required_keys():
        print("[ERROR] API keys not configured")
        print("\nPlease configure your OpenAI API key in config.py:")
        print("  OPENAI_API_KEY = 'sk-your-key-here'")
        sys.exit(1)

    # Determine input type
    if args.url:
        user_input = args.url
        print(f"Analyzing URL: {args.url}\n")
    elif args.html:
        user_input = args.html
        print("Analyzing HTML content\n")
    elif args.html_file:
        html_file = Path(args.html_file)
        if not html_file.exists():
            print(f"[ERROR] File not found: {args.html_file}")
            sys.exit(1)
        user_input = html_file.read_text(encoding='utf-8')
        print(f"Analyzing HTML from file: {args.html_file}\n")
    elif args.screenshot:
        user_input = {"screenshot": args.screenshot}
        print(f"Analyzing screenshot: {args.screenshot}\n")
    elif args.screenshots:
        # Parse JSON screenshots
        try:
            screenshots = json.loads(args.screenshots)
            user_input = {"screenshots": screenshots}
            print(f"Analyzing multiple screenshots\n")
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format for screenshots")
            print("Expected format: '{\"desktop\": \"path1.png\", \"mobile\": \"path2.png\"}'")
            sys.exit(1)
    else:
        print("[ERROR] No input provided")
        print("Use --url, --html, --html-file, --screenshot, or --screenshots")
        sys.exit(1)

    # Run analysis
    try:
        result = analyze(user_input, stream=not args.no_stream)

        # Print summary if not streaming
        if args.no_stream:
            print(result)

        print("\n" + "="*70)
        print("Analysis complete!")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cmd_config(args):
    """Show configuration status"""
    print_banner()
    Config.print_status()
    print()


def cmd_test(args):
    """Test API connection and configuration"""
    print_banner()
    print("Testing configuration...\n")

    # Check API keys
    print("1. Checking API keys...")
    if Config.validate_required_keys():
        print("   [OK] OpenAI API key configured")
    else:
        print("   [ERROR] OpenAI API key not configured")
        print("      Please set OPENAI_API_KEY in config.py")
        sys.exit(1)

    if Config.PAGESPEED_API_KEY:
        print("   [OK] PageSpeed API key configured")
    else:
        print("   [WARN] PageSpeed API key not configured (optional)")

    # Test OpenAI connection
    print("\n2. Testing OpenAI connection...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=Config.get_openai_key())
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("   [OK] OpenAI API connection successful")
    except Exception as e:
        print(f"   [ERROR] OpenAI API connection failed: {str(e)}")
        sys.exit(1)

    # Check Playwright
    print("\n3. Checking Playwright installation...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        print("   [OK] Playwright and Chromium installed")
    except Exception as e:
        print(f"   [ERROR] Playwright check failed: {str(e)}")
        print("      Run: playwright install chromium")
        sys.exit(1)

    print("\n" + "="*70)
    print("All tests passed! System is ready.")
    print("="*70 + "\n")


def cmd_examples(args):
    """Show usage examples"""
    print_banner()
    print("USAGE EXAMPLES\n")

    examples = [
        ("Analyze a URL", "python cli.py analyze --url https://example.com"),
        ("Analyze HTML from file", "python cli.py analyze --html-file index.html"),
        ("Analyze inline HTML", 'python cli.py analyze --html "<html><head><title>Test</title></head></html>"'),
        ("Analyze screenshot", "python cli.py analyze --screenshot path/to/screenshot.png"),
        ("Analyze multiple screenshots", 'python cli.py analyze --screenshots \'{"desktop": "d.png", "mobile": "m.png"}\''),
        ("Non-streaming output", "python cli.py analyze --url https://example.com --no-stream"),
        ("Check configuration", "python cli.py config"),
        ("Test system", "python cli.py test"),
    ]

    for i, (desc, cmd) in enumerate(examples, 1):
        print(f"{i}. {desc}")
        print(f"   {cmd}\n")

    print("="*70)
    print("For more help: python cli.py --help")
    print("For command help: python cli.py analyze --help")
    print("="*70 + "\n")


def cmd_api(args):
    """Start the REST API server"""
    print_banner()
    print("Starting REST API server...\n")

    # Validate configuration
    if not Config.validate_required_keys():
        print("[ERROR] API keys not configured")
        sys.exit(1)

    Config.print_status()

    print("\nAPI Endpoints:")
    print(f"  - API: http://{args.host}:{args.port}")
    print(f"  - Docs: http://{args.host}:{args.port}/docs")
    print(f"  - ReDoc: http://{args.host}:{args.port}/redoc")
    print(f"  - Health: http://{args.host}:{args.port}/health")

    print("\n" + "="*70)
    print("Starting server... (Press Ctrl+C to stop)")
    print("="*70 + "\n")

    # Start API
    try:
        import uvicorn
        from api import app
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
    except ImportError:
        print("[ERROR] FastAPI/uvicorn not installed")
        print("Install with: pip install fastapi uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        sys.exit(0)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Website Analyzer CLI - Comprehensive SEO, Performance, and UI/UX analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze --url https://example.com
  %(prog)s analyze --html-file index.html
  %(prog)s config
  %(prog)s test
  %(prog)s api
  %(prog)s examples

For more information: https://github.com/your-repo
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a website, HTML, or screenshots'
    )

    input_group = analyze_parser.add_argument_group('input options (choose one)')
    input_group.add_argument(
        '--url',
        metavar='URL',
        help='Website URL to analyze (e.g., https://example.com)'
    )
    input_group.add_argument(
        '--html',
        metavar='HTML',
        help='Raw HTML content to analyze'
    )
    input_group.add_argument(
        '--html-file',
        metavar='FILE',
        help='Path to HTML file to analyze'
    )
    input_group.add_argument(
        '--screenshot',
        metavar='PATH',
        help='Path to screenshot image for UI/UX analysis'
    )
    input_group.add_argument(
        '--screenshots',
        metavar='JSON',
        help='JSON object with multiple screenshots (e.g., \'{"desktop": "d.png", "mobile": "m.png"}\')'
    )

    analyze_parser.add_argument(
        '--no-stream',
        action='store_true',
        help='Disable streaming output (wait for complete results)'
    )
    analyze_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose error messages'
    )

    analyze_parser.set_defaults(func=cmd_analyze)

    # Config command
    config_parser = subparsers.add_parser(
        'config',
        help='Show configuration status'
    )
    config_parser.set_defaults(func=cmd_config)

    # Test command
    test_parser = subparsers.add_parser(
        'test',
        help='Test API connection and system configuration'
    )
    test_parser.set_defaults(func=cmd_test)

    # Examples command
    examples_parser = subparsers.add_parser(
        'examples',
        help='Show usage examples'
    )
    examples_parser.set_defaults(func=cmd_examples)

    # API command
    api_parser = subparsers.add_parser(
        'api',
        help='Start the REST API server'
    )
    api_parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind (default: 0.0.0.0)'
    )
    api_parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind (default: 8000)'
    )
    api_parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload on code changes'
    )
    api_parser.set_defaults(func=cmd_api)

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute command
    args.func(args)


if __name__ == "__main__":
    main()
