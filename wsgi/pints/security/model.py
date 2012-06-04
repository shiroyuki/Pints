from random import randint
from time   import time

from sqlalchemy     import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
from tori.common    import Enigma
from tori.rdb       import Entity

class AuthenticationToken(object):
    def __init__(self, id, alias, email, secret, firstname, lastname):
        self.id        = id
        self.alias     = alias
        self.email     = email
        self.secret    = secret
        self.firstname = firstname
        self.lastname  = lastname

class GroupUserManagementLevel(object):
    labels = ['member', 'staff', 'master']

    member = 0
    staff  = 1
    master = 2

class UserStatus(object):
    inactive = 0
    active   = 1
    disabled = 2

class GroupUserManagement(Entity):
    __tablename__ = 'group_user_management'
    
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    user_id  = Column(Integer, ForeignKey('users.id'), primary_key=True)
    level    = Column(Integer)

jointed_table_group_user = Table('group_user', Entity.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Group(Entity):
    __tablename__ = 'groups'

    id    = Column(Integer, primary_key=True)
    name  = Column(String(50), index=True)
    alias = Column(String(50), unique=True, index=True)
    users = relationship('User', secondary=jointed_table_group_user, backref='groups')

class User(Entity):
    __tablename__ = 'users'

    id     = Column(Integer, primary_key=True)
    
    # Security / Access Control
    email  = Column(String(50), index=True)
    hash   = Column(String(50)) # sha512(given password + salt)
    salt   = Column(String(50)) # sha512(unix timestamp + random number)
    secret = Column(String(50)) # sha512(this email + salt)
    status = Column(Integer)
    
    # Personal Information
    alias     = Column(String(20), unique=True, index=True)
    firstname = Column(String(50), index=True, nullable=True)
    lastname  = Column(String(50), index=True, nullable=True)

    def set_password(self, password):
        self.hash = Enigma.instance().hash('%s %s' % (password, self.salt))
