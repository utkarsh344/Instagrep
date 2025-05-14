from playwright.sync_api import sync_playwright
import json
import random
import time

USERNAME = "dr_house9000"
PASSWORD = "bububabyinstagram"
HASHTAG = "berlin"
MAX_POSTS = 10

def scrape_instagram():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True to run headless
        page = browser.new_page()

        # 1. Instagram login
        page.goto("https://www.instagram.com/accounts/login/")
        page.wait_for_timeout(3000)
        page.fill("input[name='username']", USERNAME)
        page.fill("input[name='password']", PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_timeout(5000)

        # 2. Go to hashtag page
        page.goto(f"https://www.instagram.com/explore/tags/{HASHTAG}/")
        page.wait_for_timeout(5000)

        # 3. Scroll and collect post links
        post_links = set()
        while len(post_links) < MAX_POSTS:
            anchors = page.query_selector_all("a[href^='/p/']")
            for anchor in anchors:
                href = anchor.get_attribute("href")
                post_links.add(href)
                if len(post_links) >= MAX_POSTS:
                    break
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(3000)

        print(f"[✓] Collected {len(post_links)} post links")

        posts_data = []

        # 4. Visit each post and extract data
        for link in list(post_links)[:MAX_POSTS]:
            page.goto(f"https://www.instagram.com{link}")
            page.wait_for_timeout(3000)

            try:
                caption = page.query_selector("div[role='dialog'] span").inner_text()
            except:
                caption = "No caption"

            try:
                img = page.query_selector("article img").get_attribute("src")
            except:
                img = None

            # 🗺️ Add fake coordinates (centered around Berlin)
            lat = 52.5200 + random.uniform(-0.01, 0.01)
            lng = 13.4050 + random.uniform(-0.01, 0.01)

            posts_data.append({
                "url": f"https://www.instagram.com{link}",
                "caption": caption,
                "image": img,
                "latitude": lat,
                "longitude": lng
            })

        # 5. Save data to JSON
        output_path = f"backend/data/{HASHTAG}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, indent=4)

        print(f"[✓] Saved posts to {output_path}")
        browser.close()

if __name__ == "__main__":
    scrape_instagram()
