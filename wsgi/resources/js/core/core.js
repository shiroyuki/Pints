// To be moved to common.js
var Class = (function() {
    return {
        /**
         * Class extender
         *
         * Copied from https://github.com/bisna/bisna-js/blob/master/src/bisna/application.js
         *
         * @author Guilherme Blanco <guilhermeblanco@hotmail.com>
         */
        extend: function(child, parent) {
            var tmp = function () {};

            tmp.prototype = parent.prototype;

            child.superClass = parent.prototype;
            child.prototype = new tmp();

            child.prototype.constructor = child;
        },
        make: function(kind, params) {
            var entity = new kind();
            
            entity.init(params);
            
            return entity;
        }
    }
})();

function DataRepositoryManager() {
    var _repositories = {};
    
    this.get = function(key) {
        return _repositories.hasOwnProperty(key)
            ? _repositories[key]
            : null;
    }
    
    this.set = function(key, entity, url) {
        _repositories[key] = new DataRepository(entity, url);
        
        return this;
    }
}

// To be moved to data_repository.js
var DataRepository = function(EntityClass, url, ok_callbacks) {
    this.url         = url.replace(/\/+$/, '');
    this.EntityClass = EntityClass;
    this.ok_callback = ok_callbacks || {}
};

DataRepository.prototype = {
    retrieve_ok_callback: function(method) {
        return this.ok_callback.hasOwnProperty(method)
            ? this.ok_callback[method]
            : function(r) {};
    },
    get: function(key, callback) {
        key      = key || '';
        callback = callback || this.retrieve_ok_callback('get');
        
        $.get([this.url, key].join('/'), {}, callback);
    },
    post: function(model, callback) {
        callback = callback || this.retrieve_ok_callback('post');
        
        var params = {};
        
        $.each(model.attributes, function(k, v) {
            if (v === null || v.length === 0) {
                return;
            }
            
            params[k] = v;
        });
        
        $.post(this.url + '/', params, callback);
    },
    put: function(model, callback) {
        callback = callback || this.retrieve_ok_callback('post');
        
        var params = {};
        
        $.each(model.attributes, function(k, v) {
            if (v === null || v.length === 0) {
                return;
            }
            
            params[k] = v;
        });
        
        $.ajax([this.url, model.get('id')].join('/'), {
            data:    params,
            success: callback,
            type:    'PUT'
        });
    },
    delete: function(model) {}
};

// To be moved to data_model.js
var DataModel = function() {};

DataModel.prototype = {
    kind: null,
    init: function(params) {
        params = params || {};
    
        for (var name in params) {
            if (name === '_kind') {
                this.kind = params[name];
                continue;
            }
            
            this.set(name, params[name]);
        }
        
        var count = 0;
        
        for (var name in this.attributes) {
            count++;
        }
        
        this.length = count;
        
        return this;
    },
    get: function(key) {
        if ( ! this.attributes.hasOwnProperty(key)) {
            return null;
        }
    
        return this.attributes[key];
    },
    set: function(key, value) {
        if ( ! this.attributes.hasOwnProperty(key)) {
            throw 'This object does not have the attribute "' + key + '"';
        }
    
        this.attributes[key] = value;
    
        return this;
    },
    partial_match: function(criteria) {
        var score
        for (var name in criteria) {
            var v = this.get(name);
            
            if (v === null) {
                throw 'This object does not have the attribute "' + name + '"';
            }
            
            if (v !== criteria[name]) {
                return false;
            }
        }
        
        return true;
    }
};
