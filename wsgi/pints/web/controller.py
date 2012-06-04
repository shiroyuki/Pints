from tori.controller import ErrorController as BaseErrorController
from tori.decorator  import controller as c

from pints.base.controller import Controller
from pints.security.model  import User

@c.custom_error('error.html')
@c.renderer('pints.web.view')
class ErrorController(Controller, BaseErrorController):
    ''' Based on https://gist.github.com/398252 '''

@c.custom_error('error.html')
@c.renderer('pints.web.view')
class IndexController(Controller):
    def get(self):
        if not self.authenticated():
            return self.redirect('/login')
        
        self.render('app.html')

@c.custom_error('error.html')
@c.renderer('pints.web.view')
class SessionController(Controller):
    access_control = None
    
    def get(self, path):
        if path == 'login' and not self.authenticated():
            return self.render('login.html')
        
        if path == 'logout':
            self.delete_session('user')
        
        self.redirect('/')
    
    def post(self, path):
        if path != 'session':
            return self.set_status(405)
        
        if self.authenticated():
            return self.set_status(403)
        
        if 'key' not in self.params or 'password' not in self.params:
            return self.set_status(400)
        
        if not self.access_control:
            self.access_control = self.component('security.access_control')
        
        user = self.access_control.authenticate(self.params['key'], self.params['password'])
        
        if not user:
            return self.set_status(401)
        
        self.session('user', user)
        self.set_status(200)
