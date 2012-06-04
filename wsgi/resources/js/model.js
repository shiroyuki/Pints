function User(params) {
    this.attributes = {
        id:    null,
        alias: null,
        name:  null,
        email: null
    };
}

Class.extend(User, DataModel);

function Project() {
    this.attributes = {
        id:          null,
        codename:    null,
        name:        null,
        owner:       null,
        description: null,
        created:     null,
        updated:     null,
        active:      true,
        milestones:  [],
        inbox:       [],    // where the reminders with no milestones are
        dropbox:     []     // where the reminders with no milestones are
    };
}

Class.extend(Project, DataModel);

function Milestone() {
    this.attributes = {
        id:        null,
        name:      null,
        created:   null,
        updated:   null,
        due:       null,
        active:    true,
        reminders: {}
    };
}

Class.extend(Milestone, DataModel);

function Reminder() {
    this.attributes = {
        id:          null,
        owner:       null,
        assignees:   [],
        responders:  [],
        alias:       [],
        summary:     null,
        description: null,
        created:     null,
        updated:     null,
        due:         null,
        active:      false,
        complete:    false
    };
}

Class.extend(Reminder, DataModel);