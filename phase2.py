from playwright.sync_api import sync_playwright
import random
import time
import json
import os

def reset_session():
    import requests

    headers = {
    'Authorization': 'Bearer f022ca794812cfa8f4cf2b038abc4dcb6591987046b5c621356ab14d46ab',
    'Content-Type': 'application/json',
    }

    json_data = {
    'residential_user_hashes': [
         '01JY9XKHHPZ984254W236K94PC',
    ],
    }

    response = requests.delete('https://resi-api.iproyal.com/v1/sessions', headers=headers, json=json_data)
    
    print("Session resetted, ip now changed")

def get_random_user_agent():
    """Generate a realistic user agent with consistent Chrome version"""
    
    # Keep Chrome version consistent (122) but vary other details
    chrome_version = "122.0.0.0"
    webkit_version = "537.36"
    
    # Different OS combinations but realistic
    os_combinations = [
        {
            "os": "Macintosh; Intel Mac OS X 10_15_7",
            "platform": '"macOS"',
            "ua": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        },
        {
            "os": "Macintosh; Intel Mac OS X 13_6_0",
            "platform": '"macOS"',
            "ua": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        },
        {
            "os": "Macintosh; Intel Mac OS X 14_1",
            "platform": '"macOS"',
            "ua": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        },
        {
            "os": "Windows NT 10.0; Win64; x64",
            "platform": '"Windows"',
            "ua": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        },
        {
            "os": "Windows NT 11.0; Win64; x64",
            "platform": '"Windows"',
            "ua": f"Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        },
        {
            "os": "X11; Linux x86_64",
            "platform": '"Linux"',
            "ua": f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/{webkit_version} (KHTML, like Gecko) Chrome/{chrome_version} Safari/{webkit_version}"
        }
    ]
    
    selected = random.choice(os_combinations)
    
    # Generate consistent sec-ch-ua header
    sec_ch_ua_variations = [
        f'"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        f'"Google Chrome";v="122", "Chromium";v="122", "Not(A:Brand";v="24"',
        f'"Chromium";v="122", "Google Chrome";v="122", "Not(A:Brand";v="99"'
    ]
    
    return {
        'user_agent': selected['ua'],
        'platform': selected['platform'],
        'sec_ch_ua': random.choice(sec_ch_ua_variations),
        'os_info': selected['os']
    }

def save_cookies(context, filename="stockx_cookies.json"):
    """Save cookies from browser context to a JSON file"""
    cookies = context.cookies()
    
    # Create cookies directory if it doesn't exist
    os.makedirs("cookies", exist_ok=True)
    filepath = os.path.join("cookies", filename)
    
    with open(filepath, 'w') as f:
        json.dump(cookies, f, indent=2)
    
    print(f"✅ Cookies saved to {filepath}")
    print(f"📊 Total cookies saved: {len(cookies)}")
    
    # Print important cookies for verification
    important_cookies = ['stockx_session', 'stockx_device_id', 'stockx_session_id']
    for cookie in cookies:
        if cookie['name'] in important_cookies:
            print(f"🔑 {cookie['name']}: {cookie['value'][:20]}...")

def run_with_proxy():
    reset_session()
    time.sleep(5)
    
    # Generate dynamic user agent
    ua_config = get_random_user_agent()
    print(f"🎭 Using User-Agent: {ua_config['os_info']}")
    print(f"🔧 Platform: {ua_config['platform']}")
    
    # Proxy configuration
    proxy_config = {
        "server": "http://geo.iproyal.com:12321",
        "username": "fOKUYXAOqvb2X9rW",
        "password": "PCpUshlGu2LEiq27_country-us_session-MORfLE7b_lifetime-5m"
    }
    
    with sync_playwright() as p:
        # Launch browser with stealth args
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-field-trial-config',
                '--disable-ipc-flooding-protection',
                '--enable-features=NetworkService,NetworkServiceLogging',
                '--force-color-profile=srgb',
                '--metrics-recording-only',
                '--use-mock-keychain',
                '--disable-extensions',
                '--no-default-browser-check',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-component-extensions-with-background-pages',
                '--disable-extensions-except',
                '--load-extension=""'
            ]
        )
        
        # Dynamic viewport based on OS
        if 'Macintosh' in ua_config['os_info']:
            viewport = {'width': random.choice([1440, 1920]), 'height': random.choice([900, 1080])}
        elif 'Windows' in ua_config['os_info']:
            viewport = {'width': random.choice([1366, 1920]), 'height': random.choice([768, 1080])}
        else:  # Linux
            viewport = {'width': random.choice([1920, 1600]), 'height': random.choice([1080, 900])}
        
        # Create context with dynamic configuration
        context = browser.new_context(
            proxy=proxy_config,
            user_agent=ua_config['user_agent'],
            viewport=viewport,
            locale='en-US',
            timezone_id='America/New_York',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Sec-Ch-Ua': ua_config['sec_ch_ua'],
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': ua_config['platform'],
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        page = context.new_page()
        
        # Enhanced anti-detection script with dynamic properties
        page.add_init_script(f"""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {{
                get: () => undefined,
            }});
            
            // Dynamic plugin count
            const pluginCount = {random.randint(3, 8)};
            Object.defineProperty(navigator, 'plugins', {{
                get: () => Array.from({{length: pluginCount}}, (_, i) => i + 1),
            }});
            
            // Mock languages with slight variations
            const languages = ['en-US', 'en'];
            Object.defineProperty(navigator, 'languages', {{
                get: () => languages,
            }});
            
            // Dynamic hardware properties
            Object.defineProperty(navigator, 'hardwareConcurrency', {{
                get: () => {random.choice([4, 8, 12, 16])},
            }});
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({{ state: Notification.permission }}) :
                    originalQuery(parameters)
            );
            
            // Mock chrome runtime
            window.chrome = {{
                runtime: {{}}
            }};
            
            // Remove automation indicators
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            
            // Add realistic screen properties with slight variance
            const screenWidth = {viewport['width']} + {random.randint(-10, 10)};
            const screenHeight = {viewport['height']} + {random.randint(-10, 10)};
            
            Object.defineProperty(screen, 'width', {{ get: () => screenWidth }});
            Object.defineProperty(screen, 'height', {{ get: () => screenHeight }});
            Object.defineProperty(screen, 'availWidth', {{ get: () => screenWidth - 10 }});
            Object.defineProperty(screen, 'availHeight', {{ get: () => screenHeight - 100 }});
        """)
        
        # Capture request headers
        # def handle_request(request):
        #     if 'stockx.com' in request.url:
        #         print(f"URL: {request.url}")
        #         print(f"Headers: {dict(request.headers)}")
        #         print("---")
        
        # page.on("request", handle_request)
        
        # Navigate to the site

        try:
            print("🚀 Navigating to StockX...")
            page.goto("https://stockx.com")
            time.sleep(15)
            page.click('p:contains("Hold")')
            
            # Human-like wait with variance
            wait_time = random.randint(2000, 4000)
            page.wait_for_timeout(wait_time)
            
            print("🔐 Attempting login...")
            page.click("#nav-login")
            page.wait_for_timeout(random.randint(2000, 4000))
            
            # Type with human-like delays
            page.fill("#email-login", "ertepberke@gmail.com")
            time.sleep(random.uniform(2, 4))
            
            page.fill("#password-login", "11024076742Da")
            time.sleep(random.uniform(2, 4))
            
            page.click("#btn-login")
            page.wait_for_timeout(random.randint(4000, 6000))

            # Check if login was successful
            try:
                print("📋 Checking login status...")
                page.goto("https://stockx.com/profile", timeout=10000)
                page.wait_for_url("https://stockx.com/profile", timeout=10000)
                page.wait_for_timeout(5000)

                print("✅ Login successful!")
                save_cookies(context, "stockx_logged_in_cookies.json")
                
            except:
                print("❌ Login may have failed or took too long")
                save_cookies(context, "stockx_partial_cookies.json")
                
            print("✨ Page loaded successfully!")
            input("Press Enter to close the browser...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            browser.close()

def run_without_proxy():
    """Version without proxy for testing"""
    # Generate dynamic user agent for non-proxy version too
    ua_config = get_random_user_agent()
    print(f"🎭 Using User-Agent: {ua_config['os_info']}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Dynamic viewport
        if 'Macintosh' in ua_config['os_info']:
            viewport = {'width': random.choice([1440, 1920]), 'height': random.choice([900, 1080])}
        elif 'Windows' in ua_config['os_info']:
            viewport = {'width': random.choice([1366, 1920]), 'height': random.choice([768, 1080])}
        else:
            viewport = {'width': random.choice([1920, 1600]), 'height': random.choice([1080, 900])}
        
        context = browser.new_context(
            user_agent=ua_config['user_agent'],
            viewport=viewport,
            extra_http_headers={
                'sec-ch-ua': ua_config['sec_ch_ua'],
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': ua_config['platform']
            }
        )
        
        page = context.new_page()
        
        # Anti-detection script
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        page.goto("https://stockx.com")
        page.wait_for_timeout(10000)        
        
        page.click("#nav-login")
        page.wait_for_timeout(10000)
        page.fill("#email-login", "ertepberke@gmail.com")
        time.sleep(3)
        page.fill("#password-login", "11024076742Da")
        time.sleep(3)
        page.click("#btn-login")
        page.wait_for_timeout(10000)
        
        # Check if login was successful and save cookies
        try:
            page.wait_for_selector('[data-testid="user-menu"], #nav-logout, .user-avatar', timeout=10000)
            print("✅ Login successful!")
            save_cookies(context, "stockx_logged_in_cookies.json")
        except:
            print("❌ Login may have failed or took too long")
            save_cookies(context, "stockx_partial_cookies.json")

        input("Press Enter to close...")
        browser.close()

if __name__ == "__main__":
    # Choose which version to run
    use_proxy = input("Use proxy? (y/n): ").lower() == 'y'
    
    if use_proxy:
        print("🔧 Using proxy with dynamic user-agent rotation...")
        run_with_proxy()
    else:
        print("🔧 Running without proxy with dynamic user-agent...")
        run_without_proxy()