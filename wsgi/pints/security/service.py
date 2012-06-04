from time        import time
from tori.common import Enigma

from pints.security.model import AuthenticationToken, Group, User

class Initialization(object):
    pass

class Registration(object):
    def __init__(self, db):
        self.db = db

    def make_user(self, **data):
        password = 'password' in data and data['password'] or None

        del data['password']

        assert password, 'The password must be provided.'

        u = User(**data)

        u.salt   = self.generate_hash(Enigma.instance().random_number(), time())
        u.secret = self.generate_hash(u.email, u.salt)
        u.hash   = self.generate_hash(password, u.salt)

        return u

    def add_user(self, alias, email, password):
        u = self.make_user(alias=alias, email=email, password=password)

        self.db.post(u)

        return u

    def generate_hash(self, primary_factor, secondary_factor):
        return Enigma.instance().hash('%s %s' % (primary_factor, secondary_factor))

class AccessControl(object):
    def __init__(self, user_directory):
        self.user_directory = user_directory

    def authenticate(self, key, password):
        user = self.user_directory.query().filter_by(email=key).first()

        if user is None:
            return None

        password_hash = self.generate_hash(password, user.salt)

        if user.hash != password_hash:
            return None
        
        return AuthenticationToken(
            user.id,
            user.alias,
            user.email,
            user.secret,
            user.firstname,
            user.lastname
        )

    def generate_hash(self, primary_factor, secondary_factor):
        return Enigma.instance().hash('%s %s' % (primary_factor, secondary_factor))
