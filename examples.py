"""
Example Usage Scripts
Demonstrates different ways to use the unified workflow.
"""

import os
from config import Config
from src.workflows.unified_workflow import analyze

# Set API key
os.environ["OPENAI_API_KEY"] = Config.get_openai_key()


def example_1_comprehensive_url_analysis():
    """
    Example 1: Full comprehensive analysis of a website
    Runs: SEO + Performance + UI/UX + Summary
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Comprehensive URL Analysis")
    print("="*70 + "\n")

    url = "https://nightwatch.io"
    analyze(url, stream=True)


def example_2_seo_only_html():
    """
    Example 2: SEO-only analysis from raw HTML
    Runs: SEO + Summary (SEO only)
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: SEO Only (HTML Input)")
    print("="*70 + "\n")

    html = """
    <html>
    <head>
        <title>Complete SEO Guide 2024 | Best Practices</title>
        <meta name="description" content="Learn the latest SEO best practices and techniques to improve your website's search engine rankings in 2024.">
        <meta property="og:title" content="Complete SEO Guide 2024">
        <meta property="og:description" content="Master SEO with our comprehensive guide">
        <meta name="twitter:card" content="summary_large_image">
    </head>
    <body>
        <header>
            <h1>Complete SEO Guide 2024</h1>
            <nav>
                <a href="#intro">Introduction</a>
                <a href="#basics">SEO Basics</a>
                <a href="#advanced">Advanced Topics</a>
            </nav>
        </header>

        <main>
            <article>
                <h2 id="intro">Introduction to SEO</h2>
                <p>Search Engine Optimization is crucial for digital success...</p>

                <h2 id="basics">SEO Basics</h2>
                <p>Understanding the fundamentals of SEO is essential...</p>

                <h3>On-Page SEO</h3>
                <p>On-page SEO refers to optimizations you can make on your website...</p>

                <h3>Off-Page SEO</h3>
                <p>Off-page SEO involves activities outside your website...</p>

                <h2 id="advanced">Advanced SEO Topics</h2>
                <p>Once you master the basics, explore advanced techniques...</p>
            </article>
        </main>

        <footer>
            <p>&copy; 2024 SEO Experts</p>
        </footer>
    </body>
    </html>
    """

    analyze(html, stream=True)


def example_3_uiux_single_screenshot():
    """
    Example 3: UI/UX analysis from a single screenshot
    Runs: UI/UX + Summary (UI/UX only)
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: UI/UX Analysis (Single Screenshot)")
    print("="*70 + "\n")

    # Note: Replace with actual screenshot path
    screenshot_data = {
        "screenshot": "path/to/your/screenshot.png"
    }

    print("⚠️  Note: Replace 'path/to/your/screenshot.png' with actual screenshot path")
    # analyze(screenshot_data, stream=True)


def example_4_uiux_multiple_screenshots():
    """
    Example 4: UI/UX responsive design analysis from multiple screenshots
    Runs: UI/UX + Summary (UI/UX only)
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: UI/UX Responsive Analysis (Multiple Screenshots)")
    print("="*70 + "\n")

    # Note: Replace with actual screenshot paths
    screenshot_data = {
        "screenshots": {
            "desktop": "path/to/desktop.png",
            "tablet": "path/to/tablet.png",
            "mobile": "path/to/mobile.png"
        }
    }

    print("⚠️  Note: Replace screenshot paths with actual files")
    # analyze(screenshot_data, stream=True)


def example_5_url_with_custom_screenshots():
    """
    Example 5: Full analysis with custom screenshots
    Runs: SEO + Performance + UI/UX (with custom screenshots) + Summary
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Full Analysis with Custom Screenshots")
    print("="*70 + "\n")

    # Note: Replace with actual data
    analysis_data = {
        "url": "https://example.com",
        "screenshots": {
            "desktop": "path/to/custom_desktop.png",
            "mobile": "path/to/custom_mobile.png"
        }
    }

    print("⚠️  Note: Replace with actual URL and screenshot paths")
    # analyze(analysis_data, stream=True)


def example_6_programmatic_usage():
    """
    Example 6: Using the workflow programmatically (non-streaming)
    Get results as a string for further processing
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Programmatic Usage (Non-Streaming)")
    print("="*70 + "\n")

    url = "https://nightwatch.io"

    # Get results as string (no streaming)
    result = analyze(url, stream=False)

    print("Analysis complete!")
    print(f"Result length: {len(result)} characters")

    # You can now process the result string
    # For example, save to file:
    # with open("analysis_result.md", "w") as f:
    #     f.write(result)

    # Or parse for specific information
    # if "Overall Website Grade: A" in result:
    #     print("Excellent website!")


def main():
    """
    Main function - choose which example to run
    """
    print("\n" + "="*70)
    print("UNIFIED WORKFLOW - USAGE EXAMPLES")
    print("="*70)
    print("\nAvailable Examples:")
    print("  1. Comprehensive URL Analysis (SEO + Performance + UI/UX)")
    print("  2. SEO Only (HTML Input)")
    print("  3. UI/UX Only (Single Screenshot)")
    print("  4. UI/UX Responsive (Multiple Screenshots)")
    print("  5. Full Analysis with Custom Screenshots")
    print("  6. Programmatic Usage (Non-Streaming)")
    print("\nCurrently running: Example 1")
    print("="*70)

    # Validate API keys
    if not Config.validate_required_keys():
        print("[!] Please configure required API keys in config.py")
        exit(1)

    # Run example 1 by default
    example_1_comprehensive_url_analysis()

    # Uncomment to run other examples:
    # example_2_seo_only_html()
    # example_3_uiux_single_screenshot()
    # example_4_uiux_multiple_screenshots()
    # example_5_url_with_custom_screenshots()
    # example_6_programmatic_usage()


if __name__ == "__main__":
    main()
