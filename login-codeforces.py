from playwright.sync_api import sync_playwright
import os

USER_DATA_DIR = os.path.join(os.getcwd(), "cf_profile")
STORAGE_STATE_FILE = "codeforces_session.json"

def login_and_save_session():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            slow_mo=50,
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = context.new_page()
        page.goto("https://codeforces.com/enter?back=%2F")

        print("✅ Solve Cloudflare + log in manually.")
        input("Press Enter after logging in successfully...")

        context.storage_state(path=STORAGE_STATE_FILE)
        print(f"✅ Session saved to {STORAGE_STATE_FILE}")

        context.close()

if __name__ == "__main__":
    login_and_save_session()
