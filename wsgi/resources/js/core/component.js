function _alert(message) {
    widget.modalDialog.show(message);
}

var widget = new function() {
    var _window    = $(window),
        _templates = {};
    
    this.template = function(name, template) {
        template = template || null;

        if (template === null && ! _templates.hasOwnProperty(name)) {
            return null;
        }

        if (template !== null) {
            _templates[name] = _.template(template);
        }

        return _templates[name];
    }
    
    this.modalDialog = new (function(root, _window) {
        var _selector,
            selector_query = '[data-widget=modalDialog]';

        function selector() {
            if ( ! _selector) {
                _selector = $(selector_query);
            }

            if (_selector.length === 0) {
                $('body').append([
                    '<section data-widget="modalDialog" data-option="disabled">',
                        '<a class="close">&times;</a>',
                        '<article></article>',
                    '</section>',
                    '<div class="w-dialog-underlay"></div>'
                ].join(''));

                _selector = $(selector_query);

                // Global event handlers
                var self = widget.modalDialog;

                _selector.children('.close').click(function(e) {
                    e.preventDefault();

                    self.hide();
                });

                _window.resize(function(e) {
                    self.reposition();
                });
            }

            return _selector;
        }

        this.reposition = function() {
            var _window_w = parseInt(_window.innerWidth()),
                _window_h = parseInt(_window.innerHeight()),
                _s   = selector(),
                _s_w = parseInt(_s.outerWidth()),
                _s_h = parseInt(_s.outerHeight());

            _s.css('left', (_window_w - _s_w) / 2);
        }

        this.show = function(data, title) {
            var s = selector();

            s.attr('data-option', '');
            s.children('article').html(data);

            this.reposition();
        }

        this.showTemplate = function(templateName, contexts) {
            var s = selector(),
                t = root.template(templateName);

            this.show(t(contexts));
            
            s.attr('class', templateName);
        }

        this.hide = function() {
            var s = selector();

            s.attr('data-option', 'disabled');
        }
    })(this, _window);
}