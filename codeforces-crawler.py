from playwright.sync_api import sync_playwright
import pandas as pd
import time 
import random 

# Input CSV file
INPUT_FILE = "filtered.csv"

# Column in CSV that contains submission status URLs
URL_COLUMN = "AC submission page"

# Output CSV file
OUTPUT_FILE = "codeforces_submission_result.csv"

# Path to your saved session from manual login
STORAGE_STATE_FILE = "codeforces_session.json"


def fetch_submission_details(url, context):
    page = context.new_page()
    print(f"🌐 Opening {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("table.status-frame-datatable", timeout=60000)

    rows = page.locator("table.status-frame-datatable tr")
    count = rows.count()
    print(f"🔍 Found {count} rows in the status table")

    for i in range(1, count):  # skip header row
        row = rows.nth(i)
        text = row.inner_text()
        if "Accepted" in text:
            cells = row.locator("td")
            submission_id = cells.nth(0).inner_text()
            problem_cell = cells.nth(3)
            problem_title = problem_cell.inner_text()
            problem_url = problem_cell.locator("a").get_attribute("href")
            language = cells.nth(4).inner_text()

            # Visit submission page to get source code
            parts = problem_url.split('/')
            contest_id = parts[2]
            submission_url = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
            page.goto(submission_url, wait_until="domcontentloaded")
            code = page.locator("pre#program-source-text").inner_text()
            time.sleep(random.uniform(15, 20))
            page.close()
            return {
                "submission_id": str(submission_id),
                "problem_title": str(problem_title),
                "problem_url": str(f"https://codeforces.com{problem_url}"),
                "language": str(language),
                "code": str(code)
            }
    page.close()
    print("⚠️ No Accepted submission found for this URL")
    return None


def main():
    df = pd.read_csv(INPUT_FILE)
    submission_urls = df[URL_COLUMN].tolist()
    count = 0

    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STORAGE_STATE_FILE)

        for url in submission_urls:
            count += 1
            print(f"🔍 Fetching submission {count} of {len(submission_urls)}")

            if count > 30: 
                break
            try:
                result = fetch_submission_details(url, context)
                time.sleep(random.uniform(15, 20))
                if result:
                    all_results.append(result)
            except Exception as e:
                print(f"❌ Failed to fetch {url}: {e}")

        browser.close()

    # Save all results to CSV
    if all_results:
        output_df = pd.DataFrame(all_results)
        output_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
        print(f"✅ All results saved to {OUTPUT_FILE}")
    else:
        print("⚠️ No results to save.")


if __name__ == "__main__":
    main()
