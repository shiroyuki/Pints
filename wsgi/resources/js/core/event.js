/**
 * Small Event Control
 */

function EventControl()
{
    var _lastListenerId = 0;
    var _events      = {};
    
    this.addListener = function(kind, listener) {
        document.addEventListener(kind, listener);
        console.log('Added listener:', kind);
    }
    
    this.dispatch = function(kind) {
        evt = document.createEvent('Event');
        evt.initEvent(kind);
        
        document.dispatchEvent(evt);
        console.log('Dispatched:', kind);
    }
}