''' Server bootstrap '''
from tori.application import Application
from tori.centre      import services

import bootstrap
from pints.foundation.initializer import Initializer

application = Application('config/server.xml')

if not bootstrap.is_production:
    initializer = Initializer(services.get('db'))
    initializer.load('%s/config/initial_directory.xml' % bootstrap.app_path)

application.start()
