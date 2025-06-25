from seleniumbase import Driver
import time

driver = Driver(
    browser="chrome",
    extension_dir="shadow-dom-extension"
)

try:
    driver.get("https://stockx.com/login")
    time.sleep(4)
    driver.get("https://stockx.com/login")
    # Wait for shadow root to appear
    wait_script = """
    return new Promise((resolve) => {
        let attempts = 0;
        const maxAttempts = 20; // 10 seconds total
        
        const checkForShadowRoot = () => {
            attempts++;
            const pxCaptcha = document.querySelector('#px-captcha');
            
            if (!pxCaptcha) {
                if (attempts < maxAttempts) {
                    setTimeout(checkForShadowRoot, 500);
                } else {
                    resolve({error: 'px-captcha never appeared'});
                }
                return;
            }
            
            // Try all methods to get shadow root
            const shadowRoot = pxCaptcha.shadowRoot || 
                              pxCaptcha._shadowRoot || 
                              (pxCaptcha.getShadowRoot ? pxCaptcha.getShadowRoot() : null);
            
            if (shadowRoot) {
                // Found it! Now look for iframe
                const iframe = shadowRoot.querySelector('iframe');
                if (iframe) {
                    // Try to access iframe content
                    try {
                        const iframeDoc = iframe.contentDocument;
                        if (iframeDoc) {
                            const p = iframeDoc.querySelector('p');
                            resolve({
                                success: true,
                                foundAfterAttempts: attempts,
                                text: p ? p.textContent : 'p not found',
                                hadToWait: attempts > 1
                            });
                        } else {
                            resolve({error: 'Cannot access iframe document'});
                        }
                    } catch (e) {
                        resolve({error: 'Iframe access error: ' + e.message});
                    }
                } else {
                    resolve({error: 'Iframe not found in shadow root'});
                }
            } else if (attempts < maxAttempts) {
                // Keep trying
                setTimeout(checkForShadowRoot, 500);
            } else {
                resolve({
                    error: 'Shadow root never appeared',
                    pxCaptchaFound: true,
                    attempts: attempts
                });
            }
        };
        
        checkForShadowRoot();
    });
    """
    
    result = driver.execute_async_script(wait_script)
    print("Result:", result)

finally:
    driver.quit()