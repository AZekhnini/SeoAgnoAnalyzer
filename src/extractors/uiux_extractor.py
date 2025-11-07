"""
UI/UX Feature Extractor
Captures screenshots, runs accessibility audits, and extracts visual design features.
"""

import os
import json
import base64
from typing import Dict, Any, Optional, List
from pathlib import Path


class UIUXExtractor:
    """
    Extract UI/UX features from websites for analysis.

    Supports three input modes:
    1. URL - Captures screenshots and runs accessibility audit
    2. Single screenshot - Analyzes provided image
    3. Multiple screenshots - Analyzes provided images for different viewports
    """

    def __init__(
        self,
        url: Optional[str] = None,
        screenshot: Optional[str] = None,
        screenshots: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize extractor with URL or screenshot(s).

        Args:
            url: Website URL to analyze (captures screenshots automatically)
            screenshot: Path to single screenshot file
            screenshots: Dict mapping viewport names to screenshot paths
                        e.g., {"desktop": "path.png", "mobile": "path2.png"}
        """
        self.url = url
        self.screenshot = screenshot
        self.screenshots = screenshots

        # Determine input mode
        if url:
            self.mode = "url"
        elif screenshots:
            self.mode = "screenshots"
        elif screenshot:
            self.mode = "screenshot"
        else:
            raise ValueError("Must provide url, screenshot, or screenshots")

    def extract(self) -> Dict[str, Any]:
        """
        Extract UI/UX features based on input mode.

        Returns:
            Dictionary containing:
            - screenshots: Dict of viewport -> base64 encoded image data
            - accessibility: Accessibility audit results (if URL provided)
            - metadata: Analysis metadata
        """
        features = {
            "mode": self.mode,
            "screenshots": {},
            "accessibility": None,
            "metadata": {}
        }

        if self.mode == "url":
            # Capture screenshots and run accessibility audit
            features["screenshots"] = self._capture_screenshots()
            features["accessibility"] = self._run_accessibility_audit()
            features["metadata"]["source"] = self.url
            features["metadata"]["viewports_captured"] = list(features["screenshots"].keys())

        elif self.mode == "screenshots":
            # Load provided screenshots
            features["screenshots"] = self._load_screenshots(self.screenshots)
            features["metadata"]["source"] = "provided_screenshots"
            features["metadata"]["viewports"] = list(self.screenshots.keys())

        elif self.mode == "screenshot":
            # Load single screenshot
            screenshot_data = self._load_screenshot(self.screenshot)
            features["screenshots"]["default"] = screenshot_data
            features["metadata"]["source"] = "provided_screenshot"
            features["metadata"]["viewport"] = "default"

        return features

    def _capture_screenshots(self) -> Dict[str, str]:
        """
        Capture screenshots at multiple viewport sizes using Playwright.

        Returns:
            Dict mapping viewport name to base64 encoded image
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[!] Playwright not installed. Install with: playwright install chromium")
            return {}

        screenshots = {}

        # Define viewport configurations
        viewports = {
            "desktop": {"width": 1920, "height": 1080},
            "tablet": {"width": 768, "height": 1024},
            "mobile": {"width": 375, "height": 667},
        }

        print(f"[UI/UX] Capturing screenshots from: {self.url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)

                for viewport_name, viewport_size in viewports.items():
                    print(f"[UI/UX] Capturing {viewport_name} view ({viewport_size['width']}x{viewport_size['height']})...")

                    try:
                        context = browser.new_context(
                            viewport=viewport_size,
                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        )
                        page = context.new_page()

                        # Navigate to page
                        page.goto(self.url, wait_until="networkidle", timeout=30000)

                        # Take screenshot
                        screenshot_bytes = page.screenshot(full_page=False, type="png")

                        # Encode to base64
                        screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
                        screenshots[viewport_name] = screenshot_base64

                        context.close()
                        print(f"[UI/UX] ✓ {viewport_name} screenshot captured")

                    except Exception as e:
                        print(f"[UI/UX] Error capturing {viewport_name} screenshot: {e}")
                        continue

                browser.close()

        except Exception as e:
            print(f"[UI/UX] Error during screenshot capture: {e}")
            return {}

        print(f"[UI/UX] Successfully captured {len(screenshots)} screenshots")
        return screenshots

    def _run_accessibility_audit(self) -> Optional[Dict[str, Any]]:
        """
        Run accessibility audit using Lighthouse.

        Returns:
            Accessibility audit results or None if audit fails
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("[UI/UX] Playwright not available for accessibility audit")
            return None

        print(f"[UI/UX] Running accessibility audit...")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                # Navigate to page
                page.goto(self.url, wait_until="networkidle", timeout=30000)

                # Inject axe-core for accessibility testing
                # For now, we'll do basic accessibility checks via Playwright
                accessibility_issues = []

                # Check for common accessibility issues

                # 1. Images without alt text
                images_without_alt = page.evaluate("""() => {
                    const images = Array.from(document.querySelectorAll('img'));
                    return images.filter(img => !img.alt || img.alt.trim() === '').length;
                }""")

                if images_without_alt > 0:
                    accessibility_issues.append({
                        "type": "missing_alt_text",
                        "severity": "serious",
                        "count": images_without_alt,
                        "description": f"{images_without_alt} images missing alt text"
                    })

                # 2. Links without accessible names
                links_without_text = page.evaluate("""() => {
                    const links = Array.from(document.querySelectorAll('a'));
                    return links.filter(link => !link.textContent.trim() && !link.getAttribute('aria-label')).length;
                }""")

                if links_without_text > 0:
                    accessibility_issues.append({
                        "type": "empty_links",
                        "severity": "serious",
                        "count": links_without_text,
                        "description": f"{links_without_text} links without accessible names"
                    })

                # 3. Form inputs without labels
                inputs_without_labels = page.evaluate("""() => {
                    const inputs = Array.from(document.querySelectorAll('input:not([type="hidden"])'));
                    return inputs.filter(input => {
                        const id = input.id;
                        const hasLabel = id && document.querySelector(`label[for="${id}"]`);
                        const hasAriaLabel = input.getAttribute('aria-label');
                        return !hasLabel && !hasAriaLabel;
                    }).length;
                }""")

                if inputs_without_labels > 0:
                    accessibility_issues.append({
                        "type": "unlabeled_inputs",
                        "severity": "critical",
                        "count": inputs_without_labels,
                        "description": f"{inputs_without_labels} form inputs without labels"
                    })

                # 4. Check for lang attribute
                has_lang = page.evaluate("""() => {
                    return document.documentElement.hasAttribute('lang');
                }""")

                if not has_lang:
                    accessibility_issues.append({
                        "type": "missing_lang",
                        "severity": "serious",
                        "count": 1,
                        "description": "HTML element missing lang attribute"
                    })

                # 5. Check heading hierarchy
                heading_issues = page.evaluate("""() => {
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
                    const levels = headings.map(h => parseInt(h.tagName[1]));

                    let issues = [];

                    // Check for H1
                    const h1Count = levels.filter(l => l === 1).length;
                    if (h1Count === 0) issues.push('No H1 heading found');
                    if (h1Count > 1) issues.push(`Multiple H1 headings (${h1Count})`);

                    // Check for skipped levels
                    for (let i = 1; i < levels.length; i++) {
                        if (levels[i] - levels[i-1] > 1) {
                            issues.push(`Skipped heading level from H${levels[i-1]} to H${levels[i]}`);
                            break;
                        }
                    }

                    return issues;
                }""")

                for issue in heading_issues:
                    accessibility_issues.append({
                        "type": "heading_hierarchy",
                        "severity": "moderate",
                        "count": 1,
                        "description": issue
                    })

                browser.close()

                # Calculate accessibility score
                critical_issues = len([i for i in accessibility_issues if i["severity"] == "critical"])
                serious_issues = len([i for i in accessibility_issues if i["severity"] == "serious"])
                moderate_issues = len([i for i in accessibility_issues if i["severity"] == "moderate"])

                # Simple scoring: start at 100, deduct points
                score = 100
                score -= critical_issues * 15
                score -= serious_issues * 10
                score -= moderate_issues * 5
                score = max(0, score)

                audit_results = {
                    "score": score,
                    "issues": accessibility_issues,
                    "summary": {
                        "critical": critical_issues,
                        "serious": serious_issues,
                        "moderate": moderate_issues,
                        "total": len(accessibility_issues)
                    }
                }

                print(f"[UI/UX] ✓ Accessibility audit complete (Score: {score}/100)")
                return audit_results

        except Exception as e:
            print(f"[UI/UX] Error during accessibility audit: {e}")
            return None

    def _load_screenshot(self, screenshot_path: str) -> str:
        """
        Load and encode a screenshot file to base64.

        Args:
            screenshot_path: Path to screenshot file

        Returns:
            Base64 encoded image string
        """
        try:
            path = Path(screenshot_path)
            if not path.exists():
                raise FileNotFoundError(f"Screenshot not found: {screenshot_path}")

            with open(path, "rb") as f:
                image_bytes = f.read()

            screenshot_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print(f"[UI/UX] ✓ Loaded screenshot: {screenshot_path}")
            return screenshot_base64

        except Exception as e:
            print(f"[UI/UX] Error loading screenshot {screenshot_path}: {e}")
            raise

    def _load_screenshots(self, screenshots_dict: Dict[str, str]) -> Dict[str, str]:
        """
        Load multiple screenshots from paths.

        Args:
            screenshots_dict: Dict mapping viewport name to file path

        Returns:
            Dict mapping viewport name to base64 encoded image
        """
        loaded_screenshots = {}

        for viewport_name, screenshot_path in screenshots_dict.items():
            try:
                screenshot_base64 = self._load_screenshot(screenshot_path)
                loaded_screenshots[viewport_name] = screenshot_base64
            except Exception as e:
                print(f"[UI/UX] Skipping {viewport_name}: {e}")
                continue

        return loaded_screenshots


def analyze_uiux(
    url: Optional[str] = None,
    screenshot: Optional[str] = None,
    screenshots: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Convenience function to extract UI/UX features.

    Args:
        url: Website URL to analyze
        screenshot: Path to single screenshot
        screenshots: Dict of viewport names to screenshot paths

    Returns:
        UI/UX features dictionary

    Examples:
        >>> # Analyze URL
        >>> features = analyze_uiux(url="https://example.com")

        >>> # Analyze single screenshot
        >>> features = analyze_uiux(screenshot="screenshot.png")

        >>> # Analyze multiple screenshots
        >>> features = analyze_uiux(screenshots={
        ...     "desktop": "desktop.png",
        ...     "mobile": "mobile.png"
        ... })
    """
    extractor = UIUXExtractor(url=url, screenshot=screenshot, screenshots=screenshots)
    return extractor.extract()
