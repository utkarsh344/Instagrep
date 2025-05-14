import instaloader

def download_posts_by_hashtag(hashtag="berlin", max_posts=5):
    L = instaloader.Instaloader()

    # Instagram login credentials (use a dummy account for safety)
    USERNAME = "dr_house9000"
    PASSWORD = "bububabyinstagram"

    try:
        L.login(USERNAME, PASSWORD)
        print("[✓] Logged in successfully.")
    except Exception as e:
        print(f"[!] Login failed: {e}")
        return

    print(f"🔍 Fetching posts for #{hashtag}...")
    try:
        hashtag_posts = instaloader.Hashtag.from_name(L.context, hashtag).get_posts()
        for index, post in enumerate(hashtag_posts, 1):
            print(f"{post.date} | {post.url} | {post.caption[:80]}")
            if index >= max_posts:
                break
    except Exception as e:
        print(f"[!] Failed to fetch posts: {e}")

if __name__ == "__main__":
    download_posts_by_hashtag()
