from playwright.sync_api import sync_playwright
import random
import time
def run_with_proxy():
    # Proxy configuration - replace with your proxy details
    proxy_config = {
        "server": "http://geo.iproyal.com:12321",  # e.g., "http://proxy.example.com:8080"
        "username": "fOKUYXAOqvb2X9rW",
        "password": "PCpUshlGu2LEiq27_country-us_session-lNQdsPLL_lifetime-30m"
    }
    # Random user agents to rotate
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    
    with sync_playwright() as p:
        # Launch browser with stealth args
        browser = p.chromium.launch(
            headless=False,  # Set to True if you want headless
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
        
        # Create context with proxy and realistic headers
        context = browser.new_context(
            proxy=proxy_config,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
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
                'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        
        page = context.new_page()
        
        # Remove automation detection
        page.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Mock permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Mock chrome runtime
            window.chrome = {
                runtime: {}
            };
            
            // Remove automation indicators
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """)
        
        # Capture request headers
        def handle_request(request):
            print(f"URL: {request.url}")
            print(f"Headers: {dict(request.headers)}")
            print("---")
        
        page.on("request", handle_request)
        
        # Navigate to the site
        try:
        
            page.goto("https://stockx.com")
            #wait for the page to load
            page.wait_for_timeout(3000)        
            
            page.click("#nav-login")
            page.wait_for_timeout(3000)
            page.fill("#email-login", "ertepberke@gmail.com")
            time.sleep(3)
            page.fill("#password-login", "11024076742Da")
            time.sleep(3)
            page.click("#btn-login")
            page.wait_for_timeout(3000)
                
            # You can add more interactions here
            print("Page loaded successfully!")
            
            # Keep the browser open for inspection
            input("Press Enter to close the browser...")
            
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            browser.close()

def run_without_proxy():
    """Version without proxy for testing"""
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
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
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
        #wait for the page to load
        page.wait_for_timeout(10000)        
        
        page.click("#nav-login")
        page.wait_for_timeout(10000)
        page.fill("#email-login", "ertepberke@gmail.com")
        time.sleep(3)
        page.fill("#password-login", "11024076742Da")
        time.sleep(3)
        page.click("#btn-login")
        page.wait_for_timeout(10000)

        input("Press Enter to close...")
        browser.close()

if __name__ == "__main__":
    # Choose which version to run
    use_proxy = input("Use proxy? (y/n): ").lower() == 'y'
    
    if use_proxy:
        print("Remember to update proxy_config with your actual proxy details!")
        run_with_proxy()
    else:
        run_without_proxy()