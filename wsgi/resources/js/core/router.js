function Route(kind, selector, handler) {
    this.kind = kind;
    this.selector = selector;
    this.handler  = handler;
};

function Router(selectorManager) {
    var _routes = {},
        _selectorManager = selectorManager;
    
    this.setSelectorManager = function(selectorManager) {
        _selectorManager = selectorManager;
        
        return this;
    }
    
    this.register = function(route, selector, handler) {
        selector = selector || null;
        handler  = handler || null;
        
        var isRouteGiven = typeof route !== 'object';
        
        if (isRouteGiven && ! selector && ! handler) {
            throw 'Router.Exception.InvalidInput';
        } else if (isRouteGiven) {
            route = new Route(route, selector, handler);
        }
        
        console.log(route);
        
        _routes[route.selector] = route;
        
        return this;
    };
    
    this.activate = function() {
        for (var routeId in _routes) {
            var route       = _routes[routeId],
                isCacheable = _selectorManager.is_cacheable(route.selector),
                element     = _selectorManager.get(route.selector);
            
            switch (true) {
                case isCacheable:
                    element.live(route.kind, route.handler);
                    break;
                default:
                    element[route.kind](route.handler);
            }
        }
    };
};