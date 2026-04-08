"""
Advanced Scraping Features dengan berbagai metode
"""
import logging
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from utils import WebScraper

logger = logging.getLogger(__name__)


class AdvancedScraper(WebScraper):
    """Advanced scraper dengan fitur tambahan"""
    
    def scrape_metadata(self, url: str) -> Dict:
        """Extract metadata dari halaman (SEO, OpenGraph, etc)"""
        try:
            html = self.fetch_url(url)
            if not html:
                return {}
            
            soup = self.parse_html(html)
            metadata = {}
            
            # Title
            title_tag = soup.find('title')
            metadata['title'] = self.extract_text(title_tag) if title_tag else ''
            
            # Meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    metadata[name] = content
            
            return metadata
        except Exception as e:
            logger.error(f"Error scraping metadata: {e}")
            return {}
    
    def scrape_json_ld(self, url: str) -> List[Dict]:
        """Extract JSON-LD structured data"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            json_ld_data = []
            
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    json_ld_data.append(data)
                except json.JSONDecodeError:
                    continue
            
            return json_ld_data
        except Exception as e:
            logger.error(f"Error scraping JSON-LD: {e}")
            return []
    
    def scrape_sitemap(self, sitemap_url: str) -> List[str]:
        """Extract semua URLs dari sitemap"""
        try:
            html = self.fetch_url(sitemap_url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            urls = []
            
            # Parse XML sitemap
            for loc in soup.find_all('loc'):
                url = self.extract_text(loc)
                if url:
                    urls.append(url)
            
            return urls
        except Exception as e:
            logger.error(f"Error scraping sitemap: {e}")
            return []
    
    def scrape_social_stats(self, url: str) -> Dict:
        """Try to extract social media stats"""
        try:
            html = self.fetch_url(url)
            if not html:
                return {}
            
            soup = self.parse_html(html)
            stats = {}
            
            # Look for common social share counters
            # Note: Banyak sites tidak expose ini dalam HTML lagi
            selectors = {
                'likes': ['.like-count', '.facebook-count', '[data-like-count]'],
                'shares': ['.share-count', '[data-share-count]'],
                'comments': ['.comment-count', '[data-comment-count]'],
            }
            
            for stat_type, selector_list in selectors.items():
                for selector in selector_list:
                    element = soup.select_one(selector)
                    if element:
                        stats[stat_type] = self.extract_text(element)
                        break
            
            return stats
        except Exception as e:
            logger.error(f"Error scraping social stats: {e}")
            return {}
    
    def scrape_structured_data(self, url: str) -> Dict:
        """Extract structured data (microdata, schema.org, etc)"""
        try:
            html = self.fetch_url(url)
            if not html:
                return {}
            
            soup = self.parse_html(html)
            data = {}
            
            # Microdata
            for item in soup.find_all(attrs={'itemtype': True}):
                item_type = item.get('itemtype')
                item_data = {}
                
                for prop in item.find_all(attrs={'itemprop': True}):
                    prop_name = prop.get('itemprop')
                    prop_value = prop.get('content') or self.extract_text(prop)
                    item_data[prop_name] = prop_value
                
                data[item_type] = item_data
            
            return data
        except Exception as e:
            logger.error(f"Error scraping structured data: {e}")
            return {}
    
    def scrape_forms(self, url: str) -> List[Dict]:
        """Extract form information"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            forms = []
            
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET').upper(),
                    'fields': []
                }
                
                for input_field in form.find_all(['input', 'textarea', 'select']):
                    field = {
                        'name': input_field.get('name', ''),
                        'type': input_field.get('type', 'text'),
                        'value': input_field.get('value', ''),
                    }
                    form_data['fields'].append(field)
                
                forms.append(form_data)
            
            return forms
        except Exception as e:
            logger.error(f"Error scraping forms: {e}")
            return []
    
    def scrape_images(self, url: str, min_size: int = 0) -> List[Dict]:
        """Extract semua images dari halaman"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            images = []
            
            base_url = url
            
            for img in soup.find_all('img'):
                img_url = img.get('src') or img.get('data-src')
                if img_url:
                    # Convert relative URLs to absolute
                    if img_url.startswith(('http', 'https')):
                        full_url = img_url
                    else:
                        full_url = urljoin(base_url, img_url)
                    
                    images.append({
                        'src': full_url,
                        'alt': img.get('alt', ''),
                        'title': img.get('title', ''),
                        'width': img.get('width', ''),
                        'height': img.get('height', ''),
                    })
            
            return images
        except Exception as e:
            logger.error(f"Error scraping images: {e}")
            return []
    
    def scrape_headings(self, url: str) -> Dict[str, List[str]]:
        """Extract semua headings dari halaman (H1-H6)"""
        try:
            html = self.fetch_url(url)
            if not html:
                return {}
            
            soup = self.parse_html(html)
            headings = {}
            
            for level in range(1, 7):
                tag = f'h{level}'
                headings[tag] = [
                    self.extract_text(h) for h in soup.find_all(tag)
                ]
            
            return headings
        except Exception as e:
            logger.error(f"Error scraping headings: {e}")
            return {}
    
    def scrape_videos(self, url: str) -> List[Dict]:
        """Extract video information"""
        try:
            html = self.fetch_url(url)
            if not html:
                return []
            
            soup = self.parse_html(html)
            videos = []
            
            # Video tags
            for video in soup.find_all('video'):
                video_data = {
                    'type': 'HTML5',
                    'width': video.get('width'),
                    'height': video.get('height'),
                    'sources': []
                }
                
                for source in video.find_all('source'):
                    video_data['sources'].append({
                        'src': source.get('src'),
                        'type': source.get('type'),
                    })
                
                videos.append(video_data)
            
            # YouTube embeds
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src', '')
                if 'youtube' in src or 'youtu.be' in src:
                    videos.append({
                        'type': 'YouTube',
                        'src': src,
                        'width': iframe.get('width'),
                        'height': iframe.get('height'),
                    })
            
            return videos
        except Exception as e:
            logger.error(f"Error scraping videos: {e}")
            return []


class FeedScraper(WebScraper):
    """Scraper untuk RSS/Atom feeds"""
    
    def parse_feed(self, feed_url: str) -> List[Dict]:
        """Parse RSS/Atom feed"""
        import feedparser
        
        try:
            feed = feedparser.parse(feed_url)
            entries = []
            
            for entry in feed.entries[:20]:
                entries.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'author': entry.get('author', ''),
                })
            
            return entries
        except Exception as e:
            logger.error(f"Error parsing feed: {e}")
            return []


class PDFScraper(WebScraper):
    """Scraper untuk document extraction"""
    
    def extract_pdf_text(self, pdf_url: str) -> str:
        """Extract text dari PDF (memerlukan PyPDF2)"""
        try:
            import requests
            from io import BytesIO
            
            response = requests.get(pdf_url, timeout=self.timeout)
            if response.status_code == 200:
                # Ini memerlukan PyPDF2 atau pdfplumber
                # pip install PyPDF2
                from PyPDF2 import PdfReader
                
                pdf = PdfReader(BytesIO(response.content))
                text = ""
                
                for page in pdf.pages:
                    text += page.extract_text()
                
                return text
        except ImportError:
            logger.warning("PyPDF2 tidak terinstall. Install dengan: pip install PyPDF2")
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
        
        return ""
