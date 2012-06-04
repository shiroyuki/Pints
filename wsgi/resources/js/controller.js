var controller = {
    handleEntityForm: function(e) {
        e.preventDefault();
        
        var form   = $(this),
            method = form.attr('method') || 'post',
            entity_class_name   = form.attr('data-entity'),
            primary_input_name  = form.attr('data-primary'),
            primary_input       = form.find('[name=' + primary_input_name + ']'),
            primary_input_value = $.trim(primary_input.val()),
            repository_name     = entity_class_name.toLowerCase(),
            entity_class        = window[entity_class_name];
        
        if (primary_input_value.length === 0) {
            _alert('It cannot be empty.');
            return;
        }
        
        var params = {};
        
        params[primary_input_name] = primary_input_value;
        
        var entity = Class.make(entity_class, params);
        
        primary_input.val('');
        
        try {
            // Replace this call with the event manager.
            app.repositories
                .get(repository_name)
                .post(
                    entity,
                    ui[repository_name].list
                );
        } catch (e) {
            alert(e + repository_name);
        }
        
        form.addClass('disabled');
    },
    disableForm: function(e) {
        e.preventDefault();
        widget.modalDialog.show('Disabled!');
    }
};