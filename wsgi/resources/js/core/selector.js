function SelectorLoader() {
    var lookup_directories = {};
    var cached_selectors = {};
    
    function register(key, selector, cacheable) {
        cacheable = cacheable || false;
        
        lookup_directories[key] = {
            selector:   selector,
            auto_cache: cacheable
        };
        
        return this;
    }
    
    function has(key) {
        return lookup_directories.hasOwnProperty(key);
    }
    
    function get(key) {
        if ( ! has(key)) {
            throw 'Error SelectorLoader.get.unknown_key for ' + key;
        }
        
        if (cached_selectors.hasOwnProperty(key)) {
            return cached_selectors[key];
        }
        
        var metadata = lookup_directories[key];
        var selector = $(metadata.selector);
        
        if (metadata.cacheable) {
            cached_selectors[key] = selector;
        }
        
        return selector;
    }
    
    function is_cacheable(key) {
        if ( ! has(key)) {
            throw 'Error SelectorLoader.is_cacheable.unknown_key for ' + key;
        }
        
        return lookup_directories[key].auto_cache;
    }
    
    return {
        get:          get,
        has:          has,
        register:     register,
        is_cacheable: is_cacheable
    };
}