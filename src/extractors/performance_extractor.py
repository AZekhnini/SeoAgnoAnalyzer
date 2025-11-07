"""
Technical Performance Analysis Extractor
Extracts performance metrics using multiple free/cost-effective sources.
"""

import json
import requests
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
from config import Config


@dataclass
class TechnicalPerformanceFeatures:
    """Dataclass to store all technical performance metrics"""

    # Source information
    url: str = ""
    analyzed_at: str = ""

    # ==== CORE WEB VITALS (from PageSpeed Insights) ====
    # Largest Contentful Paint (LCP) - Loading performance
    lcp_score: Optional[float] = None  # 0-100
    lcp_value: Optional[float] = None  # milliseconds
    lcp_category: Optional[str] = None  # "FAST", "AVERAGE", "SLOW"

    # First Input Delay (FID) - Interactivity
    fid_score: Optional[float] = None
    fid_value: Optional[float] = None
    fid_category: Optional[str] = None

    # Cumulative Layout Shift (CLS) - Visual stability
    cls_score: Optional[float] = None
    cls_value: Optional[float] = None
    cls_category: Optional[str] = None

    # First Contentful Paint (FCP)
    fcp_score: Optional[float] = None
    fcp_value: Optional[float] = None
    fcp_category: Optional[str] = None

    # Time to Interactive (TTI)
    tti_score: Optional[float] = None
    tti_value: Optional[float] = None
    tti_category: Optional[str] = None

    # Speed Index
    speed_index_score: Optional[float] = None
    speed_index_value: Optional[float] = None
    speed_index_category: Optional[str] = None

    # Total Blocking Time (TBT)
    tbt_score: Optional[float] = None
    tbt_value: Optional[float] = None
    tbt_category: Optional[str] = None

    # ==== OVERALL SCORES ====
    performance_score: Optional[int] = None  # 0-100
    accessibility_score: Optional[int] = None
    best_practices_score: Optional[int] = None
    seo_score: Optional[int] = None

    # ==== RESOURCE ANALYSIS ====
    total_page_size: Optional[int] = None  # bytes
    total_requests: Optional[int] = None

    # Resource breakdown
    html_size: Optional[int] = None
    css_size: Optional[int] = None
    js_size: Optional[int] = None
    image_size: Optional[int] = None
    font_size: Optional[int] = None
    other_size: Optional[int] = None

    html_requests: int = 0
    css_requests: int = 0
    js_requests: int = 0
    image_requests: int = 0
    font_requests: int = 0
    other_requests: int = 0

    # ==== CACHING & COMPRESSION ====
    uses_gzip_compression: bool = False
    uses_brotli_compression: bool = False
    has_cache_control: bool = False
    cache_control_value: Optional[str] = None
    has_etag: bool = False
    has_expires: bool = False
    expires_value: Optional[str] = None

    # ==== SECURITY HEADERS ====
    has_hsts: bool = False  # HTTP Strict Transport Security
    hsts_value: Optional[str] = None
    has_csp: bool = False  # Content Security Policy
    csp_value: Optional[str] = None
    has_x_frame_options: bool = False
    x_frame_options_value: Optional[str] = None
    has_x_content_type_options: bool = False
    has_referrer_policy: bool = False
    referrer_policy_value: Optional[str] = None

    # ==== SERVER & RESPONSE ====
    server_type: Optional[str] = None
    response_time: Optional[float] = None  # milliseconds
    http_status_code: Optional[int] = None
    redirects_count: int = 0
    uses_http2: bool = False
    uses_http3: bool = False

    # ==== RENDER BLOCKING RESOURCES ====
    render_blocking_css_count: int = 0
    render_blocking_js_count: int = 0
    render_blocking_resources: List[str] = field(default_factory=list)

    # ==== IMAGE OPTIMIZATION ====
    unoptimized_images_count: int = 0
    images_without_dimensions: int = 0
    next_gen_images_opportunity: bool = False  # WebP, AVIF

    # ==== JAVASCRIPT ANALYSIS ====
    unused_js_bytes: Optional[int] = None
    total_js_execution_time: Optional[float] = None  # milliseconds
    main_thread_work_time: Optional[float] = None

    # ==== CSS ANALYSIS ====
    unused_css_bytes: Optional[int] = None

    # ==== FONT OPTIMIZATION ====
    font_display_set: bool = False
    preconnect_to_required_origins: List[str] = field(default_factory=list)

    # ==== THIRD-PARTY ANALYSIS ====
    third_party_requests: int = 0
    third_party_size: Optional[int] = None
    third_party_blocking_time: Optional[float] = None

    # ==== OPPORTUNITIES (PageSpeed Insights suggestions) ====
    opportunities: List[Dict[str, Any]] = field(default_factory=list)

    # ==== DIAGNOSTICS ====
    diagnostics: List[Dict[str, Any]] = field(default_factory=list)

    # ==== METADATA ====
    analysis_source: str = "unknown"  # "pagespeed", "local", "headers"
    api_error: Optional[str] = None
    fallback_used: bool = False


class PerformanceAnalyzer:
    """
    Analyzes website performance using Google PageSpeed Insights API.
    """

    def __init__(self, url: str, api_key: Optional[str] = None):
        """
        Initialize the Performance Analyzer.

        Args:
            url: URL to analyze
            api_key: Optional PageSpeed Insights API key (increases rate limits)
        """
        self.url = url
        self.api_key = api_key or Config.PAGESPEED_API_KEY
        self.features = TechnicalPerformanceFeatures(url=url)

        # PageSpeed Insights API endpoint
        self.api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def extract(self) -> Dict[str, Any]:
        """
        Extract performance metrics from PageSpeed Insights API.

        Returns:
            Dictionary of performance features
        """
        print(f"[*] Analyzing performance using PageSpeed Insights API...")

        try:
            # Build API request parameters
            params = {
                "url": self.url,
                "category": ["PERFORMANCE", "ACCESSIBILITY", "BEST_PRACTICES", "SEO"],
                "strategy": "MOBILE",  # Can also be "DESKTOP"
            }

            if self.api_key:
                params["key"] = self.api_key

            # Make API request (increased timeout for slower sites)
            response = requests.get(self.api_url, params=params, timeout=90)
            response.raise_for_status()

            data = response.json()

            # Extract metrics
            self._extract_lighthouse_metrics(data)
            self._extract_core_web_vitals(data)
            self._extract_opportunities(data)
            self._extract_diagnostics(data)

            self.features.analysis_source = "pagespeed"
            self.features.analyzed_at = time.strftime("%Y-%m-%d %H:%M:%S")

            print("[+] PageSpeed Insights analysis complete")

        except requests.exceptions.RequestException as e:
            error_msg = f"PageSpeed API request failed: {str(e)}"
            print(f"[!] {error_msg}")
            self.features.api_error = error_msg
            self.features.fallback_used = True

        except Exception as e:
            error_msg = f"Unexpected error during PageSpeed analysis: {str(e)}"
            print(f"[!] {error_msg}")
            self.features.api_error = error_msg

        return self._to_dict()

    def _extract_lighthouse_metrics(self, data: Dict) -> None:
        """Extract Lighthouse performance scores"""
        try:
            lighthouse = data.get("lighthouseResult", {})
            categories = lighthouse.get("categories", {})

            # Overall category scores (0-1 scale, convert to 0-100)
            perf = categories.get("performance", {})
            self.features.performance_score = int(perf.get("score", 0) * 100) if perf.get("score") else None

            access = categories.get("accessibility", {})
            self.features.accessibility_score = int(access.get("score", 0) * 100) if access.get("score") else None

            bp = categories.get("best-practices", {})
            self.features.best_practices_score = int(bp.get("score", 0) * 100) if bp.get("score") else None

            seo = categories.get("seo", {})
            self.features.seo_score = int(seo.get("score", 0) * 100) if seo.get("score") else None

        except Exception as e:
            print(f"[!] Error extracting Lighthouse metrics: {str(e)}")

    def _extract_core_web_vitals(self, data: Dict) -> None:
        """Extract Core Web Vitals and other performance metrics"""
        try:
            lighthouse = data.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})

            # Helper function to extract metric
            def extract_metric(audit_key: str):
                audit = audits.get(audit_key, {})
                return {
                    "score": audit.get("score"),  # 0-1
                    "value": audit.get("numericValue"),  # milliseconds
                    "display_value": audit.get("displayValue"),
                }

            # Largest Contentful Paint (LCP)
            lcp = extract_metric("largest-contentful-paint")
            self.features.lcp_score = lcp["score"] * 100 if lcp["score"] is not None else None
            self.features.lcp_value = lcp["value"]

            # First Input Delay (FID) - often estimated as TBT
            # Note: FID requires real user data, so we use TBT as proxy

            # Cumulative Layout Shift (CLS)
            cls = extract_metric("cumulative-layout-shift")
            self.features.cls_score = cls["score"] * 100 if cls["score"] is not None else None
            self.features.cls_value = cls["value"]

            # First Contentful Paint (FCP)
            fcp = extract_metric("first-contentful-paint")
            self.features.fcp_score = fcp["score"] * 100 if fcp["score"] is not None else None
            self.features.fcp_value = fcp["value"]

            # Time to Interactive (TTI)
            tti = extract_metric("interactive")
            self.features.tti_score = tti["score"] * 100 if tti["score"] is not None else None
            self.features.tti_value = tti["value"]

            # Speed Index
            si = extract_metric("speed-index")
            self.features.speed_index_score = si["score"] * 100 if si["score"] is not None else None
            self.features.speed_index_value = si["value"]

            # Total Blocking Time (TBT) - proxy for FID
            tbt = extract_metric("total-blocking-time")
            self.features.tbt_score = tbt["score"] * 100 if tbt["score"] is not None else None
            self.features.tbt_value = tbt["value"]
            # Use TBT as FID proxy
            self.features.fid_score = self.features.tbt_score
            self.features.fid_value = self.features.tbt_value

        except Exception as e:
            print(f"[!] Error extracting Core Web Vitals: {str(e)}")

    def _extract_opportunities(self, data: Dict) -> None:
        """Extract optimization opportunities from PageSpeed Insights"""
        try:
            lighthouse = data.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})

            opportunity_keys = [
                "render-blocking-resources",
                "unused-css-rules",
                "unused-javascript",
                "modern-image-formats",
                "offscreen-images",
                "unminified-css",
                "unminified-javascript",
                "uses-optimized-images",
                "uses-text-compression",
                "uses-responsive-images",
            ]

            for key in opportunity_keys:
                audit = audits.get(key, {})
                if audit.get("score") is not None and audit["score"] < 1:
                    self.features.opportunities.append({
                        "id": key,
                        "title": audit.get("title"),
                        "description": audit.get("description"),
                        "score": audit["score"],
                        "savings_ms": audit.get("numericValue"),
                        "display_value": audit.get("displayValue"),
                    })

            # Extract specific resource information
            rb = audits.get("render-blocking-resources", {})
            if rb.get("details"):
                items = rb["details"].get("items", [])
                self.features.render_blocking_resources = [item.get("url") for item in items]
                for item in items:
                    url = item.get("url", "")
                    if url.endswith(".css"):
                        self.features.render_blocking_css_count += 1
                    elif url.endswith(".js"):
                        self.features.render_blocking_js_count += 1

            # Unused JS
            unused_js = audits.get("unused-javascript", {})
            if unused_js.get("details"):
                self.features.unused_js_bytes = unused_js.get("numericValue")

            # Unused CSS
            unused_css = audits.get("unused-css-rules", {})
            if unused_css.get("details"):
                self.features.unused_css_bytes = unused_css.get("numericValue")

        except Exception as e:
            print(f"[!] Error extracting opportunities: {str(e)}")

    def _extract_diagnostics(self, data: Dict) -> None:
        """Extract diagnostic information"""
        try:
            lighthouse = data.get("lighthouseResult", {})
            audits = lighthouse.get("audits", {})

            diagnostic_keys = [
                "main-thread-tasks",
                "bootup-time",
                "third-party-summary",
                "font-display",
                "uses-http2",
            ]

            for key in diagnostic_keys:
                audit = audits.get(key, {})
                if audit.get("score") is not None:
                    self.features.diagnostics.append({
                        "id": key,
                        "title": audit.get("title"),
                        "description": audit.get("description"),
                        "score": audit["score"],
                        "display_value": audit.get("displayValue"),
                    })

            # Main thread work
            bootup = audits.get("bootup-time", {})
            self.features.total_js_execution_time = bootup.get("numericValue")

            # Third-party analysis
            third_party = audits.get("third-party-summary", {})
            if third_party.get("details"):
                items = third_party["details"].get("items", [])
                self.features.third_party_requests = len(items)
                self.features.third_party_size = sum(item.get("transferSize", 0) for item in items)
                self.features.third_party_blocking_time = sum(item.get("blockingTime", 0) for item in items)

            # HTTP/2
            http2_audit = audits.get("uses-http2", {})
            self.features.uses_http2 = http2_audit.get("score", 0) == 1

            # Font display
            font_audit = audits.get("font-display", {})
            self.features.font_display_set = font_audit.get("score", 0) == 1

        except Exception as e:
            print(f"[!] Error extracting diagnostics: {str(e)}")

    def _to_dict(self) -> Dict[str, Any]:
        """Convert features to dictionary"""
        return {
            "url": self.features.url,
            "analyzed_at": self.features.analyzed_at,
            "performance_score": self.features.performance_score,
            "accessibility_score": self.features.accessibility_score,
            "best_practices_score": self.features.best_practices_score,
            "seo_score": self.features.seo_score,
            "lcp_score": self.features.lcp_score,
            "lcp_value": self.features.lcp_value,
            "fid_score": self.features.fid_score,
            "fid_value": self.features.fid_value,
            "cls_score": self.features.cls_score,
            "cls_value": self.features.cls_value,
            "fcp_score": self.features.fcp_score,
            "fcp_value": self.features.fcp_value,
            "tti_score": self.features.tti_score,
            "tti_value": self.features.tti_value,
            "speed_index_score": self.features.speed_index_score,
            "speed_index_value": self.features.speed_index_value,
            "tbt_score": self.features.tbt_score,
            "tbt_value": self.features.tbt_value,
            "render_blocking_css_count": self.features.render_blocking_css_count,
            "render_blocking_js_count": self.features.render_blocking_js_count,
            "render_blocking_resources": self.features.render_blocking_resources,
            "unused_js_bytes": self.features.unused_js_bytes,
            "unused_css_bytes": self.features.unused_css_bytes,
            "total_js_execution_time": self.features.total_js_execution_time,
            "third_party_requests": self.features.third_party_requests,
            "third_party_size": self.features.third_party_size,
            "third_party_blocking_time": self.features.third_party_blocking_time,
            "uses_http2": self.features.uses_http2,
            "font_display_set": self.features.font_display_set,
            "opportunities": self.features.opportunities,
            "diagnostics": self.features.diagnostics,
            "analysis_source": self.features.analysis_source,
            "api_error": self.features.api_error,
            "fallback_used": self.features.fallback_used,
        }


class HeaderAnalyzer:
    """
    Analyzes HTTP headers for caching, compression, and security.

    This is a FREE operation that provides valuable technical insights.
    """

    def __init__(self, url: str):
        """
        Initialize the Header Analyzer.

        Args:
            url: URL to analyze
        """
        self.url = url
        self.features = TechnicalPerformanceFeatures(url=url)

    def extract(self) -> Dict[str, Any]:
        """
        Extract HTTP header information.

        Returns:
            Dictionary of header-based features
        """
        print(f"[*] Analyzing HTTP headers...")

        try:
            # Make HEAD request first (faster)
            response = requests.head(self.url, timeout=10, allow_redirects=True)
            headers = response.headers

            # Track response time
            self.features.response_time = response.elapsed.total_seconds() * 1000  # convert to ms
            self.features.http_status_code = response.status_code

            # Count redirects
            self.features.redirects_count = len(response.history)

            # Compression
            content_encoding = headers.get("Content-Encoding", "").lower()
            self.features.uses_gzip_compression = "gzip" in content_encoding
            self.features.uses_brotli_compression = "br" in content_encoding

            # Caching
            if "Cache-Control" in headers:
                self.features.has_cache_control = True
                self.features.cache_control_value = headers["Cache-Control"]

            if "ETag" in headers:
                self.features.has_etag = True

            if "Expires" in headers:
                self.features.has_expires = True
                self.features.expires_value = headers["Expires"]

            # Security Headers
            if "Strict-Transport-Security" in headers:
                self.features.has_hsts = True
                self.features.hsts_value = headers["Strict-Transport-Security"]

            if "Content-Security-Policy" in headers:
                self.features.has_csp = True
                self.features.csp_value = headers["Content-Security-Policy"]

            if "X-Frame-Options" in headers:
                self.features.has_x_frame_options = True
                self.features.x_frame_options_value = headers["X-Frame-Options"]

            if "X-Content-Type-Options" in headers:
                self.features.has_x_content_type_options = True

            if "Referrer-Policy" in headers:
                self.features.has_referrer_policy = True
                self.features.referrer_policy_value = headers["Referrer-Policy"]

            # Server information
            if "Server" in headers:
                self.features.server_type = headers["Server"]

            # HTTP version detection (approximate)
            if hasattr(response.raw, 'version'):
                if response.raw.version == 20:
                    self.features.uses_http2 = True
                elif response.raw.version == 30:
                    self.features.uses_http3 = True

            self.features.analysis_source = "headers"
            self.features.analyzed_at = time.strftime("%Y-%m-%d %H:%M:%S")

            print("[+] HTTP header analysis complete")

        except Exception as e:
            error_msg = f"Error analyzing headers: {str(e)}"
            print(f"[!] {error_msg}")
            self.features.api_error = error_msg

        return self._to_dict()

    def _to_dict(self) -> Dict[str, Any]:
        """Convert features to dictionary"""
        return {
            "url": self.features.url,
            "analyzed_at": self.features.analyzed_at,
            "response_time": self.features.response_time,
            "http_status_code": self.features.http_status_code,
            "redirects_count": self.features.redirects_count,
            "uses_gzip_compression": self.features.uses_gzip_compression,
            "uses_brotli_compression": self.features.uses_brotli_compression,
            "has_cache_control": self.features.has_cache_control,
            "cache_control_value": self.features.cache_control_value,
            "has_etag": self.features.has_etag,
            "has_expires": self.features.has_expires,
            "expires_value": self.features.expires_value,
            "has_hsts": self.features.has_hsts,
            "hsts_value": self.features.hsts_value,
            "has_csp": self.features.has_csp,
            "csp_value": self.features.csp_value,
            "has_x_frame_options": self.features.has_x_frame_options,
            "x_frame_options_value": self.features.x_frame_options_value,
            "has_x_content_type_options": self.features.has_x_content_type_options,
            "has_referrer_policy": self.features.has_referrer_policy,
            "referrer_policy_value": self.features.referrer_policy_value,
            "server_type": self.features.server_type,
            "uses_http2": self.features.uses_http2,
            "uses_http3": self.features.uses_http3,
            "analysis_source": self.features.analysis_source,
            "api_error": self.features.api_error,
        }


class LocalPerformanceAnalyzer:
    """
    Fallback analyzer using local tools (Playwright + Chrome DevTools Protocol).

    This is completely FREE and provides detailed metrics when APIs fail or reach limits.
    Requires: pip install playwright && playwright install chromium
    """

    def __init__(self, url: str):
        """
        Initialize the Local Performance Analyzer.

        Args:
            url: URL to analyze
        """
        self.url = url
        self.features = TechnicalPerformanceFeatures(url=url)

    def extract(self) -> Dict[str, Any]:
        """
        Extract performance metrics using Playwright.

        Returns:
            Dictionary of performance features
        """
        print(f"[*] Analyzing performance using local Playwright...")

        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Collect resource information
                resources = []

                def on_response(response):
                    # Try to get body size, but handle cases where body is not available
                    try:
                        body_size = len(response.body()) if response.status == 200 else 0
                    except Exception:
                        # Body not available (redirect, failed request, or unsupported resource type)
                        body_size = 0

                    resources.append({
                        "url": response.url,
                        "status": response.status,
                        "content_type": response.headers.get("content-type", ""),
                        "size": body_size,
                    })

                page.on("response", on_response)

                # Navigate and measure time
                start_time = time.time()
                page.goto(self.url, wait_until="networkidle", timeout=30000)
                load_time = (time.time() - start_time) * 1000  # ms

                # Extract performance metrics using JavaScript
                performance_data = page.evaluate("""() => {
                    const perf = performance.getEntriesByType('navigation')[0];
                    const paint = performance.getEntriesByType('paint');

                    return {
                        loadTime: perf.loadEventEnd - perf.fetchStart,
                        domContentLoaded: perf.domContentLoadedEventEnd - perf.fetchStart,
                        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime,
                        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
                        transferSize: perf.transferSize,
                        encodedBodySize: perf.encodedBodySize,
                        decodedBodySize: perf.decodedBodySize,
                    };
                }""")

                # Analyze resources
                self._analyze_resources(resources)

                # Store basic metrics
                self.features.response_time = load_time
                self.features.fcp_value = performance_data.get("firstContentfulPaint")
                self.features.total_page_size = performance_data.get("decodedBodySize")
                self.features.total_requests = len(resources)

                browser.close()

                self.features.analysis_source = "local"
                self.features.analyzed_at = time.strftime("%Y-%m-%d %H:%M:%S")

                print("[+] Local performance analysis complete")

        except ImportError:
            error_msg = "Playwright not installed. Run: pip install playwright && playwright install chromium"
            print(f"[!] {error_msg}")
            self.features.api_error = error_msg

        except Exception as e:
            error_msg = f"Error during local performance analysis: {str(e)}"
            print(f"[!] {error_msg}")
            self.features.api_error = error_msg

        return self._to_dict()

    def _analyze_resources(self, resources: List[Dict]) -> None:
        """Analyze resource breakdown"""
        for resource in resources:
            content_type = resource["content_type"].lower()
            size = resource["size"]

            if "text/html" in content_type:
                self.features.html_size = (self.features.html_size or 0) + size
                self.features.html_requests += 1
            elif "text/css" in content_type or resource["url"].endswith(".css"):
                self.features.css_size = (self.features.css_size or 0) + size
                self.features.css_requests += 1
            elif "javascript" in content_type or resource["url"].endswith(".js"):
                self.features.js_size = (self.features.js_size or 0) + size
                self.features.js_requests += 1
            elif "image" in content_type:
                self.features.image_size = (self.features.image_size or 0) + size
                self.features.image_requests += 1
            elif "font" in content_type or any(resource["url"].endswith(ext) for ext in [".woff", ".woff2", ".ttf", ".otf"]):
                self.features.font_size = (self.features.font_size or 0) + size
                self.features.font_requests += 1
            else:
                self.features.other_size = (self.features.other_size or 0) + size
                self.features.other_requests += 1

    def _to_dict(self) -> Dict[str, Any]:
        """Convert features to dictionary"""
        return {
            "url": self.features.url,
            "analyzed_at": self.features.analyzed_at,
            "response_time": self.features.response_time,
            "fcp_value": self.features.fcp_value,
            "total_page_size": self.features.total_page_size,
            "total_requests": self.features.total_requests,
            "html_size": self.features.html_size,
            "css_size": self.features.css_size,
            "js_size": self.features.js_size,
            "image_size": self.features.image_size,
            "font_size": self.features.font_size,
            "other_size": self.features.other_size,
            "html_requests": self.features.html_requests,
            "css_requests": self.features.css_requests,
            "js_requests": self.features.js_requests,
            "image_requests": self.features.image_requests,
            "font_requests": self.features.font_requests,
            "other_requests": self.features.other_requests,
            "analysis_source": self.features.analysis_source,
            "api_error": self.features.api_error,
        }


def analyze_performance(url: str, use_fallback: bool = True) -> Dict[str, Any]:
    """
    Comprehensive performance analysis with automatic fallback.

    Strategy:
    1. Try PageSpeed Insights API (best, most comprehensive)
    2. Always run HTTP Headers analysis (free, fast)
    3. If API fails and fallback enabled, use local Playwright

    Args:
        url: URL to analyze
        use_fallback: Whether to use local fallback if API fails

    Returns:
        Combined dictionary of all performance features
    """
    combined_features = {}

    # 1. Try PageSpeed Insights
    pagespeed = PerformanceAnalyzer(url)
    pagespeed_data = pagespeed.extract()
    combined_features.update(pagespeed_data)

    # 2. Always get HTTP headers (fast and free)
    headers = HeaderAnalyzer(url)
    headers_data = headers.extract()
    combined_features.update(headers_data)

    # 3. Use local fallback if API failed
    if pagespeed_data.get("api_error") and use_fallback:
        print("[*] PageSpeed API failed, using local fallback...")
        local = LocalPerformanceAnalyzer(url)
        local_data = local.extract()
        # Only update missing fields
        for key, value in local_data.items():
            if combined_features.get(key) is None:
                combined_features[key] = value

    return combined_features
