app.repositories
    .set('project', Project, '/api/v1/projects')
    .set('reminder', Reminder, '/api/v1/reminders');

app.selector
    .register('app-menu-create', 'aside menu .create', true)
    .register('prompts', 'section.prompts', true)
    .register('prompts-canceller', 'section.prompts > .close', true)
    .register('projects-data-table-tbody', 'article.projects table tbody', true)
    .register('entity-form', 'form[data-entity][data-primary]', false);

app.router
    .register('click', 'app-menu-create', ui.prompts.create)
    .register('click', 'prompts-canceller', ui.prompts.hide)
    .register('submit', 'entity-form', controller.handleEntityForm);

app.events
    .addListener('projects-list', ui.project.list);

app.project = null;

$(document).ready(function () {
    app.router.activate();
    app.events.dispatch('projects-list');
});