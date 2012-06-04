widget.template(
    'project-data-table-entry',
    [
        '<% _.each(projects, function(project) { %>',
            '<tr>',
                '<td><%= project.name %></td>',
                '<td><%= project.owner.alias %></td>',
                '<td><%= project.due %></td>',
                '<td><%= project.updated %></td>',
            '</tr>',
        '<% }); %>'
    ].join('')
);

var ui = (function(app) {
    'use strict';
    
    var s = app.selector;
    
    return {
        prompts: {
            create: function() {
                s.get('prompts').removeClass('disabled');
                s.get('entity-form').hide();
                s.get('entity-form')
                    .filter(
                        '[data-entity='
                        + ( app.project
                            ? 'Reminder'
                            : 'Project'
                        ) + ']'
                    ).show();
            },
            hide: function() {
                s.get('prompts').addClass('disabled');
            }
        },
        project: {
            list: function() {
                console.log('Shit!');
                
                var selectorKey  = 'projects-data-table-tbody',
                    templateName = 'project-data-table-entry',
                    template     = widget.template(templateName),
                    dropzone, output;
                
                if ( ! s.has(selectorKey)) {
                    return;
                }
                
                var dropzone = s.get(selectorKey);
                
                app.repositories
                    .get('project')
                    .get(null, function(projects) {
                        output = template({projects: projects});
                    
                        dropzone.html(output);
                    });
            }
        },
        reminder: {
            list: function() {
                if ( ! s.has('reminder-list')) {
                    return;
                }
                
                var l = s.get('reminder-list');
                
                app.repository.reminder.get(null, function(reminders) {
                    l.empty();
            
                    $.each(reminders, function(index, reminder) {
                        reminder = Class.make(Reminder, reminder);
                        
                        l.append([
                            '<li data-alias="', reminder.get('alias'), '"',
                                ' data-id="', reminder.get('id'), '"',
                                ' data-type="', reminder.kind, '"',
                                ' class="', (reminder.get('complete') ? 'complete' : ''), '"',
                            '>',
                                '<a class="checkbox"></a>',
                                reminder.get('summary'),
                            '</li>'
                        ].join(''));
                    });
                });
            }
        }
    };
})(app);