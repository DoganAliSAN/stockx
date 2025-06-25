import time, random, json, os

# Using standard Playwright with manual stealth (most reliable approach)
from playwright.sync_api import sync_playwright

# === Proxy ===
PROXY_SERVER = "http://geo.iproyal.com:12321"
PROXY_USERNAME = "fOKUYXAOqvb2X9rW"
PROXY_PASSWORD = "PCpUshlGu2LEiq27_country-us_session-lNQdsPLL_lifetime-30m"

# === Enhanced User Agent Pool ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

# === File paths ===
COOKIES_PATH = "stockx_cookies.json"
USER_DATA_DIR = "./undetected_user_data"

def get_random_viewport():
    """Return random realistic viewport sizes"""
    viewports = [
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 1536, "height": 864},
        {"width": 1440, "height": 900},
        {"width": 1280, "height": 720}
    ]
    return random.choice(viewports)

def make_stealth_context(playwright):
    """Create a stealth browser context with comprehensive evasion"""
    
    # Maximum stealth Chrome arguments
    args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-features=VizDisplayCompositor",
        "--disable-ipc-flooding-protection",
        "--disable-renderer-backgrounding", 
        "--disable-backgrounding-occluded-windows",
        "--disable-field-trial-config",
        "--disable-background-timer-throttling",
        "--disable-dev-shm-usage",
        "--disable-web-security",
        "--disable-features=TranslateUI",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-gpu-sandbox",
        "--disable-software-rasterizer",
        "--disable-background-networking",
        "--disable-default-apps",
        "--disable-sync",
        "--metrics-recording-only",
        "--no-first-run",
        "--safebrowsing-disable-auto-update",
        "--disable-component-update",
        "--disable-domain-reliability",
        "--disable-client-side-phishing-detection",
        "--disable-hang-monitor",
        "--disable-popup-blocking",
        "--disable-prompt-on-repost",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI,BlinkGenPropertyTrees",
        "--disable-plugins-discovery",
        "--disable-preconnect",
        "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
        "--use-fake-ui-for-media-stream"
    ]
    
    random_user_agent = random.choice(USER_AGENTS)
    viewport = get_random_viewport()
    
    # Launch browser with stealth args
    browser = playwright.chromium.launch(
        headless=False,  # Headless is easier to detect
        args=args
    )
    
    # Create context with realistic settings
    context = browser.new_context(
        proxy={
            "server": PROXY_SERVER,     # 👈 PROXY USED HERE
            "username": PROXY_USERNAME, # 👈 PROXY USERNAME
            "password": PROXY_PASSWORD  # 👈 PROXY PASSWORD
        },
        viewport=viewport,
        user_agent=random_user_agent,
        locale="en-US",
        timezone_id="America/New_York",
        extra_http_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        },
        ignore_https_errors=True,
        java_script_enabled=True,
        bypass_csp=True
    )
    
    return browser, context

def apply_comprehensive_stealth(page):
    """Apply the most comprehensive stealth scripts available"""
    page.add_init_script("""
        // === COMPREHENSIVE STEALTH INJECTION ===
        
        // 1. Remove webdriver property completely
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        delete navigator.webdriver;
        
        // 2. Mock Chrome runtime properly
        window.navigator.chrome = {
            runtime: {
                onConnect: undefined,
                onMessage: undefined,
                onStartup: undefined,
                onInstalled: undefined,
                onSuspend: undefined,
                onSuspendCanceled: undefined,
                onUpdateAvailable: undefined,
                onBrowserUpdateAvailable: undefined,
                onRestartRequired: undefined,
                onConnectExternal: undefined,
                onMessageExternal: undefined
            },
            loadTimes: function() {
                return {
                    commitLoadTime: 1484781500.081,
                    connectionInfo: 'http/1.1',
                    finishDocumentLoadTime: 1484781500.132,
                    finishLoadTime: 1484781500.136,
                    firstPaintAfterLoadTime: 1484781500.139,
                    firstPaintTime: 1484781500.134,
                    navigationType: 'Other',
                    npnNegotiatedProtocol: 'unknown',
                    requestTime: 1484781500.062,
                    startLoadTime: 1484781500.063,
                    wasAlternateProtocolAvailable: false,
                    wasFetchedViaSpdy: false,
                    wasNpnNegotiated: false
                };
            },
            csi: function() {
                return {
                    pageT: Math.random() * 1000,
                    startE: Math.random() * 1000,
                    tran: Math.floor(Math.random() * 15)
                };
            },
            app: {
                isInstalled: false,
                InstallState: {
                    DISABLED: 'disabled',
                    INSTALLED: 'installed',
                    NOT_INSTALLED: 'not_installed'
                },
                RunningState: {
                    CANNOT_RUN: 'cannot_run',
                    READY_TO_RUN: 'ready_to_run',
                    RUNNING: 'running'
                }
            }
        };
        
        // 3. Mock plugins realistically
        Object.defineProperty(navigator, 'plugins', {
            get: () => {
                const plugins = [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format", enabledPlugin: {}},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    },
                    {
                        0: {type: "application/pdf", suffixes: "pdf", description: "", enabledPlugin: {}},
                        description: "",
                        filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                        length: 1,
                        name: "Chrome PDF Viewer"
                    },
                    {
                        0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable", enabledPlugin: {}},
                        1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable", enabledPlugin: {}},
                        description: "",
                        filename: "internal-nacl-plugin",
                        length: 2,
                        name: "Native Client"
                    }
                ];
                
                // Make plugins behave like real PluginArray
                plugins.item = function(index) { return this[index] || null; };
                plugins.namedItem = function(name) {
                    return this.find(plugin => plugin.name === name) || null;
                };
                plugins.refresh = function() {};
                
                return plugins;
            }
        });
        
        // 4. Mock languages properly
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        
        // 5. Mock permissions API
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // 6. Remove all automation indicators
        [
            'cdc_adoQpoasnfa76pfcZLmcfl_Array',
            'cdc_adoQpoasnfa76pfcZLmcfl_Promise', 
            'cdc_adoQpoasnfa76pfcZLmcfl_Symbol',
            'cdc_adoQpoasnfa76pfcZLmcfl_JSON',
            'cdc_adoQpoasnfa76pfcZLmcfl_Object',
            'cdc_adoQpoasnfa76pfcZLmcfl_Proxy',
            'cdc_adoQpoasnfa76pfcZLmcfl_Reflect'
        ].forEach(prop => {
            delete window[prop];
        });
        
        // 7. Mock screen properties realistically
        Object.defineProperty(screen, 'availTop', {get: () => 0});
        Object.defineProperty(screen, 'availLeft', {get: () => 0});
        Object.defineProperty(screen, 'availHeight', {get: () => screen.height});
        Object.defineProperty(screen, 'availWidth', {get: () => screen.width});
        Object.defineProperty(screen, 'colorDepth', {get: () => 24});
        Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
        
        // 8. Mock battery API
        Object.defineProperty(navigator, 'getBattery', {
            value: () => Promise.resolve({
                charging: true,
                chargingTime: 0,
                dischargingTime: Infinity,
                level: Math.random() * 0.3 + 0.7, // Random between 0.7-1.0
                addEventListener: () => {},
                removeEventListener: () => {},
                dispatchEvent: () => true
            })
        });
        
        // 9. Mock connection
        Object.defineProperty(navigator, 'connection', {
            get: () => ({
                effectiveType: '4g',
                rtt: Math.floor(Math.random() * 50) + 25, // 25-75ms
                downlink: Math.random() * 10 + 5, // 5-15 Mbps
                addEventListener: () => {},
                removeEventListener: () => {}
            })
        });
        
        // 10. Mock media devices
        if (navigator.mediaDevices) {
            const originalEnumerate = navigator.mediaDevices.enumerateDevices;
            navigator.mediaDevices.enumerateDevices = () => Promise.resolve([
                {deviceId: 'default', groupId: 'group1', kind: 'audioinput', label: 'Default - Built-in Microphone'},
                {deviceId: 'default', groupId: 'group2', kind: 'audiooutput', label: 'Default - Built-in Speakers'},
                {deviceId: 'default', groupId: 'group3', kind: 'videoinput', label: 'Default - Built-in Camera'}
            ]);
        }
        
        // 11. Mock hardware concurrency realistically
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => Math.max(2, Math.floor(Math.random() * 8) + 2) // 2-10 cores
        });
        
        // 12. Mock device memory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => [2, 4, 8, 16][Math.floor(Math.random() * 4)]
        });
        
        // 13. Override iframe srcdoc
        Object.defineProperty(HTMLIFrameElement.prototype, 'srcdoc', {
            get: function() { return this.getAttribute('srcdoc'); },
            set: function(value) { this.setAttribute('srcdoc', value); }
        });
        
        // 14. Mock WebGL vendor and renderer
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.'; // UNMASKED_VENDOR_WEBGL
            if (parameter === 37446) return 'Intel Iris OpenGL Engine'; // UNMASKED_RENDERER_WEBGL
            return getParameter.call(this, parameter);
        };
        
        // 15. Mock canvas fingerprinting
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {
            const context = this.getContext('2d');
            if (context) {
                // Add slight random noise to prevent fingerprinting
                const imageData = context.getImageData(0, 0, this.width, this.height);
                for (let i = 0; i < imageData.data.length; i += 4) {
                    imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                }
                context.putImageData(imageData, 0, 0);
            }
            return originalToDataURL.apply(this, arguments);
        };
        
        // 16. Remove any toString modifications
        Function.prototype.toString = (function(original) {
            return function() {
                if (this === navigator.webdriver) {
                    return 'function webdriver() { [native code] }';
                }
                return original.apply(this, arguments);
            };
        })(Function.prototype.toString);
        
        console.log('🔒 Comprehensive stealth mode activated');
    """)

def human_like_mouse_move(page):
    """Simulate realistic human mouse movements"""
    movements = random.randint(2, 5)
    for i in range(movements):
        # More realistic mouse movement patterns
        start_x = random.randint(100, 400)
        start_y = random.randint(100, 300)
        
        # Move to start position
        page.mouse.move(start_x, start_y)
        time.sleep(random.uniform(0.1, 0.2))
        
        # Make curved movement
        for step in range(3):
            x = start_x + random.randint(-200, 200)
            y = start_y + random.randint(-100, 100)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.05, 0.15))

def human_like_delay():
    """More realistic human delays"""
    time.sleep(random.uniform(2.0, 5.0))

def human_like_typing(page, selector, text):
    """Type like a human with realistic delays"""
    element = page.locator(selector)
    element.click()
    time.sleep(random.uniform(0.3, 0.8))
    
    # Type character by character with random delays
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.05, 0.2))

def save_cookies(context):
    """Save browser state"""
    storage = context.storage_state()
    with open(COOKIES_PATH, "w") as f:
        json.dump(storage, f)

def load_cookies():
    """Load saved browser state"""
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, "r") as f:
            return json.load(f)
    return None

def login_and_save(playwright):
    """Login with maximum stealth and save session"""
    print("🔐 Starting login process with comprehensive stealth...")
    
    browser, context = make_stealth_context(playwright)
    page = context.new_page()
    
    # Apply comprehensive stealth
    apply_comprehensive_stealth(page)
    
    # Initialize PerimeterX protection
    from perimeter_x_handler import PerimeterXHandler
    px_handler = PerimeterXHandler(page, max_attempts=3, debug=True)
    px_handler.start_monitoring()
    
    try:
        # Check IP first
        print("🌐 Checking IP address...")
        page.goto("https://whatsmyipaddress.org", timeout=60000)
        
        # Wait for any PerimeterX challenges
        if not px_handler.wait_if_blocked():
            print("❌ Session blocked during IP check. Exiting...")
            return
            
        human_like_delay()
        
        try:
            ip_element = page.locator(".ip").first
            if ip_element.is_visible():
                print(f"📍 Current IP: {ip_element.text_content()}")
        except:
            print("📍 IP check completed (couldn't extract IP text)")
        
        # Navigate to StockX with human-like behavior
        print("🏠 Navigating to StockX homepage...")
        page.goto("https://stockx.com/", timeout=60000)
        
        # Check for challenges after navigation
        if not px_handler.wait_if_blocked():
            print("❌ Session blocked during StockX navigation. Exiting...")
            return
            
        human_like_mouse_move(page)
        human_like_delay()
        
        print("🔑 Going to login page...")
        page.goto("https://stockx.com/login", timeout=60000)
        
        # Check for challenges after login page load
        if not px_handler.wait_if_blocked():
            print("❌ Session blocked during login page load. Exiting...")
            return
            
        human_like_delay()
        
        # Human-like form filling
        print("✍️ Filling login form with human-like typing...")
        
        # Check before each form interaction
        if px_handler.is_session_blocked():
            print("❌ Session blocked before form filling. Exiting...")
            return
            
        human_like_typing(page, 'input[id="email-login"]', "ertepberke@gmail.com")
        time.sleep(random.uniform(0.8, 1.5))
        
        if px_handler.is_session_blocked():
            print("❌ Session blocked during form filling. Exiting...")
            return
            
        human_like_typing(page, 'input[id="password-login"]', "11024076742Da")
        
        time.sleep(random.uniform(1.0, 2.0))
        human_like_mouse_move(page)
        
        # Click login with human timing
        print("🖱️ Clicking login button...")
        
        if px_handler.is_session_blocked():
            print("❌ Session blocked before login click. Exiting...")
            return
            
        login_btn = page.locator('#btn-login')
        px_handler.human_like_click(login_btn)
        
        print("⏳ Waiting for login to complete...")
        
        # Wait for successful login with challenge monitoring
        try:
            page.wait_for_url("https://stockx.com/", timeout=15000)
            
            # Final check for challenges after login
            if not px_handler.wait_if_blocked(timeout=10):
                print("❌ Session blocked after login. Exiting...")
                return
                
            print("✅ Login successful!")
            
            # Save session
            save_cookies(context)
            print("💾 Session saved successfully!")
            
        except Exception as login_error:
            print(f"⚠️ Login may have failed or requires manual intervention: {login_error}")
            print("🔍 Current URL:", page.url)
            
            # Check if it's a challenge issue
            if px_handler.detect_challenge():
                print("🚨 PerimeterX challenge detected during login!")
                if not px_handler.wait_if_blocked(timeout=30):
                    print("❌ Could not resolve challenge. Session terminated.")
                    return
            
            # Keep browser open for manual intervention if needed
            input("Press ENTER after manually completing login (if needed)...")
            save_cookies(context)
            
    except Exception as e:
        print(f"❌ Login process failed: {str(e)}")
        print(f"🔍 Current URL: {page.url if 'page' in locals() else 'Unknown'}")
        
        # Check if failure was due to PerimeterX
        if 'px_handler' in locals() and px_handler.is_session_blocked():
            print("🚫 Login failed due to PerimeterX protection. Session terminated.")
        else:
            # Keep browser open for debugging
            input("Press ENTER to continue...")
    finally:
        # Stop PerimeterX monitoring
        if 'px_handler' in locals():
            px_handler.stop_monitoring()
        browser.close()

def use_cookies_and_scrape(playwright):
    import requests
    from bs4 import BeautifulSoup as bs
    """Use saved session and perform scraping with maximum stealth"""
    print("🚀 Starting scraping with comprehensive stealth...")
    
    browser, context = make_stealth_context(playwright)
    
    # Load saved state if exists
    storage_state = load_cookies()
    if storage_state:
        print("📥 Loading saved session...")
        context.close()
        browser, context = make_stealth_context(playwright)
        # We'll handle cookies manually since the context is fresh
    
    page = context.new_page()
    apply_comprehensive_stealth(page)
    
    try:
        page.goto("https://ipv4.icanhazip.com")
        #find element body > pre and get text 
        ip = page.locator("body > pre").text_content()
        print("ip:",ip)
        def handle_request(request):
            print(f"URL: {request.url}")
            print(f"Headers: {request.headers}")
            print("---")
        
        page.on("request", handle_request)
        page.goto("https://stockx.com")
        page.click("#nav-login")
        time.sleep(9999)
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")
        input("Press ENTER to close browser...")
    finally:
        browser.close()

def main():
    """Main execution function"""
    print("🤖 Undetected StockX Scraper Starting...")
    print("=" * 50)
    print("🔧 Using Standard Playwright with Comprehensive Stealth")
    print("=" * 50)
    
    # Create user data directory
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    with sync_playwright() as playwright:

        use_cookies_and_scrape(playwright)

if __name__ == "__main__":
    main()