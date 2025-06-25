import json
import os
import requests

def load_cookies(filename="stockx_partial_cookies.json"):
    #check if filename exists
    if not os.path.exists("cookies/" + filename):
        print(f"❌ Cookie file not found: {filename}")
        print("🔍 Available cookie files:")
        cookies_dir = "cookies"
        if os.path.exists(cookies_dir):
            for file in os.listdir(cookies_dir):
                if file.endswith('.json'):
                    print(f"   - {file}")
        return None

    """Load cookies from saved JSON file"""
    filepath = os.path.join("cookies", filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Cookie file not found: {filepath}")
        print("🔍 Available cookie files:")
        cookies_dir = "cookies"
        if os.path.exists(cookies_dir):
            for file in os.listdir(cookies_dir):
                if file.endswith('.json'):
                    print(f"   - {file}")
        return None
    
    with open(filepath, 'r') as f:
        cookies = json.load(f)
    
    print(f"✅ Loaded {len(cookies)} cookies from {filepath}")
    return cookies

def cookies_to_dict(cookies):
    """Convert Playwright cookies to simple dict format"""
    if not cookies:
        return {}
    
    cookie_dict = {}
    
    # Handle both Playwright format and simple dict format
    for cookie in cookies:
        if isinstance(cookie, dict):
            if 'name' in cookie and 'value' in cookie:
                # Playwright format: {"name": "...", "value": "..."}
                cookie_dict[cookie['name']] = cookie['value']
            else:
                # Simple dict format: {"cookie_name": "cookie_value"}
                cookie_dict.update(cookie)
        else:
            print(f"⚠️  Unexpected cookie format: {cookie}")
    
    # Print important cookies for verification
    important_cookies = ['stockx_session', 'stockx_device_id', 'stockx_session_id', 'loggedIn', 'token']
    print("🔑 Important cookies loaded:")
    for name, value in cookie_dict.items():
        if name in important_cookies:
            print(f"   {name}: {value[:20]}...")
    
    # Check if we have authentication cookies
    if 'loggedIn' in cookie_dict and 'token' in cookie_dict:
        print("🎉 AUTHENTICATED cookies detected!")
    else:
        print("⚠️  NO authentication cookies found - will be anonymous session")
        print("   Missing: loggedIn and/or token cookies")
    
    print(f"📊 Total cookies: {len(cookie_dict)}")
    return cookie_dict

def make_scrapfly_request(url, cookies_dict, method="GET", data=None, api_headers=None):
    """Make request using ScrapFly API with requests library"""
    
    # Your ScrapFly API key
    SCRAPFLY_API_KEY = "scp-live-5219a5535b2742818451e6a43e1ca637"
    
    # ScrapFly API endpoint
    scrapfly_url = "https://api.scrapfly.io/scrape"
    
    # Base headers for browser simulation
    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Use API headers if provided, otherwise use base headers
    headers = api_headers if api_headers else base_headers
    
    # Convert cookies dict to cookie string format
    cookie_string = "; ".join([f"{name}={value}" for name, value in cookies_dict.items()])
    
    # Prepare ScrapFly parameters
    params = {
        'key': SCRAPFLY_API_KEY,
        'url': url,
        'country': 'US',
        'render_js': 'true',
        'wait_for_selector': 'body',
        'cookies': cookie_string,
    }
    
    # Add headers in the correct format for ScrapFly
    for header_name, header_value in headers.items():
        params[f'headers[{header_name}]'] = header_value
    
    # Add method and data for POST requests
    if method.upper() == 'POST':
        params['method'] = 'POST'
        if data:
            params['data'] = data
    
    # Debug: Save request details for debugging
    debug_info = {
        'url': url,
        'method': method,
        'scrapfly_url': scrapfly_url,
        'headers_sent': headers,
        'cookies_dict': cookies_dict,
        'cookie_string': cookie_string,
        'all_params': {k: v for k, v in params.items() if k != 'key'},  # Don't save API key
        'cookie_count': len(cookies_dict),
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }
    
    # Save debug info to file
    debug_filename = f"debug_request_{url.replace('https://', '').replace('/', '_').replace('?', '_')[:50]}.json"
    with open(debug_filename, 'w') as f:
        json.dump(debug_info, f, indent=2)
    print(f"🐛 Debug info saved to {debug_filename}")
    
    try:
        print(f"📡 Making {method} request to: {url}")
        print(f"🍪 Sending {len(cookies_dict)} cookies")
        print(f"📋 Cookie string length: {len(cookie_string)} characters")
        
        # Make request to ScrapFly API
        response = requests.get(scrapfly_url, params=params, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('result', {}).get('success'):
                content = result['result']['content']
                status_code = result['result']['status_code']
                
                # Extract cookies from response if available
                response_cookies = result.get('result', {}).get('cookies', {})
                
                print(f"✅ Success! Status: {status_code}")
                print(f"📄 Content length: {len(content)} characters")
                print(f"🍪 Response cookies received: {len(response_cookies)}")
                
                # Save response cookies for debugging
                if response_cookies:
                    cookies_filename = f"response_cookies_{url.replace('https://', '').replace('/', '_')[:30]}.json"
                    with open(cookies_filename, 'w') as f:
                        json.dump(response_cookies, f, indent=2)
                    print(f"🍪 Response cookies saved to {cookies_filename}")
                
                # Save full response details
                response_debug = {
                    'success': True,
                    'status_code': status_code,
                    'content_length': len(content),
                    'response_cookies': response_cookies,
                    'full_scrapfly_response': result,
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                }
                
                response_filename = f"response_debug_{url.replace('https://', '').replace('/', '_')[:30]}.json"
                with open(response_filename, 'w') as f:
                    json.dump(response_debug, f, indent=2)
                print(f"📊 Full response debug saved to {response_filename}")
                
                return {
                    'success': True,
                    'content': content,
                    'status_code': status_code,
                    'response_cookies': response_cookies,
                    'full_result': result
                }
            else:
                error_msg = result.get('result', {}).get('error', 'Unknown error')
                print(f"❌ ScrapFly request failed: {error_msg}")
                
                # Save error details
                error_debug = {
                    'success': False,
                    'error': error_msg,
                    'full_response': result,
                    'timestamp': __import__('datetime').datetime.now().isoformat()
                }
                
                error_filename = f"error_debug_{url.replace('https://', '').replace('/', '_')[:30]}.json"
                with open(error_filename, 'w') as f:
                    json.dump(error_debug, f, indent=2)
                print(f"❌ Error details saved to {error_filename}")
                
                return {'success': False, 'error': result}
        
        else:
            print(f"❌ ScrapFly API error: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Save API error details
            api_error_debug = {
                'api_status_code': response.status_code,
                'api_response': response.text,
                'timestamp': __import__('datetime').datetime.now().isoformat()
            }
            
            with open("api_error_debug.json", 'w') as f:
                json.dump(api_error_debug, f, indent=2)
            print("❌ API error details saved to api_error_debug.json")
            
            return {'success': False, 'error': response.text}
    
    except Exception as e:
        print(f"❌ Request error: {e}")
        
        # Save exception details
        exception_debug = {
            'exception': str(e),
            'exception_type': type(e).__name__,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        
        with open("exception_debug.json", 'w') as f:
            json.dump(exception_debug, f, indent=2)
        print("❌ Exception details saved to exception_debug.json")
        
        return {'success': False, 'error': str(e)}

def test_stockx_pages():
    """Test authenticated requests to StockX pages"""
    
    # Load cookies
    cookies = load_cookies()
    if not cookies:
        return
    
    cookies_dict = cookies_to_dict(cookies)
    
    # Test URLs
    test_urls = [
        "https://stockx.com/",
        "https://stockx.com/profile",
        "https://stockx.com/portfolio",
    ]
    
    print("\n🚀 Testing StockX pages with ScrapFly...\n")
    
    for url in test_urls:
        result = make_scrapfly_request(url, cookies_dict)
        
        if result['success']:
            content = result['content'].lower()
            
            # Check if we're logged in
            if any(indicator in content for indicator in ['profile', 'portfolio', 'logout', 'account']):
                print("🎉 Appears to be authenticated!")
            else:
                print("⚠️  May not be authenticated - check content")
            
            # Save response
            filename = url.replace('https://stockx.com/', '').replace('/', '_') or 'homepage'
            with open(f"response_{filename}.html", 'w', encoding='utf-8') as f:
                f.write(result['content'])
            print(f"💾 Response saved to response_{filename}.html")
        
        print("-" * 50)

def test_stockx_api():
    """Test authenticated API request to StockX GraphQL"""
    
    # Load cookies
    cookies = load_cookies()
    if not cookies:
        return
    
    cookies_dict = cookies_to_dict(cookies)
    
    # API endpoint
    api_url = "https://stockx.com/api/p/e"
    
    # API-specific headers
    api_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'App-Platform': 'Iron',
        'App-Version': '2025.06.15.01',
        'Apollographql-Client-Name': 'Iron',
        'Apollographql-Client-Version': '2025.06.15.01',
        'Selected-Country': 'US',
        'Origin': 'https://stockx.com',
        'Referer': 'https://stockx.com/',
    }
    
    # GraphQL query
    graphql_payload = {
        "query": """
        query GetTrendingProducts {
            browse(input: {
                category: "sneakers",
                sort: {id: FEATURED},
                page: {index: 0, size: 10}
            }) {
                results {
                    edges {
                        node {
                            ... on Product {
                                id
                                title
                                brand
                                market {
                                    bidAskData {
                                        lowestAsk
                                        highestBid
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """,
        "variables": {}
    }
    
    print("\n🔥 Testing StockX GraphQL API...\n")
    
    result = make_scrapfly_request(
        api_url, 
        cookies_dict, 
        method="POST", 
        data=json.dumps(graphql_payload),
        api_headers=api_headers
    )
    
    if result['success']:
        try:
            data = json.loads(result['content'])
            
            if 'data' in data and 'browse' in data['data']:
                products = data['data']['browse']['results']['edges']
                print(f"📦 Found {len(products)} trending products:")
                
                for i, edge in enumerate(products[:5]):  # Show first 5
                    product = edge['node']
                    title = product.get('title', 'N/A')
                    brand = product.get('brand', 'N/A')
                    
                    market = product.get('market', {})
                    bid_ask = market.get('bidAskData', {}) if market else {}
                    lowest_ask = bid_ask.get('lowestAsk', 'N/A') if bid_ask else 'N/A'
                    
                    print(f"   {i+1}. {brand} - {title} | Ask: ${lowest_ask}")
            
            else:
                print("⚠️  Unexpected API response structure")
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            # Save API response
            with open("stockx_api_response.json", 'w') as f:
                json.dump(data, f, indent=2)
            print("💾 API response saved to stockx_api_response.json")
            
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON response")
            print(f"Raw response: {result['content'][:500]}...")

def test_simple_request():
    """Simple test to verify cookies work"""
    
    print("\n🧪 Simple cookie test...\n")
    
    # Load cookies
    cookies = load_cookies()
    if not cookies:
        return
    
    cookies_dict = cookies_to_dict(cookies)
    
    # Simple homepage request
    result = make_scrapfly_request("https://stockx.com/", cookies_dict)
    
    if result['success']:
        content = result['content']
        
        # Basic checks
        if 'stockx' in content.lower():
            print("✅ Successfully loaded StockX page")
        
        # Check for authentication indicators
        auth_indicators = ['profile', 'portfolio', 'account', 'logout', 'sell now', 'my collection']
        login_indicators = ['login', 'sign in', 'create account']
        
        auth_found = any(term in content.lower() for term in auth_indicators)
        login_found = any(term in content.lower() for term in login_indicators)
        
        if auth_found and not login_found:
            print("🎉 AUTHENTICATED session detected!")
            print("   ✓ Found user-specific content")
            print("   ✓ No login prompts detected")
        elif login_found:
            print("❌ NOT authenticated - login form detected")
            print("   Login indicators found in page")
        else:
            print("⚠️  Authentication status unclear")
        
        # Check for specific authenticated elements
        if 'bef2162d-3e4f-11f0-a79a-12568e98116f' in content:
            print("🔑 Found your specific user ID in page!")
        
        # Look for JSON data that shows user info
        if '"loggedIn":true' in content or '"isLoggedIn":true' in content:
            print("🎯 JavaScript indicates user is logged in!")
        
        print(f"📊 Page size: {len(content)} characters")
        
        # Save for inspection
        with open("simple_test.html", 'w', encoding='utf-8') as f:
            f.write(content)
        print("💾 Saved to simple_test.html")
        
        # Extract and show any user-specific data
        import re
        user_data_patterns = [
            r'"user":\s*{[^}]+}',
            r'"customer":\s*{[^}]+}',
            r'"profile":\s*{[^}]+}',
            r'loggedIn["\']?\s*:\s*["\']?([^"\']+)',
        ]
        
        for pattern in user_data_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"🔍 Found user data: {matches[0][:100]}...")
                break

if __name__ == "__main__":
    print("🍪 StockX ScrapFly + Requests Test\n")
    
    # Replace with your ScrapFly API key
    print("⚠️  Remember to replace 'YOUR_SCRAPFLY_API_KEY' with your actual API key!\n")
    
    test_choice = input("Choose test:\n1. Simple test\n2. Web pages\n3. GraphQL API\n4. All tests\nEnter choice (1-4): ").strip()
    
    if test_choice in ['1', '4']:
        test_simple_request()
    
    if test_choice in ['2', '4']:
        test_stockx_pages()
    
    if test_choice in ['3', '4']:
        test_stockx_api()
    
    print("\n🎯 Test complete!")
    print("\n💡 Next steps:")
    print("   1. Check the saved HTML/JSON files")
    print("   2. Look for authentication indicators")
    print("   3. Verify product data if API worked")