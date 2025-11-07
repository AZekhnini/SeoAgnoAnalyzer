"""
Unified Website Analysis Workflow
Combines SEO and Performance analysis with conditional execution based on input type.
"""

from agno.workflow import Workflow, Step, StepInput, StepOutput, Condition
from agno.media import Image
from src.extractors.html_extractor import HtmlContentExtractor
from src.extractors.performance_extractor import analyze_performance
from src.extractors.uiux_extractor import UIUXExtractor
from src.agents.classifier_agent import input_classifier
from src.agents.seo_agent import seo_analyst
from src.agents.performance_agent import performance_analyst
from src.agents.uiux_agent import uiux_analyst
from src.agents.summary_agent import summary_analyst
from typing import Dict, Any, Union
import base64
import json


def extract_seo_features_step(step_input: StepInput) -> StepOutput:
    """
    Extract SEO features from URL or raw HTML (FREE operation).

    Args:
        step_input: StepInput containing either URL string or dict with url/html

    Returns:
        StepOutput with formatted SEO features
    """
    input_data = step_input.input

    # Parse input - can be string or dict
    if isinstance(input_data, dict):
        url = input_data.get("url")
        html = input_data.get("html")
    else:
        # String input - determine if URL or HTML
        if isinstance(input_data, str) and (input_data.startswith('http://') or input_data.startswith('https://')):
            url = input_data
            html = None
        else:
            url = None
            html = input_data

    # Determine source type for display
    if url:
        print(f"\n[SEO Feature Extraction] Analyzing URL: {url}")
        source_type = "URL"
        source_value = url
    else:
        print(f"\n[SEO Feature Extraction] Analyzing raw HTML content")
        source_type = "Raw HTML"
        source_value = "HTML Document"

    try:
        # Run HTML extractor
        if url:
            extractor = HtmlContentExtractor(url=url)
        else:
            extractor = HtmlContentExtractor(html=html)

        features = extractor.extract()

        # Format features for agent
        formatted_features = format_seo_features(features, source_type, source_value)

        print("[SEO Feature Extraction] Complete\n")
        return StepOutput(content=formatted_features)

    except Exception as e:
        error_message = f"[SEO] Error extracting features: {str(e)}"
        print(error_message)
        return StepOutput(content=error_message)


def extract_performance_features_step(step_input: StepInput) -> StepOutput:
    """
    Extract performance features from URL (FREE/Low-cost operation).

    This step should only run when a URL is provided (enforced by Condition).

    Args:
        step_input: StepInput containing URL string or dict with url

    Returns:
        StepOutput with formatted performance features
    """
    input_data = step_input.input

    # Parse input
    if isinstance(input_data, dict):
        url = input_data.get("url")
    else:
        url = input_data if isinstance(input_data, str) and (input_data.startswith('http://') or input_data.startswith('https://')) else None

    if not url:
        error_message = "[PERFORMANCE] Error: Performance analysis requires a valid URL"
        print(error_message)
        return StepOutput(content=error_message)

    print(f"\n[Performance Feature Extraction] Analyzing URL: {url}")
    print("[Performance Feature Extraction] This may take 10-30 seconds...")

    try:
        # Run comprehensive performance analysis
        features = analyze_performance(url, use_fallback=True)

        # Format features for agent
        formatted_features = format_performance_features(features, url)

        print("[Performance Feature Extraction] Complete\n")
        return StepOutput(content=formatted_features)

    except Exception as e:
        error_message = f"[PERFORMANCE] Error extracting features: {str(e)}"
        print(error_message)
        return StepOutput(content=error_message)


def extract_uiux_features_step(step_input: StepInput) -> StepOutput:
    """
    Extract UI/UX features from URL or screenshot(s).

    Args:
        step_input: StepInput containing URL, screenshot path, or screenshots dict

    Returns:
        StepOutput with formatted UI/UX features including screenshots and accessibility data
    """
    input_data = step_input.input

    # Parse input to determine mode
    url = None
    screenshot = None
    screenshots = None

    if isinstance(input_data, dict):
        url = input_data.get("url")
        screenshot = input_data.get("screenshot")
        screenshots = input_data.get("screenshots")
    elif isinstance(input_data, str) and (input_data.startswith('http://') or input_data.startswith('https://')):
        url = input_data

    # Determine extraction mode
    if url:
        print(f"\n[UI/UX Feature Extraction] Analyzing URL: {url}")
        print("[UI/UX Feature Extraction] Capturing screenshots and running accessibility audit...")
    elif screenshots:
        print(f"\n[UI/UX Feature Extraction] Analyzing provided screenshots: {list(screenshots.keys())}")
    elif screenshot:
        print(f"\n[UI/UX Feature Extraction] Analyzing provided screenshot: {screenshot}")
    else:
        error_message = "[UI/UX] Error: No valid input for UI/UX analysis"
        print(error_message)
        return StepOutput(content=error_message)

    try:
        # Run UI/UX extractor
        extractor = UIUXExtractor(url=url, screenshot=screenshot, screenshots=screenshots)
        features = extractor.extract()

        print("[UI/UX Feature Extraction] Complete\n")

        # Return features as JSON string (will be parsed in analysis step)
        return StepOutput(content=json.dumps(features))

    except Exception as e:
        error_message = f"[UI/UX] Error extracting features: {str(e)}"
        print(error_message)
        return StepOutput(content=error_message)


def analyze_uiux_with_vision_step(step_input: StepInput) -> StepOutput:
    """
    Analyze UI/UX features with vision model by passing screenshots as images.

    Args:
        step_input: StepInput containing JSON-encoded features from extraction step

    Returns:
        StepOutput with UI/UX analysis from vision agent
    """
    try:
        # Get the content from the previous step (UI/UX Feature Extraction)
        previous_content = step_input.previous_step_content

        # Debug: check what we received
        if not previous_content or previous_content == "":
            raise ValueError("No content received from UI/UX Feature Extraction step")

        # Parse JSON string from previous step
        features = json.loads(previous_content)

        # Prepare text context for the agent
        mode = features.get('mode', 'unknown')
        metadata = features.get('metadata', {})
        accessibility = features.get('accessibility')

        # Build context text
        context = f"""
=== UI/UX ANALYSIS REQUEST ===

Analysis Mode: {mode.upper()}
Source: {metadata.get('source', 'N/A')}
"""

        if mode == 'url':
            context += f"Viewports Captured: {', '.join(metadata.get('viewports_captured', []))}\n"
        elif mode == 'screenshots':
            context += f"Viewports Provided: {', '.join(metadata.get('viewports', []))}\n"
        elif mode == 'screenshot':
            context += f"Viewport: {metadata.get('viewport', 'default')}\n"

        # Add accessibility data if available
        if accessibility:
            score = accessibility.get('score', 'N/A')
            summary = accessibility.get('summary', {})
            issues = accessibility.get('issues', [])

            context += f"""
=== ACCESSIBILITY AUDIT RESULTS ===

Overall Accessibility Score: {score}/100

Issue Summary:
  Critical Issues: {summary.get('critical', 0)}
  Serious Issues: {summary.get('serious', 0)}
  Moderate Issues: {summary.get('moderate', 0)}
  Total Issues: {summary.get('total', 0)}

"""
            if issues:
                context += "Detailed Issues:\n"
                for issue in issues:
                    context += f"  [{issue.get('severity', 'unknown').upper()}] {issue.get('description', 'No description')}\n"
                context += "\n"

        context += """
Please analyze the provided screenshots and accessibility data to provide a comprehensive UI/UX evaluation.
Focus on visual design, user experience, accessibility compliance, and responsive design quality.
"""

        # Convert base64 screenshots to Image objects
        screenshots = features.get('screenshots', {})
        image_objects = []

        for viewport_name, screenshot_base64 in screenshots.items():
            # Decode base64 to bytes
            image_bytes = base64.b64decode(screenshot_base64)
            # Create Image object
            image_objects.append(Image(content=image_bytes, format="png"))

        print(f"\n[UI/UX Analysis with Vision] Analyzing {len(image_objects)} screenshots with vision model...\n")

        # Call agent with images and display the response
        uiux_analyst.print_response(
            input=context,
            images=image_objects,
            markdown=True,
            stream=True
        )

        print("\n[UI/UX Analysis with Vision] Complete\n")
        return StepOutput(content="UI/UX analysis completed (displayed above)")

    except Exception as e:
        error_message = f"[UI/UX] Error during vision analysis: {str(e)}"
        print(error_message)
        import traceback
        traceback.print_exc()
        return StepOutput(content=error_message)


def classify_input_step(step_input: StepInput) -> StepOutput:
    """
    First step: Classify the input using AI to determine if it's URL, HTML, or Screenshot.

    Args:
        step_input: StepInput containing raw user input

    Returns:
        StepOutput with classification results in JSON format
    """
    try:
        # Get the raw input
        user_input = step_input.input

        # Convert to string if needed
        if isinstance(user_input, dict):
            input_str = json.dumps(user_input)
        else:
            input_str = str(user_input)

        print(f"\n[Input Classification] Analyzing input type...")

        # Call the classifier agent
        response = input_classifier.run(
            input=f"Classify this input:\n\n{input_str}",
            stream=False
        )

        # The agent returns JSON classification
        classification = response.content

        print(f"[Input Classification] Complete\n")

        # Return the classification result
        return StepOutput(content=classification)

    except Exception as e:
        error_message = f"[Classifier] Error during classification: {str(e)}"
        print(error_message)
        import traceback
        traceback.print_exc()

        # Return a default classification
        default = json.dumps({
            "type": "unknown",
            "confidence": "low",
            "reasoning": f"Classification failed: {str(e)}",
            "normalized_input": str(step_input.input)
        })
        return StepOutput(content=default)


def _check_is_url(input_data: Any) -> bool:
    """
    Helper function to check if input contains a URL.

    Args:
        input_data: Raw input data (string or dict)

    Returns:
        True if input contains a valid URL, False otherwise
    """
    if isinstance(input_data, dict):
        url = input_data.get("url")
        return url is not None and isinstance(url, str) and (url.startswith('http://') or url.startswith('https://'))
    elif isinstance(input_data, str):
        return input_data.startswith('http://') or input_data.startswith('https://')
    return False


def is_url_input(step_input: StepInput, session_state: Any = None) -> bool:
    """
    Condition evaluator for Agno workflow to check if input contains a URL.

    Used to determine if performance analysis should run.

    Args:
        step_input: StepInput object from Agno workflow
        session_state: Session state (not used)

    Returns:
        True if input contains a valid URL, False otherwise
    """
    return _check_is_url(step_input.input)


def _check_has_url_or_html(input_data: Any) -> bool:
    """
    Helper function to check if input contains URL or HTML.

    Args:
        input_data: Raw input data (string or dict)

    Returns:
        True if input contains URL or HTML, False otherwise
    """
    if isinstance(input_data, dict):
        return "url" in input_data or "html" in input_data
    elif isinstance(input_data, str):
        return True  # String is either URL or HTML
    return False


def has_url_or_html(step_input: StepInput, session_state: Any = None) -> bool:
    """
    Condition evaluator to check if input has URL or HTML (for SEO analysis).

    Args:
        step_input: StepInput object from Agno workflow
        session_state: Session state (not used)

    Returns:
        True if input contains URL or HTML, False otherwise
    """
    return _check_has_url_or_html(step_input.input)


def _check_has_screenshot(input_data: Any) -> bool:
    """
    Helper function to check if input contains screenshot(s).

    Args:
        input_data: Raw input data (string or dict)

    Returns:
        True if input contains screenshot or screenshots, False otherwise
    """
    if isinstance(input_data, dict):
        return "screenshot" in input_data or "screenshots" in input_data
    return False


def has_screenshot(step_input: StepInput, session_state: Any = None) -> bool:
    """
    Condition evaluator to check if input has screenshot(s).

    Args:
        step_input: StepInput object from Agno workflow
        session_state: Session state (not used)

    Returns:
        True if input contains screenshot(s), False otherwise
    """
    return _check_has_screenshot(step_input.input)


def needs_uiux_analysis(step_input: StepInput, session_state: Any = None) -> bool:
    """
    Condition evaluator to check if UI/UX analysis should run.

    UI/UX analysis runs when:
    - URL is provided (captures screenshots automatically), OR
    - Screenshot(s) are provided

    Args:
        step_input: StepInput object from Agno workflow
        session_state: Session state (not used)

    Returns:
        True if UI/UX analysis should run, False otherwise
    """
    return _check_is_url(step_input.input) or _check_has_screenshot(step_input.input)


def format_seo_features(features: Dict[str, Any], source_type: str, source_value: str) -> str:
    """Format SEO features into structured string for agent analysis"""

    def format_list(items, max_items=5):
        if not items:
            return 'None'
        if len(items) <= max_items:
            return ', '.join(str(item) for item in items)
        return ', '.join(str(item) for item in items[:max_items]) + f' (+ {len(items) - max_items} more)'

    h1_display = format_list(features.get('h1_texts', []), max_items=3)
    h2_display = format_list(features.get('h2_texts', []), max_items=5)
    json_ld_display = format_list(features.get('json_ld_types', []))

    top_keywords = features.get('top_keywords', [])
    if top_keywords:
        keyword_display = ', '.join([
            f"{kw['keyword']}({kw['density']}%)" for kw in top_keywords[:5]
        ])
    else:
        keyword_display = 'None analyzed'

    page_text = features.get('text', '')
    preview_text = page_text[:500] if page_text else 'No text content found'

    formatted = f"""SEO FEATURES EXTRACTED FROM {source_type}: {source_value}

=== URL STRUCTURE ===
URL Length: {features.get('url_length', 0)} characters
URL Readability: {features.get('url_readability', 'N/A')}
URL Depth: {features.get('url_depth', 0)} levels
Uses HTTPS: {features.get('url_uses_https', False)}
Contains Keywords: {features.get('url_has_keywords', False)}

=== META TAGS ===
Title: {features.get('title', 'N/A')} ({features.get('title_length', 0)} chars)
Meta Description: {features.get('meta_description', 'N/A')} ({features.get('meta_description_length', 0)} chars)
Meta Robots: {features.get('meta_robots', 'N/A')}
Canonical URL: {features.get('canonical_url', 'N/A')}

=== HEADING STRUCTURE ===
H1 Count: {features.get('h1_count', 0)}
H1 Texts: {h1_display}
H2 Count: {features.get('h2_count', 0)}
H2 Texts: {h2_display}
H3 Count: {features.get('h3_count', 0)}
H4 Count: {features.get('h4_count', 0)}
H5 Count: {features.get('h5_count', 0)}
H6 Count: {features.get('h6_count', 0)}

=== CONTENT METRICS ===
Word Count: {features.get('word_count', 0)}
Paragraph Count: {features.get('paragraph_count', 0)}
Average Paragraph Length: {features.get('average_paragraph_length', 0)} words
Text-to-HTML Ratio: {features.get('text_html_ratio', 0)}%
Readability Score: {features.get('readability_score', 'N/A')}
Content Depth Score: {features.get('content_depth_score', 0)}/100

=== CONTENT STRUCTURE ===
Has Lists: {features.get('has_lists', False)} (Count: {features.get('list_count', 0)})
Has Tables: {features.get('has_tables', False)} (Count: {features.get('table_count', 0)})

=== KEYWORD ANALYSIS ===
Top Keywords: {keyword_display}
Title Keyword Match: {features.get('title_keyword_match', False)}
H1 Keyword Match: {features.get('h1_keyword_match', False)}

=== LINKS ===
Internal Links: {features.get('internal_links', 0)}
External Links: {features.get('external_links', 0)}
Total Links: {features.get('total_links', 0)}

=== IMAGES ===
Total Images: {features.get('total_images', 0)}
Images with Alt Text: {features.get('images_with_alt', 0)}
Images without Alt Text: {features.get('images_without_alt', 0)}

=== STRUCTURED DATA ===
Has JSON-LD: {features.get('has_json_ld', False)}
JSON-LD Types: {json_ld_display}
Has FAQ Schema: {features.get('has_faq_schema', False)}
Has Breadcrumb Schema: {features.get('has_breadcrumb_schema', False)}
Has Local Business Schema: {features.get('has_local_business_schema', False)}

=== SOCIAL MEDIA TAGS ===
OG Title: {features.get('og_title', 'N/A')}
OG Description: {features.get('og_description', 'N/A')}
OG Image: {features.get('og_image', 'N/A')}
Twitter Card: {features.get('twitter_card', 'N/A')}
Twitter Title: {features.get('twitter_title', 'N/A')}

=== INTERNATIONAL SEO ===
Language: {features.get('language', 'N/A')}
Has Hreflang: {features.get('has_hreflang', False)}

=== NAVIGATION & UX ===
Has Breadcrumbs: {features.get('has_breadcrumbs', False)}
Has Search Functionality: {features.get('has_search', False)}
Has Contact Info: {features.get('has_contact_info', False)}

=== CONTENT FRESHNESS ===
Has Date Modified: {features.get('has_date_modified', False)}
Last Modified: {features.get('last_modified', 'N/A')}

=== MOBILE & TECHNICAL ===
Has Viewport Meta: {features.get('has_viewport', False)}
Page Size: {features.get('page_size_kb', 0)} KB

=== PAGE CONTENT PREVIEW (First 500 chars) ===
{preview_text}...
"""
    return formatted


def format_performance_features(features: Dict[str, Any], url: str) -> str:
    """Format performance features into structured string for agent analysis"""

    def format_score(score):
        if score is None:
            return "N/A"
        return f"{int(score)}/100"

    def format_ms(value):
        if value is None:
            return "N/A"
        return f"{int(value)}ms"

    def format_bytes(value):
        if value is None:
            return "N/A"
        if value < 1024:
            return f"{value} bytes"
        elif value < 1024 * 1024:
            return f"{value / 1024:.2f} KB"
        else:
            return f"{value / (1024 * 1024):.2f} MB"

    def categorize_lcp(value):
        if value is None:
            return "N/A"
        if value < 2500:
            return "Good (< 2.5s)"
        elif value < 4000:
            return "Needs Improvement (2.5-4s)"
        else:
            return "Poor (> 4s)"

    def categorize_fid(value):
        if value is None:
            return "N/A"
        if value < 100:
            return "Good (< 100ms)"
        elif value < 300:
            return "Needs Improvement (100-300ms)"
        else:
            return "Poor (> 300ms)"

    def categorize_cls(value):
        if value is None:
            return "N/A"
        if value < 0.1:
            return "Good (< 0.1)"
        elif value < 0.25:
            return "Needs Improvement (0.1-0.25)"
        else:
            return "Poor (> 0.25)"

    opportunities_display = "None analyzed"
    if features.get('opportunities'):
        opps = features['opportunities'][:5]
        opportunities_display = "\n".join([
            f"  • {opp.get('title', 'Unknown')}: {format_ms(opp.get('savings_ms'))}"
            for opp in opps
        ])

    rb_resources = features.get('render_blocking_resources', [])
    rb_display = "None" if not rb_resources else "\n".join([f"  • {res}" for res in rb_resources[:5]])
    if len(rb_resources) > 5:
        rb_display += f"\n  • ... and {len(rb_resources) - 5} more"

    formatted = f"""TECHNICAL PERFORMANCE FEATURES EXTRACTED FROM URL: {url}

=== ANALYSIS SOURCE ===
Primary Source: {features.get('analysis_source', 'unknown')}
Analyzed At: {features.get('analyzed_at', 'N/A')}
Fallback Used: {features.get('fallback_used', False)}
API Error: {features.get('api_error', 'None')}

=== OVERALL SCORES ===
Performance Score: {format_score(features.get('performance_score'))}
Accessibility Score: {format_score(features.get('accessibility_score'))}
Best Practices Score: {format_score(features.get('best_practices_score'))}
SEO Score: {format_score(features.get('seo_score'))}

=== CORE WEB VITALS ===
Largest Contentful Paint (LCP): {format_ms(features.get('lcp_value'))} - {categorize_lcp(features.get('lcp_value'))}
  Score: {format_score(features.get('lcp_score'))}

First Input Delay (FID/TBT): {format_ms(features.get('fid_value'))} - {categorize_fid(features.get('fid_value'))}
  Score: {format_score(features.get('fid_score'))}

Cumulative Layout Shift (CLS): {features.get('cls_value', 'N/A')} - {categorize_cls(features.get('cls_value'))}
  Score: {format_score(features.get('cls_score'))}

=== LOADING PERFORMANCE ===
First Contentful Paint (FCP): {format_ms(features.get('fcp_value'))}
  Score: {format_score(features.get('fcp_score'))}

Time to Interactive (TTI): {format_ms(features.get('tti_value'))}
  Score: {format_score(features.get('tti_score'))}

Speed Index: {format_ms(features.get('speed_index_value'))}
  Score: {format_score(features.get('speed_index_score'))}

Total Blocking Time (TBT): {format_ms(features.get('tbt_value'))}
  Score: {format_score(features.get('tbt_score'))}

=== RESOURCE ANALYSIS ===
Total Page Size: {format_bytes(features.get('total_page_size'))}
Total Requests: {features.get('total_requests', 'N/A')}

Resource Breakdown:
  HTML: {format_bytes(features.get('html_size'))} ({features.get('html_requests', 0)} requests)
  CSS: {format_bytes(features.get('css_size'))} ({features.get('css_requests', 0)} requests)
  JavaScript: {format_bytes(features.get('js_size'))} ({features.get('js_requests', 0)} requests)
  Images: {format_bytes(features.get('image_size'))} ({features.get('image_requests', 0)} requests)
  Fonts: {format_bytes(features.get('font_size'))} ({features.get('font_requests', 0)} requests)
  Other: {format_bytes(features.get('other_size'))} ({features.get('other_requests', 0)} requests)

=== RENDER-BLOCKING RESOURCES ===
Render-Blocking CSS: {features.get('render_blocking_css_count', 0)} files
Render-Blocking JavaScript: {features.get('render_blocking_js_count', 0)} files
Resources:
{rb_display}

=== JAVASCRIPT ANALYSIS ===
Unused JavaScript: {format_bytes(features.get('unused_js_bytes'))}
Total JS Execution Time: {format_ms(features.get('total_js_execution_time'))}
Main Thread Work Time: {format_ms(features.get('main_thread_work_time'))}

=== CSS ANALYSIS ===
Unused CSS: {format_bytes(features.get('unused_css_bytes'))}

=== CACHING & COMPRESSION ===
Compression:
  Gzip: {features.get('uses_gzip_compression', False)}
  Brotli: {features.get('uses_brotli_compression', False)}

Caching:
  Cache-Control: {features.get('has_cache_control', False)}
  Cache-Control Value: {features.get('cache_control_value', 'N/A')}
  ETag: {features.get('has_etag', False)}
  Expires: {features.get('has_expires', False)}
  Expires Value: {features.get('expires_value', 'N/A')}

=== SECURITY HEADERS ===
HSTS (Strict-Transport-Security): {features.get('has_hsts', False)}
  Value: {features.get('hsts_value', 'N/A')}

Content-Security-Policy (CSP): {features.get('has_csp', False)}
  Value: {features.get('csp_value', 'N/A')}

X-Frame-Options: {features.get('has_x_frame_options', False)}
  Value: {features.get('x_frame_options_value', 'N/A')}

X-Content-Type-Options: {features.get('has_x_content_type_options', False)}

Referrer-Policy: {features.get('has_referrer_policy', False)}
  Value: {features.get('referrer_policy_value', 'N/A')}

=== SERVER & RESPONSE ===
Server Type: {features.get('server_type', 'N/A')}
Response Time: {format_ms(features.get('response_time'))}
HTTP Status Code: {features.get('http_status_code', 'N/A')}
Redirects Count: {features.get('redirects_count', 0)}
Uses HTTP/2: {features.get('uses_http2', False)}
Uses HTTP/3: {features.get('uses_http3', False)}

=== THIRD-PARTY ANALYSIS ===
Third-Party Requests: {features.get('third_party_requests', 0)}
Third-Party Size: {format_bytes(features.get('third_party_size'))}
Third-Party Blocking Time: {format_ms(features.get('third_party_blocking_time'))}

=== FONT OPTIMIZATION ===
Font Display Set: {features.get('font_display_set', False)}

=== TOP OPTIMIZATION OPPORTUNITIES ===
{opportunities_display}

=== DIAGNOSTICS COUNT ===
Total Diagnostics: {len(features.get('diagnostics', []))}
"""
    return formatted


def format_uiux_features(features: Dict[str, Any]) -> str:
    """
    Format UI/UX features for agent analysis.

    Returns a formatted string with metadata, accessibility results,
    and screenshot information for the vision-enabled agent.
    """
    # Add metadata text
    mode = features.get('mode', 'unknown')
    metadata = features.get('metadata', {})

    formatted = f"""
=== UI/UX ANALYSIS REQUEST ===

Analysis Mode: {mode.upper()}
Source: {metadata.get('source', 'N/A')}
"""

    if mode == 'url':
        formatted += f"Viewports Captured: {', '.join(metadata.get('viewports_captured', []))}\n"
    elif mode == 'screenshots':
        formatted += f"Viewports Provided: {', '.join(metadata.get('viewports', []))}\n"
    elif mode == 'screenshot':
        formatted += f"Viewport: {metadata.get('viewport', 'default')}\n"

    # Add accessibility data if available
    accessibility = features.get('accessibility')
    if accessibility:
        score = accessibility.get('score', 'N/A')
        summary = accessibility.get('summary', {})
        issues = accessibility.get('issues', [])

        formatted += f"""
=== ACCESSIBILITY AUDIT RESULTS ===

Overall Accessibility Score: {score}/100

Issue Summary:
  Critical Issues: {summary.get('critical', 0)}
  Serious Issues: {summary.get('serious', 0)}
  Moderate Issues: {summary.get('moderate', 0)}
  Total Issues: {summary.get('total', 0)}

"""

        if issues:
            formatted += "Detailed Issues:\n"
            for issue in issues:
                formatted += f"  [{issue.get('severity', 'unknown').upper()}] {issue.get('description', 'No description')}\n"
            formatted += "\n"

    # Add screenshots info
    screenshots = features.get('screenshots', {})

    formatted += f"""
=== SCREENSHOTS AVAILABLE ===

Number of Viewports: {len(screenshots)}
Viewports: {', '.join(screenshots.keys())}

Note: Screenshots have been captured and will be analyzed visually.
Each screenshot is approximately {len(list(screenshots.values())[0]) if screenshots else 0} bytes (base64 encoded).

"""

    # Add note about limitations
    formatted += """
=== ANALYSIS INSTRUCTIONS ===

Please provide a comprehensive UI/UX evaluation based on the screenshots and accessibility data.
Analyze visual design, user experience, accessibility compliance, and responsive design quality.
Provide specific, actionable recommendations prioritized by impact.

"""

    return formatted


# Create the Unified Workflow with Conditional Execution
unified_workflow = Workflow(
    name="Unified Website Analysis Workflow",
    description="Comprehensive SEO, Performance, and UI/UX analysis with conditional execution based on input type",
    steps=[
        # Input Classification - ALWAYS RUNS FIRST: Detects input type using AI
        Step(
            name="Input Classification",
            executor=classify_input_step,
        ),

        # SEO Analysis - CONDITIONAL: Only if URL or HTML provided
        Condition(
            name="SEO Analysis Condition",
            description="Run SEO analysis if URL or HTML provided",
            evaluator=has_url_or_html,
            steps=[
                Step(
                    name="SEO Feature Extraction",
                    executor=extract_seo_features_step,
                ),
                Step(
                    name="SEO Analysis",
                    agent=seo_analyst,
                ),
            ],
        ),

        # Performance Analysis - CONDITIONAL: Only if URL provided
        Condition(
            name="Performance Analysis Condition",
            description="Run performance analysis if URL is provided",
            evaluator=is_url_input,
            steps=[
                Step(
                    name="Performance Feature Extraction",
                    executor=extract_performance_features_step,
                ),
                Step(
                    name="Performance Analysis",
                    agent=performance_analyst,
                ),
            ],
        ),

        # UI/UX Analysis - CONDITIONAL: Only if URL or Screenshot(s) provided
        Condition(
            name="UI/UX Analysis Condition",
            description="Run UI/UX analysis if URL or screenshot(s) are provided",
            evaluator=needs_uiux_analysis,
            steps=[
                Step(
                    name="UI/UX Feature Extraction",
                    executor=extract_uiux_features_step,
                ),
                Step(
                    name="UI/UX Analysis with Vision",
                    executor=analyze_uiux_with_vision_step,
                ),
            ],
        ),

        # Final Summary - ALWAYS RUNS: Synthesizes all analysis results
        Step(
            name="Executive Summary & Recommendations",
            agent=summary_analyst,
        ),
    ],
)


def analyze(input_data: Union[str, Dict[str, str]], stream: bool = False) -> str:
    """
    Unified analysis function for SEO, Performance, and UI/UX.

    Automatically determines what analysis to run based on input:
    - URL string: Runs SEO + Performance + UI/UX (comprehensive)
    - HTML string: Runs SEO only
    - Dict with 'url': Runs SEO + Performance + UI/UX
    - Dict with 'html': Runs SEO only
    - Dict with 'screenshot': Runs UI/UX only
    - Dict with 'screenshots': Runs UI/UX only

    Args:
        input_data: URL string, HTML string, or dict with keys:
                   - 'url': Website URL
                   - 'html': Raw HTML content
                   - 'screenshot': Path to single screenshot file
                   - 'screenshots': Dict of {viewport_name: screenshot_path}
        stream: Whether to stream the output (default: False)

    Returns:
        String containing the analysis results

    Examples:
        >>> # Analyze URL (SEO + Performance + UI/UX)
        >>> analyze("https://example.com", stream=True)

        >>> # Analyze HTML (SEO only)
        >>> html = "<html><head><title>Test</title></head></html>"
        >>> analyze(html, stream=True)

        >>> # Analyze single screenshot (UI/UX only)
        >>> analyze({"screenshot": "screenshot.png"}, stream=True)

        >>> # Analyze multiple screenshots (UI/UX only)
        >>> analyze({
        ...     "screenshots": {
        ...         "desktop": "desktop.png",
        ...         "mobile": "mobile.png"
        ...     }
        ... }, stream=True)

        >>> # Analyze URL with custom screenshots
        >>> analyze({
        ...     "url": "https://example.com",
        ...     "screenshots": {"desktop": "custom.png"}
        ... }, stream=True)
    """

    # Determine what will be analyzed
    is_url = _check_is_url(input_data)
    is_html = _check_has_url_or_html(input_data) and not is_url
    has_screenshot = _check_has_screenshot(input_data)

    print(f"\n{'='*70}")
    print("UNIFIED WEBSITE ANALYSIS")
    print(f"{'='*70}")

    # Display analysis mode
    if is_url:
        print("Analysis Mode: SEO + Performance + UI/UX (URL detected)")
    elif is_html:
        print("Analysis Mode: SEO Only (HTML input detected)")
    elif has_screenshot:
        print("Analysis Mode: UI/UX Only (Screenshot provided)")
    else:
        print("Analysis Mode: Unknown input type")

    print(f"{'='*70}\n")

    if stream:
        unified_workflow.print_response(input=input_data, markdown=True, stream=True)
        return "Analysis streamed above"
    else:
        result = unified_workflow.run(input=input_data)
        return result.content
