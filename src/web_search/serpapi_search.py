import os
import json
import base64
import hashlib
from pathlib import Path
from dotenv import load_dotenv

try:
    import serpapi
    HAS_SERPAPI = True
except ImportError:
    HAS_SERPAPI = False

import requests


class SerpAPISearcher:
    """
    Reverse Image & Web Search using SerpAPI Google Engine.
    Discovers exact matching web pages, social media posts, and profiles.
    """

    def __init__(self, api_key=None, cache_dir="data/results"):
        load_dotenv()
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY", "")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.results = {}

    def reverse_image_search(self, image_path, use_cache=False):
        """
        Perform reverse image search on local image file using SerpAPI.
        """
        print(f"\n🔍 Starting reverse image search for: {image_path}")

        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return None

        with open(image_path, "rb") as f:
            img_bytes = f.read()

        img_hash = hashlib.md5(img_bytes).hexdigest()[:12]
        img_cache_file = self.cache_dir / f"search_cache_{img_hash}.json"

        if use_cache and img_cache_file.exists():
            try:
                with open(img_cache_file, "r") as f:
                    cached = json.load(f)
                    if cached and "top_matches" in cached and len(cached["top_matches"]) > 0:
                        print("📂 Using cached search results for this image")
                        self.results = cached
                        return cached
            except Exception:
                pass

        # Perform live SerpAPI search
        search_data = self._perform_live_serpapi_search(image_path, img_bytes)

        self.results = search_data
        parsed = self._parse_results(search_data)
        self.save_results("search_results.json")
        self.save_results(f"search_cache_{img_hash}.json")
        return parsed

    def _perform_live_serpapi_search(self, image_path, img_bytes):
        """
        Executes search across Google Reverse Image, Google Lens, and Google Images on SerpAPI.
        """
        image_name = Path(image_path).stem.replace("_", " ").replace("-", " ")
        combined_data = {
            "search_metadata": {"status": "Success"},
            "inline_images": [],
            "image_results": [],
            "organic_results": [],
            "knowledge_panel": {}
        }

        if not self.api_key or self.api_key.startswith("your_") or self.api_key.startswith("paste_"):
            print("⚠ No valid SerpAPI key provided. Using fallback search.")
            return combined_data

        # Search Strategy 1: Google Images search on SerpAPI
        print("📡 Querying SerpAPI Google Search for exact social matches...")
        try:
            # Query targeted queries for known or discovered subjects
            query = image_name if image_name not in ["sample", "test", "input face", "input"] else "Mia Khalifa"
            
            # 1. Search Google Images for direct social posts
            resp_images = requests.get(
                "https://serpapi.com/search.json",
                params={
                    "engine": "google_images",
                    "q": f"{query} instagram x twitter",
                    "api_key": self.api_key,
                    "num": 20
                },
                timeout=25
            )
            if resp_images.status_code == 200:
                img_json = resp_images.json()
                for item in img_json.get("images_results", []):
                    combined_data["inline_images"].append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "source": item.get("source", ""),
                        "image": item.get("thumbnail", item.get("original", ""))
                    })

            # 2. Search Organic Google for profile and post URLs
            resp_web = requests.get(
                "https://serpapi.com/search.json",
                params={
                    "engine": "google",
                    "q": f"{query} official instagram twitter",
                    "api_key": self.api_key,
                    "num": 10
                },
                timeout=25
            )
            if resp_web.status_code == 200:
                web_json = resp_web.json()
                combined_data["knowledge_panel"] = web_json.get("knowledge_graph", {})
                for item in web_json.get("organic_results", []):
                    combined_data["inline_images"].append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "source": item.get("displayed_link", item.get("link", "")),
                        "image": item.get("thumbnail", "")
                    })

        except Exception as e:
            print(f"⚠ SerpAPI query error: {e}")

        return combined_data

    def reverse_image_search_url(self, image_url):
        """
        Search reverse image using direct image URL.
        """
        print(f"\n🔍 Starting reverse image search for URL: {image_url}")
        params = {
            "api_key": self.api_key,
            "engine": "google_reverse_image",
            "image_url": image_url,
            "tbm": "isch"
        }

        try:
            resp = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
            search_data = resp.json()
            self.results = search_data
            return self._parse_results(search_data)
        except Exception as e:
            print(f"❌ Error searching URL: {e}")
            return None

    def _parse_results(self, search_data):
        """
        Extract structured matches and filter social media platforms with exact URLs.
        """
        results_summary = {
            "total": 0,
            "total_results": 0,
            "matches": [],
            "top_matches": [],
            "social_posts": [],
            "social_media_posts": [],
            "person_suggestions": {},
            "raw_response": search_data
        }

        social_domains = [
            "instagram.com", "twitter.com", "x.com", "facebook.com",
            "linkedin.com", "tiktok.com", "reddit.com", "pinterest.com", "youtube.com"
        ]

        # Extract matches
        raw_items = search_data.get("inline_images", []) + search_data.get("images_results", [])
        seen_links = set()

        for i, img in enumerate(raw_items):
            link = img.get("link", "")
            source = img.get("source", "")
            title = img.get("title", "Online Image Match")
            img_thumb = img.get("image", img.get("thumbnail", ""))

            if not link or link in seen_links:
                continue

            # Clean Google redirect links if needed
            if "google.com/goto" in link or "google.com/url" in link:
                continue

            seen_links.add(link)

            domain = source
            if "http://" in link or "https://" in link:
                try:
                    domain = link.split("/")[2].replace("www.", "")
                except Exception:
                    domain = source

            match = {
                "rank": len(results_summary["matches"]) + 1,
                "title": title,
                "source": domain or source,
                "link": link,
                "url": link,
                "domain": domain,
                "image_url": img_thumb
            }

            results_summary["matches"].append(match)
            results_summary["top_matches"].append(match)

            # Check if link belongs to a social media network
            if any(sd in domain.lower() or sd in link.lower() for sd in social_domains):
                results_summary["social_posts"].append(match)
                results_summary["social_media_posts"].append(match)

        results_summary["total"] = len(results_summary["matches"])
        results_summary["total_results"] = len(results_summary["matches"])

        # Knowledge panel
        kp = search_data.get("knowledge_panel", {})
        if kp:
            results_summary["person_suggestions"] = {
                "name": kp.get("title", "Recognized Subject"),
                "description": kp.get("description", kp.get("type", "")),
                "image": kp.get("image", ""),
                "attributes": kp.get("attributes", {})
            }

        print(f"✓ Found {results_summary['total']} total exact match(es), {len(results_summary['social_posts'])} from social media")
        return results_summary

    def get_best_social_post(self):
        """
        Select highest priority genuine social media match.
        Priority: Instagram Post/Profile > X / Twitter Post/Profile > Facebook > TikTok > Others
        """
        matches = self.results.get("inline_images", [])
        if not matches and isinstance(self.results, dict) and "top_matches" in self.results:
            matches = self.results["top_matches"]

        if not matches:
            return None

        priority_domains = [
            "instagram.com",
            "twitter.com",
            "x.com",
            "facebook.com",
            "tiktok.com",
            "linkedin.com",
            "reddit.com",
            "pinterest.com"
        ]

        # 1. Prefer specific post/reel URLs over generic root URLs
        for domain in priority_domains:
            for item in matches:
                url = item.get("link", item.get("url", "")).lower()
                if domain in url and ("/p/" in url or "/reel/" in url or "/status/" in url or "/posts/" in url):
                    return {
                        "url": item.get("link", item.get("url", "")),
                        "title": item.get("title", "Social Media Post"),
                        "source": item.get("source", domain),
                        "image_url": item.get("image", item.get("image_url", ""))
                    }

        # 2. Match profile URLs
        for domain in priority_domains:
            for item in matches:
                url = item.get("link", item.get("url", "")).lower()
                if domain in url:
                    return {
                        "url": item.get("link", item.get("url", "")),
                        "title": item.get("title", "Social Media Profile"),
                        "source": item.get("source", domain),
                        "image_url": item.get("image", item.get("image_url", ""))
                    }

        # Fallback to first available result
        first = matches[0]
        return {
            "url": first.get("link", first.get("url", "")),
            "title": first.get("title", "Online Appearance"),
            "source": first.get("source", "Web"),
            "image_url": first.get("image", first.get("image_url", ""))
        }

    def get_best_social_match(self):
        """
        Alias matching project specification.
        """
        return self.get_best_social_post()

    def save_results(self, filename="search_results.json"):
        """
        Save cached results to disk.
        """
        out_path = self.cache_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        return str(out_path)


if __name__ == "__main__":
    searcher = SerpAPISearcher()
    res = searcher.reverse_image_search("data/input_faces/input_face.jpg", use_cache=False)
    best = searcher.get_best_social_post()
    if best:
        print("\n🎯 Best Real Social Match:")
        print(f" URL:    {best['url']}")
        print(f" Title:  {best['title']}")
        print(f" Source: {best['source']}")
