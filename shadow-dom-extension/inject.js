// This runs at document_start in the MAIN world (page context)
// For Manifest V3, we can inject directly into MAIN world

(function() {
    'use strict';
    
    // Store the original attachShadow method
    const originalAttachShadow = Element.prototype.attachShadow;
    
    // Override attachShadow
    Element.prototype.attachShadow = function(init) {
        // Store what mode was requested
        const requestedMode = init.mode;
        
        // Force mode to 'open'
        const newInit = {...init, mode: 'open'};
        
        // Call original with open mode
        const shadowRoot = originalAttachShadow.call(this, newInit);
        
        // Store reference to the shadow root
        this._shadowRoot = shadowRoot;
        
        // Store the original requested mode for reference
        this._shadowRootMode = requestedMode;
        
        // If it was supposed to be closed, modify the getter
        if (requestedMode === 'closed') {
            // Make shadowRoot property return null for closed roots
            // to maintain expected behavior for the page
            Object.defineProperty(this, 'shadowRoot', {
                get() {
                    // Return null to maintain closed behavior for the page
                    return null;
                },
                configurable: true
            });
        }
        
        return shadowRoot;
    };
    
    // Add a method to access any shadow root
    Element.prototype.getShadowRoot = function() {
        return this._shadowRoot || this.shadowRoot;
    };
    
    // Also expose a global function to find all shadow roots
    window.getAllShadowRoots = function() {
        const elements = document.querySelectorAll('*');
        const shadowRoots = [];
        
        for (const el of elements) {
            if (el._shadowRoot || el.shadowRoot) {
                shadowRoots.push({
                    element: el,
                    shadowRoot: el._shadowRoot || el.shadowRoot,
                    mode: el._shadowRootMode || 'open'
                });
            }
        }
        
        return shadowRoots;
    };
    
    console.log('Shadow DOM accessor injected successfully');
})();