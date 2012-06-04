from os.path  import abspath, dirname, join as path_join
from unittest import TestCase

from imagination.locator import Locator
from tori.service.rdb    import RelationalDatabaseService as DatabaseService

from pints.security.model         import Group, User, GroupUserManagement, GroupUserManagementLevel
from pints.foundation.initializer import Initializer

class TestFoundationInitializer(TestCase):
    def setUp(self):
        self.base_path = abspath(path_join(dirname(__file__), '../..'))
    
    def test_foundation_initializer_ok(self):
        db = DatabaseService()
        it = Initializer(db)
        p = path_join(self.base_path, 'config/initial_directory.xml')
        
        entities = it.load(p)
        
        self.assertEquals(len(entities), 6, '6 entities added')
        
        for entity in entities:
            self.assertTrue(entity.id is not None, 'Entity %s of class %s should be registered' % (entity.alias, entity.__class__))