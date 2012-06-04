var app = {
    user:     null,
    selector: new SelectorLoader(),
    router:   new Router(),
    events:   new EventControl(),
    repositories: new DataRepositoryManager()
};

app.router.setSelectorManager(app.selector);