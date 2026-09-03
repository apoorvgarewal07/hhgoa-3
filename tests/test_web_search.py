import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.web_search.serpapi_search import SerpAPISearcher
from src.utils.helpers import create_sample_face_image


def test_web_search():
    test_image = "data/input_faces/test.jpg"
    if not os.path.exists(test_image):
        create_sample_face_image(test_image)

    searcher = SerpAPISearcher()
    results = searcher.reverse_image_search(test_image, use_cache=False)

    assert results is not None, "Search returned no results"
    assert results["total"] > 0, "No matches found in search output"
    assert len(results["social_posts"]) > 0, "No social media posts detected in results"

    best = searcher.get_best_social_post()
    assert best is not None, "Best social media post is None"
    assert "url" in best and len(best["url"]) > 0, "Best post missing URL"
    assert "source" in best, "Best post missing source"

    print("✓ Web search tests passed successfully!")
    print(f"  Best Match: {best['url']} ({best['source']})")


if __name__ == "__main__":
    test_web_search()
