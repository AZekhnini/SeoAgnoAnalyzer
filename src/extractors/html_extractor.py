import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json
import re
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple
from collections import Counter


@dataclass
class SEOFeatures:
    """Data class to store extracted SEO features from html"""
    # Meta tags
    title: Optional[str] = None
    title_length: int = 0
    meta_description: Optional[str] = None
    meta_description_length: int = 0
    meta_robots: Optional[str] = None
    canonical_url: Optional[str] = None

    # Headings
    h1_count: int = 0
    h1_texts: List[str] = field(default_factory=list)
    h2_count: int = 0
    h2_texts: List[str] = field(default_factory=list)
    h3_count: int = 0
    h3_texts: List[str] = field(default_factory=list)
    h4_count: int = 0
    h5_count: int = 0
    h6_count: int = 0

    # Content
    word_count: int = 0
    text_html_ratio: float = 0.0
    text: str = None

    # Content Quality & Depth (NEW)
    paragraph_count: int = 0
    average_paragraph_length: float = 0.0
    readability_score: Optional[str] = None
    content_depth_score: float = 0.0
    has_lists: bool = False
    list_count: int = 0
    has_tables: bool = False
    table_count: int = 0

    # Keyword Analysis (NEW)
    top_keywords: List[Dict[str, any]] = field(default_factory=list)
    keyword_density: Dict[str, float] = field(default_factory=dict)
    title_keyword_match: bool = False
    h1_keyword_match: bool = False

    # URL Structure (NEW)
    url_length: int = 0
    url_has_keywords: bool = False
    url_readability: str = "N/A"
    url_depth: int = 0
    url_uses_https: bool = False

    # Links
    internal_links: int = 0
    external_links: int = 0
    total_links: int = 0
    broken_links: int = 0
    internal_link_texts: List[str] = field(default_factory=list)

    # Structured data
    has_json_ld: bool = False
    json_ld_types: List[str] = field(default_factory=list)
    has_faq_schema: bool = False
    has_breadcrumb_schema: bool = False
    has_local_business_schema: bool = False

    # Open Graph
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    og_url: Optional[str] = None

    # Twitter Cards (NEW)
    twitter_card: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None

    # Performance
    page_size_bytes: int = 0
    page_size_kb: float = 0.0

    # Mobile & Language
    has_viewport: bool = False
    language: Optional[str] = None
    has_hreflang: bool = False
    hreflang_tags: List[str] = field(default_factory=list)

    # Navigation & UX (NEW)
    has_breadcrumbs: bool = False
    has_search: bool = False
    has_contact_info: bool = False

    # Content Freshness (NEW)
    has_date_modified: bool = False
    last_modified: Optional[str] = None

    # Images
    total_images: int = 0
    images_with_alt: int = 0
    images_without_alt: int = 0
    missing_alt_images: List[str] = field(default_factory=list)

class HtmlContentExtractor:
    """Main class for analyzing SEO features from HTML"""
    
    def __init__(self, url: str = None, html: str = None):
        """
        Initialize with either URL or HTML content
        
        Args:
            url: URL to fetch and analyze
            html: Raw HTML content to analyze
        """
        self.url = url
        self.html = html
        self.soup = None
        self.features = SEOFeatures()
        
        if url and not html:
            self._fetch_html()
        
        if self.html:
            self.soup = BeautifulSoup(self.html, 'html.parser')
    
    def _fetch_html(self) -> None:
        """Fetch HTML content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            self.html = response.text
            self.features.page_size_bytes = len(response.content)
            self.features.page_size_kb = round(self.features.page_size_bytes / 1024, 2)
        except requests.RequestException as e:
            return(f"Error fetching URL {self.url}: {e}")
            raise
    
    def extract_meta_tags(self) -> None:
        """Extract meta tag features"""
        if not self.soup:
            return
        
        # Title tag
        title_tag = self.soup.find('title')
        if title_tag:
            self.features.title = title_tag.get_text(strip=True)
            self.features.title_length = len(self.features.title)
        
        # Meta description
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            self.features.meta_description = meta_desc.get('content', '')
            self.features.meta_description_length = len(self.features.meta_description)
        
        # Meta robots
        meta_robots = self.soup.find('meta', attrs={'name': 'robots'})
        if meta_robots:
            self.features.meta_robots = meta_robots.get('content', '')
        
        # Canonical URL
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            self.features.canonical_url = canonical.get('href', '')
    
    def extract_headings(self) -> None:
        """Extract heading tag features"""
        if not self.soup:
            return

        # H1 tags
        h1_tags = self.soup.find_all('h1')
        self.features.h1_count = len(h1_tags)
        self.features.h1_texts = [h1.get_text(strip=True) for h1 in h1_tags]

        # H2 tags
        h2_tags = self.soup.find_all('h2')
        self.features.h2_count = len(h2_tags)
        self.features.h2_texts = [h2.get_text(strip=True) for h2 in h2_tags]

        # H3 tags
        h3_tags = self.soup.find_all('h3')
        self.features.h3_count = len(h3_tags)
        self.features.h3_texts = [h3.get_text(strip=True) for h3 in h3_tags]

        # H4, H5, H6 counts
        self.features.h4_count = len(self.soup.find_all('h4'))
        self.features.h5_count = len(self.soup.find_all('h5'))
        self.features.h6_count = len(self.soup.find_all('h6'))
    
    def extract_content_metrics(self) -> None:
        """Extract content-related metrics"""
        if not self.soup:
            return
        
        # Get visible text
        for script in self.soup(['script', 'style']):
            script.decompose()
        
        text = self.soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Word count
        words = re.findall(r'\b\w+\b', text)
        self.features.word_count = len(words)
        
        # Text to HTML ratio
        text_length = len(text)
        html_length = len(self.html) if self.html else 1
        self.features.text_html_ratio = round((text_length / html_length) * 100, 2)
    
    def extract_image_features(self) -> None:
        """Extract image-related features"""
        if not self.soup:
            return
        
        images = self.soup.find_all('img')
        self.features.total_images = len(images)
        
        for img in images:
            alt_text = img.get('alt', '')
            src = img.get('src', '')
            
            if alt_text and alt_text.strip():
                self.features.images_with_alt += 1
            else:
                self.features.images_without_alt += 1
                if src:
                    self.features.missing_alt_images.append(src[:100])  # Limit URL length
    
    def extract_link_features(self) -> None:
        """Extract link-related features"""
        if not self.soup or not self.url:
            return
        
        base_domain = urlparse(self.url).netloc
        links = self.soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            
            # Skip anchors and javascript links
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Make absolute URL
            absolute_url = urljoin(self.url, href)
            link_domain = urlparse(absolute_url).netloc
            
            if link_domain == base_domain:
                self.features.internal_links += 1
            elif link_domain:  # External link
                self.features.external_links += 1
        
        self.features.total_links = self.features.internal_links + self.features.external_links
    
    
    def extract_text(self) -> Optional[str]:
        """Extract text content"""
        if not self.soup:
            return None
        scripts = self.soup(['script', 'style'])
        for script in scripts:
            script.decompose()
        text = self.soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        self.features.text = ' '.join(chunk for chunk in chunks if chunk)

    def extract_url_structure(self) -> None:
        """Extract and analyze URL structure features"""
        if not self.url:
            return

        parsed_url = urlparse(self.url)

        # URL length
        self.features.url_length = len(self.url)

        # HTTPS check
        self.features.url_uses_https = parsed_url.scheme == 'https'

        # URL depth (number of path segments)
        path_segments = [seg for seg in parsed_url.path.split('/') if seg]
        self.features.url_depth = len(path_segments)

        # URL readability (check for readable words vs IDs/numbers)
        path = parsed_url.path.lower()
        if re.search(r'[a-z]{3,}', path):
            self.features.url_readability = "Good"
        elif re.search(r'\d{3,}', path):
            self.features.url_readability = "Poor (contains IDs)"
        else:
            self.features.url_readability = "Average"

        # Check if URL contains common keywords
        common_keywords = ['blog', 'article', 'product', 'service', 'about', 'contact', 'news']
        self.features.url_has_keywords = any(keyword in path for keyword in common_keywords)

    def extract_keyword_analysis(self) -> None:
        """Analyze keyword usage and density"""
        if not self.soup or not self.features.text:
            return

        # Get text content
        text = self.features.text.lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)

        # Common stop words to exclude
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
            'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
            'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did',
            'she', 'use', 'way', 'this', 'that', 'with', 'have', 'from', 'they',
            'been', 'more', 'when', 'what', 'were', 'will', 'would', 'there'
        }

        # Filter out stop words
        filtered_words = [word for word in words if word not in stop_words]

        # Count word frequency
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)

        # Get top 10 keywords
        top_10 = word_freq.most_common(10)
        self.features.top_keywords = [
            {"keyword": word, "count": count, "density": round((count / total_words) * 100, 2)}
            for word, count in top_10
        ]

        # Store density for top 5
        for word, count in top_10[:5]:
            self.features.keyword_density[word] = round((count / total_words) * 100, 2)

        # Check if top keywords appear in title
        if self.features.title and top_10:
            title_lower = self.features.title.lower()
            self.features.title_keyword_match = any(
                word in title_lower for word, _ in top_10[:5]
            )

        # Check if top keywords appear in H1
        if self.features.h1_texts and top_10:
            h1_text = ' '.join(self.features.h1_texts).lower()
            self.features.h1_keyword_match = any(
                word in h1_text for word, _ in top_10[:5]
            )

    def extract_content_depth(self) -> None:
        """Analyze content depth and quality indicators"""
        if not self.soup:
            return

        # Paragraph analysis
        paragraphs = self.soup.find_all('p')
        self.features.paragraph_count = len(paragraphs)

        if paragraphs:
            para_lengths = [len(p.get_text(strip=True).split()) for p in paragraphs]
            self.features.average_paragraph_length = round(
                sum(para_lengths) / len(para_lengths), 1
            )

        # Lists (ordered and unordered)
        lists = self.soup.find_all(['ul', 'ol'])
        self.features.list_count = len(lists)
        self.features.has_lists = len(lists) > 0

        # Tables
        tables = self.soup.find_all('table')
        self.features.table_count = len(tables)
        self.features.has_tables = len(tables) > 0

        # Calculate content depth score (0-100)
        score = 0

        # Word count contribution (max 30 points)
        if self.features.word_count >= 2000:
            score += 30
        elif self.features.word_count >= 1000:
            score += 20
        elif self.features.word_count >= 500:
            score += 10
        elif self.features.word_count >= 300:
            score += 5

        # Paragraph quality (max 20 points)
        if self.features.paragraph_count >= 10:
            score += 10
        elif self.features.paragraph_count >= 5:
            score += 5

        if self.features.average_paragraph_length >= 30:
            score += 10
        elif self.features.average_paragraph_length >= 15:
            score += 5

        # Structural elements (max 20 points)
        if self.features.has_lists:
            score += 10
        if self.features.has_tables:
            score += 10

        # Heading structure (max 15 points)
        if self.features.h1_count == 1:
            score += 5
        if self.features.h2_count >= 3:
            score += 5
        if self.features.h3_count >= 2:
            score += 5

        # Images (max 15 points)
        if self.features.total_images >= 5:
            score += 10
        elif self.features.total_images >= 2:
            score += 5

        if self.features.images_with_alt > 0:
            alt_ratio = self.features.images_with_alt / max(self.features.total_images, 1)
            if alt_ratio >= 0.8:
                score += 5

        self.features.content_depth_score = min(score, 100)

        # Readability assessment (simple)
        if self.features.word_count > 0:
            avg_word_length = len(self.features.text.replace(' ', '')) / self.features.word_count
            if avg_word_length < 5:
                self.features.readability_score = "Easy"
            elif avg_word_length < 6:
                self.features.readability_score = "Moderate"
            else:
                self.features.readability_score = "Complex"

    def extract_structured_data_enhanced(self) -> None:
        """Enhanced structured data extraction with specific schema detection"""
        if not self.soup:
            return

        # Find JSON-LD scripts
        json_ld_scripts = self.soup.find_all('script', type='application/ld+json')

        if json_ld_scripts:
            self.features.has_json_ld = True

            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)

                    # Handle both single objects and arrays
                    items = data if isinstance(data, list) else [data]

                    for item in items:
                        if isinstance(item, dict):
                            schema_type = item.get('@type', '')

                            # Store type
                            if schema_type and schema_type not in self.features.json_ld_types:
                                self.features.json_ld_types.append(schema_type)

                            # Check for specific schemas
                            if schema_type == 'FAQPage' or 'FAQ' in schema_type:
                                self.features.has_faq_schema = True
                            elif schema_type == 'BreadcrumbList':
                                self.features.has_breadcrumb_schema = True
                            elif schema_type == 'LocalBusiness':
                                self.features.has_local_business_schema = True

                except (json.JSONDecodeError, TypeError):
                    continue

    def extract_social_meta_tags(self) -> None:
        """Extract Open Graph and Twitter Card meta tags"""
        if not self.soup:
            return

        # Open Graph tags
        og_title = self.soup.find('meta', property='og:title')
        if og_title:
            self.features.og_title = og_title.get('content', '')

        og_desc = self.soup.find('meta', property='og:description')
        if og_desc:
            self.features.og_description = og_desc.get('content', '')

        og_image = self.soup.find('meta', property='og:image')
        if og_image:
            self.features.og_image = og_image.get('content', '')

        og_url = self.soup.find('meta', property='og:url')
        if og_url:
            self.features.og_url = og_url.get('content', '')

        # Twitter Card tags
        twitter_card = self.soup.find('meta', attrs={'name': 'twitter:card'})
        if twitter_card:
            self.features.twitter_card = twitter_card.get('content', '')

        twitter_title = self.soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title:
            self.features.twitter_title = twitter_title.get('content', '')

        twitter_desc = self.soup.find('meta', attrs={'name': 'twitter:description'})
        if twitter_desc:
            self.features.twitter_description = twitter_desc.get('content', '')

    def extract_international_seo(self) -> None:
        """Extract hreflang and language features"""
        if not self.soup:
            return

        # Language attribute
        html_tag = self.soup.find('html')
        if html_tag:
            self.features.language = html_tag.get('lang', '')

        # Hreflang tags
        hreflang_links = self.soup.find_all('link', rel='alternate', hreflang=True)
        if hreflang_links:
            self.features.has_hreflang = True
            self.features.hreflang_tags = [
                f"{link.get('hreflang')}: {link.get('href', '')[:50]}"
                for link in hreflang_links[:5]  # Limit to first 5
            ]

    def extract_navigation_ux(self) -> None:
        """Extract navigation and UX-related features"""
        if not self.soup:
            return

        # Breadcrumbs detection (common patterns)
        breadcrumb_indicators = [
            self.soup.find('nav', class_=re.compile(r'breadcrumb', re.I)),
            self.soup.find('ol', class_=re.compile(r'breadcrumb', re.I)),
            self.soup.find('div', class_=re.compile(r'breadcrumb', re.I)),
        ]
        self.features.has_breadcrumbs = any(breadcrumb_indicators)

        # Search functionality
        search_forms = self.soup.find_all('input', attrs={'type': 'search'})
        search_forms += self.soup.find_all('input', attrs={'name': re.compile(r'search|query', re.I)})
        self.features.has_search = len(search_forms) > 0

        # Contact information (email, phone)
        page_text = self.soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'

        has_email = bool(re.search(email_pattern, page_text))
        has_phone = bool(re.search(phone_pattern, page_text))
        self.features.has_contact_info = has_email or has_phone

    def extract_content_freshness(self) -> None:
        """Extract content freshness indicators"""
        if not self.soup:
            return

        # Look for last modified meta tag
        last_modified = self.soup.find('meta', attrs={'name': re.compile(r'last-modified|updated', re.I)})
        if last_modified:
            self.features.has_date_modified = True
            self.features.last_modified = last_modified.get('content', '')

        # Look for time tags (HTML5)
        time_tags = self.soup.find_all('time', datetime=True)
        if time_tags and not self.features.last_modified:
            self.features.has_date_modified = True
            self.features.last_modified = time_tags[0].get('datetime', '')

    def extract_image_features(self) -> None:
        """Extract image-related features"""
        if not self.soup:
            return

        images = self.soup.find_all('img')
        self.features.total_images = len(images)

        for img in images:
            alt_text = img.get('alt', '')
            src = img.get('src', '')

            if alt_text and alt_text.strip():
                self.features.images_with_alt += 1
            else:
                self.features.images_without_alt += 1
                if src:
                    self.features.missing_alt_images.append(src[:100])  # Limit URL length

    def extract(self) -> Dict:
        """
        Run all extraction methods and return results

        Returns:
            Dictionary of all extracted features
        """
        if not self.soup:
            return {"error": "No HTML content to analyze"}

        # Core SEO extraction
        self.extract_meta_tags()
        self.extract_headings()
        self.extract_content_metrics()
        self.extract_text()

        # Link analysis
        self.extract_link_features()

        # Image analysis
        self.extract_image_features()

        # Structured data (enhanced)
        self.extract_structured_data_enhanced()

        # Social meta tags (Open Graph + Twitter)
        self.extract_social_meta_tags()

        # Mobile
        self.features.has_viewport = self.soup.find('meta', attrs={'name': 'viewport'}) is not None

        # NEW: Phase 1 enhancements
        self.extract_url_structure()
        self.extract_keyword_analysis()
        self.extract_content_depth()
        self.extract_international_seo()
        self.extract_navigation_ux()
        self.extract_content_freshness()

        return asdict(self.features)
    
