from datetime import datetime
from random   import randint
from time     import time

from sqlalchemy     import Boolean, Column, DateTime, event, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship, backref
from tori.common    import Enigma
from tori.rdb       import Entity

from pints.security.model import User

jointed_table_project_reminder = Table('project_reminder', Entity.metadata,
    Column('project_id', Integer, ForeignKey('groups.id')),
    Column('reminder_id', Integer, ForeignKey('users.id'))
)

class SingleKeyModel(object):
    id          = Column(Integer, primary_key=True)
    description = Column(Text, index=True, nullable=True)
    created     = Column(DateTime(True), index=True, default=datetime.utcnow)
    updated     = Column(DateTime(True), index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    due         = Column(DateTime(True), index=True, nullable=True)
    active      = Column(Boolean, default=True)
    complete    = Column(Boolean, default=False)

class Project(Entity, SingleKeyModel):
    __tablename__ = 'projects'

    name       = Column(String(80), index=True)
    codename   = Column(String(80), index=True)
    milestones = None
    dropbox    = None # the list of reminders without milestones
    
    # Many projects to one owner (user)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner    = relationship('User')

class Reminder(Entity, SingleKeyModel):
    __tablename__ = 'reminders'
    
    assignees  = []
    responders = []
    summary    = Column(String(80), index=True)
    alias      = Column(String(80), index=True)
    
    # Many projects to one owner (user)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner    = relationship('User')

def post_commit_listener(entity, value, oldvalue, initiator):
    if value:
        entity.updated = datetime.utcnow()
    else:
        entity.updated = None
    
    return value

event.listen(Project.complete, 'set', post_commit_listener, retval=True)
event.listen(Reminder.complete, 'set', post_commit_listener, retval=True)
