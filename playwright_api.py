#Browser problems constantly occurring!

import time, random, json, os
from playwright.sync_api import sync_playwright

# === Proxy ===
PROXY_SERVER = "http://brd.superproxy.io:33335"
PROXY_USERNAME = "brd-customer-hl_97d61f65-zone-cityproxy"
PROXY_PASSWORD = "dc1p9n86drhw"

# === User Agent Pool ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15A5341f Safari/604.1"
]
random_user_agent = random.choice(USER_AGENTS)

# === File paths ===
COOKIES_PATH = "stockx_cookies.json"
USER_DATA_DIR = "./user_data"

def make_stealth_context(playwright):
    context = playwright.chromium.launch_persistent_context(
        user_data_dir="playwright_data",  # or a path you want
        headless=False,
        proxy={
            "server": PROXY_SERVER,
            "username": PROXY_USERNAME,
            "password": PROXY_PASSWORD
        },
        viewport={"width": 1000, "height": 560},
        user_agent=random_user_agent,
        locale="en-US",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        },
        ignore_https_errors=True
    )

    # Stealth script injection to evade bot detection
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
        window.navigator.chrome = { runtime: {} };
    """)

    return context
def save_cookies(context):
    storage = context.storage_state()
    with open(COOKIES_PATH, "w") as f:
        json.dump(storage, f)

def load_cookies(context):
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

def login_and_save(playwright):
    context = make_stealth_context(playwright)
    page = context.new_page()
    page.goto("https://whatsmyipaddress.org", timeout=60000)
    print("ip:",page.locator(".ip").text_content())
    page.goto("https://stockx.com/", timeout=60000)
    time.sleep(5)
    page.goto("https://stockx.com/login", timeout=60000)

    time.sleep(3)
    try:
        page.fill('input[id="email-login"]', "ertepberke@gmail.com")
        page.fill('input[id="password-login"]', "11024076742Da")
        page.click('#btn-login')
        page.wait_for_url("https://stockx.com/", timeout=10000)

        save_cookies(context)
        print("✅ Logged in and cookies saved.")
    except Exception as e:
        print("❌ Login failed:", str(e))
    finally:
        context.close()

def use_cookies_and_scrape(playwright):
    context = make_stealth_context(playwright)
    load_cookies(context)
    page = context.new_page()
    page.goto("https://whatsmyipaddress.org", timeout=60000)
    print("ip:",page.locator(".ip").text_content())
    page.goto("https://stockx.com", timeout=60000)

    page.goto("https://stockx.com/category/shoes/slides-and-sandals", timeout=60000)
    time.sleep(5)
    print("✅ Page title:", page.title())
    context.close()

# === Run ===
with sync_playwright() as playwright:
    if not os.path.exists(COOKIES_PATH):
        login_and_save(playwright)
    else:
        use_cookies_and_scrape(playwright)