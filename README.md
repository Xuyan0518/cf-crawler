# Codeforces Crawler

A Python-based web scraper that extracts accepted submission details and source code from Codeforces using browser automation. This tool reads submission status URLs from a CSV file and collects submission IDs, problem information, languages, and source code.

## Features

- 🔐 **Session-based authentication**: Uses saved browser sessions to maintain login state
- 🤖 **Browser automation**: Leverages Playwright for reliable web scraping
- 📊 **CSV input/output**: Reads submission URLs from CSV and exports results to CSV
- ⏱️ **Rate limiting**: Built-in delays to avoid overwhelming the server
- 🎯 **Smart filtering**: Automatically finds and extracts "Accepted" submissions

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip for package management
- A Codeforces account (for login)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd codeforces-crawler
```

2. Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Step 1: Login and Save Session

First, you need to log in to Codeforces and save your session:

```bash
python login-codeforces.py
```

This will:
- Open a browser window
- Navigate to the Codeforces login page
- Wait for you to manually solve any Cloudflare challenges and log in
- Save your authenticated session to `codeforces_session.json`

**Note**: Press `Enter` in the terminal after you've successfully logged in.

### Step 2: Prepare Input CSV

Create a CSV file named `filtered.csv` with a column containing submission status URLs. The default column name is `"AC submission page"`, but you can modify this in the script.

Example CSV structure:
```csv
AC submission page
https://codeforces.com/contest/123/submission/456789
https://codeforces.com/contest/124/submission/456790
```

### Step 3: Run the Crawler

```bash
python codeforces-crawler.py
```

The crawler will:
- Read submission URLs from `filtered.csv`
- Visit each URL and find the first "Accepted" submission
- Extract submission details (ID, problem title, language, source code)
- Save results to `codeforces_submission_result.csv`
- Process up to 30 submissions (configurable in the script)

## Configuration

You can modify these variables in `codeforces-crawler.py`:

- `INPUT_FILE`: Path to input CSV file (default: `"filtered.csv"`)
- `URL_COLUMN`: Column name containing submission URLs (default: `"AC submission page"`)
- `OUTPUT_FILE`: Path to output CSV file (default: `"codeforces_submission_result.csv"`)
- `STORAGE_STATE_FILE`: Path to saved session file (default: `"codeforces_session.json"`)
- Submission limit: Change `count > 30` on line 75 to adjust the maximum number of submissions to process
- Rate limiting: Modify `time.sleep(random.uniform(15, 20))` to adjust delays between requests

**Note**: It is advisable to increase the duration of the pause between every fetch of the webpage to prevent `rate limit exceeded` error, which would cause your account being blocked by Codeforces. 

## Output Format

The output CSV (`codeforces_submission_result.csv`) contains the following columns:

- `submission_id`: The unique submission ID
- `problem_title`: The title of the problem
- `problem_url`: Full URL to the problem page
- `language`: Programming language used
- `code`: The complete source code of the submission

**Note**: You can also customise the data you wish to fetch from the Codeforces website. You may adjust the code as you wish. 

## Project Structure

```
codeforces-crawler/
├── codeforces-crawler.py    # Main crawler script
├── login-codeforces.py      # Login and session saving script
├── codeforces_session.json  # Saved browser session (generated)
├── filtered.csv             # Input CSV (you provide this)
├── codeforces_submission_result.csv  # Output CSV (generated)
├── cf_profile/              # Browser profile directory (generated)
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## Important Notes

- **Rate Limiting**: The script includes 15-20 second delays between requests to be respectful to Codeforces servers. Adjust these delays carefully.
- **Session Expiry**: If your session expires, re-run `login-codeforces.py` to create a new session.
- **Cloudflare**: You may need to manually solve Cloudflare challenges during login. The crawler uses the saved session to avoid repeated challenges.
- **Browser Visibility**: The browser runs in non-headless mode by default (`headless=False`) for debugging. You can change this in the script.

## Dependencies

- `playwright`: Browser automation framework
- `pandas`: CSV file handling
- `requests`: HTTP library (included but not actively used in current version)
- `tqdm`: Progress bars (included but not actively used in current version)

## Troubleshooting

- **"No Accepted submission found"**: The status page may not contain any accepted submissions, or the page structure may have changed.
- **Session expired**: Re-run `login-codeforces.py` to create a fresh session.
- **Timeout errors**: Increase timeout values in the script if you have a slow connection.
- **CSV column not found**: Ensure your input CSV has the correct column name (default: `"AC submission page"`).
