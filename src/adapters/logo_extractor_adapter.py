from ..ports.visual_extraction_port import LogoExtractorPort
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import re

class LogoExtractorAdapter(LogoExtractorPort):
    def extract_logos(self, url: str) -> dict:
        domain = urlparse(url).netloc or "unknown"
        # domain could be 'www.veelapp.com', 'brand.io', etc.
        brand_name = domain.replace('www.', '').split('.')[0].lower()
        
        # We save to data
        logos_dir = Path("data")
        logos_dir.mkdir(parents=True, exist_ok=True)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"Warning: Page load issue or timeout: {e}")
            html_content = page.content()
            browser.close()
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        candidates = []
        
        def add_candidate(src, element, candidate_type="image"):
            if not src or src.startswith("data:"):
                return
            full_url = urljoin(url, src)
            # check if already added to avoid duplicates from same URL
            if any(c['url'] == full_url for c in candidates):
                return
            candidates.append({
                "url": full_url,
                "element": element,
                "type": candidate_type,
                "score": 0,
                "reasoning": []
            })

        # 1. img tags containing logo, brand, navbar-logo
        pattern = re.compile(r'logo|brand|navbar-logo', re.IGNORECASE)
        for img in soup.find_all('img'):
            src = img.get('src')
            alt = img.get('alt', '')
            classes = ' '.join(img.get('class', []))
            img_id = img.get('id', '')
            if pattern.search(src or '') or pattern.search(alt) or pattern.search(classes) or pattern.search(img_id):
                add_candidate(src, img, "image")
                
        # 2 & 3. class names and ids containing logo
        for el in soup.find_all(attrs={"class": re.compile(r'logo', re.IGNORECASE)}):
            if el.name == 'img':
                add_candidate(el.get('src'), el, "image")
        for el in soup.find_all(attrs={"id": re.compile(r'logo', re.IGNORECASE)}):
            if el.name == 'img':
                add_candidate(el.get('src'), el, "image")
                
        # 4. SVGs in navigation/header
        for container in soup.find_all(['header', 'nav']):
            for svg in container.find_all('svg'):
                # Store svg content as url for candidate logic (custom handling)
                candidates.append({
                    "url": "svg_inline",
                    "element": svg,
                    "type": "svg",
                    "content": str(svg),
                    "score": 0,
                    "reasoning": []
                })
                
        # 5. favicon fallback
        favicon = soup.find("link", rel=re.compile("^(shortcut )?icon$", re.IGNORECASE))
        if favicon and favicon.get("href"):
            add_candidate(favicon.get("href"), favicon, "favicon")
        else:
            add_candidate("/favicon.ico", None, "favicon")
            
        # Scoring Engine
        for c in candidates:
            score = 0
            reasons = []
            el = c['element']
            
            if c['type'] == "favicon":
                # Favicons get a base score, easily outscored by proper logos
                score += 10
                reasons.append("Fallback favicon candidate")
                
            if el:
                # DOM-based signals
                parents = [p.name.lower() for p in el.parents if p.name]
                parent_classes = []
                for p in el.parents:
                    if p.name:
                        p_cls = p.get('class')
                        if p_cls:
                            if isinstance(p_cls, list):
                                parent_classes.extend(p_cls)
                            else:
                                parent_classes.append(p_cls)
                parent_classes_str = " ".join(parent_classes).lower()
                parent_ids = [p.get('id', '').lower() for p in el.parents if p.name and p.get('id')]
                parent_ids_str = " ".join(parent_ids)
                
                # Positive signals
                if 'header' in parents or 'nav' in parents or 'navbar' in parent_classes_str or 'top' in parent_classes_str:
                    score += 50
                    reasons.append("Located inside header/nav")
                    
                el_classes = " ".join(el.get('class', [])).lower() if el.name else ""
                el_id = (el.get('id') or "").lower() if el.name else ""
                
                if 'logo' in el_classes or 'brand-logo' in el_classes or 'navbar-logo' in el_classes or \
                   'logo' in el_id or 'brand-logo' in el_id:
                    score += 25
                    reasons.append("Class/ID contains 'logo' or 'brand-logo'")
                    
                # Links to homepage
                parent_a = el.find_parent('a')
                if parent_a and parent_a.get('href'):
                    href = parent_a.get('href')
                    if href in ['/', f"https://{domain}", f"http://{domain}", f"https://www.{domain}", f"http://www.{domain}"]:
                        score += 40
                        reasons.append("Image links to homepage")
                        
                # Alt text contains brand name
                alt = el.get('alt', '').lower() if el.name == 'img' else ""
                if brand_name and brand_name in alt:
                    score += 50
                    reasons.append("Alt text contains brand name")
                    
                # Dimensions reasonable
                if el.name == 'img':
                    width = el.get('width')
                    height = el.get('height')
                    if width and height:
                        try:
                            w = int(re.sub(r'\D', '', width))
                            h = int(re.sub(r'\D', '', height))
                            if 50 <= w <= 400 and 15 <= h <= 150:
                                score += 15
                                reasons.append(f"Dimensions ({w}x{h}) reasonable for logo")
                            if w < 32 and h < 32:
                                score -= 50
                                reasons.append("Very tiny icon")
                        except ValueError:
                            pass
                            
                # Negative signals
                if 'footer' in parents or 'footer' in parent_classes_str or 'footer' in parent_ids_str:
                    score -= 40
                    reasons.append("Located in footer")
                    
                if 'partner' in parent_classes_str or 'sponsor' in parent_classes_str or \
                   'partner' in parent_ids_str or 'sponsor' in parent_ids_str:
                    score -= 50
                    reasons.append("Located in partner/sponsor section")
                    
                if 'carousel' in parent_classes_str or 'slider' in parent_classes_str or 'swiper' in parent_classes_str:
                    score -= 30
                    reasons.append("Located in carousel/slider")
                    
                if 'article' in parents or 'main' in parents and 'header' not in parents:
                    # just checking if it's in content but not header
                    score -= 30
                    reasons.append("Located in article/main content")
                    
                # specific strings in URL or alt
                neg_url_alt = (c['url'] + " " + alt).lower()
                if 'app store' in neg_url_alt or 'google play' in neg_url_alt or 'badge' in el_classes:
                    score -= 100
                    reasons.append("App-store badge detected")
                    
                socials = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok']
                if any(s in neg_url_alt for s in socials):
                    score -= 100
                    reasons.append("Social icon detected")
                    
                payments = ['visa', 'mastercard', 'paypal', 'stripe', 'amex']
                if any(p in neg_url_alt for p in payments):
                    score -= 100
                    reasons.append("Payment provider logo detected")
                    
            if c['type'] == 'svg':
                pass
            elif c['type'] == 'image':
                # Filename contains brand name
                filename = Path(urlparse(c['url']).path).name.lower()
                if brand_name and brand_name in filename:
                    score += 50
                    reasons.append("Filename contains brand name")
                    
            c['score'] = score
            c['reasoning'] = reasons
            
        if not candidates:
            return {}
            
        # Sort candidates
        candidates.sort(key=lambda x: x['score'], reverse=True)
        best_candidate = candidates[0]
        
        # Download best candidate
        final_logo_url = best_candidate['url']
        primary_logo_path = logos_dir / "primary_logo.png"
        primary_logo_svg_path = logos_dir / "primary_logo.svg"
        
        # Remove old ones if exist
        if primary_logo_path.exists():
            primary_logo_path.unlink()
        if primary_logo_svg_path.exists():
            primary_logo_svg_path.unlink()
        
        downloaded_url = final_logo_url
        
        if best_candidate['type'] == 'svg':
            content = best_candidate['content']
            if 'xmlns=' not in content:
                content = content.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            with open(primary_logo_svg_path, "w", encoding="utf-8") as f:
                f.write(content)
            downloaded_url = primary_logo_svg_path.as_posix()
        else:
            try:
                response = requests.get(final_logo_url, timeout=10)
                if response.status_code == 200:
                    ext = Path(urlparse(final_logo_url).path).suffix.lower()
                    if ext == '.svg':
                        with open(primary_logo_svg_path, "wb") as f:
                            f.write(response.content)
                        downloaded_url = primary_logo_svg_path.as_posix()
                    else:
                        with open(primary_logo_path, "wb") as f:
                            f.write(response.content)
                        downloaded_url = primary_logo_path.as_posix()
            except Exception as e:
                print(f"Failed to download best logo {final_logo_url}: {e}")
                
        return {
            "logo_url": downloaded_url,
            "confidence": max(0, min(100, best_candidate['score'])), # roughly normalize or just cap
            "reasoning": best_candidate['reasoning']
        }
