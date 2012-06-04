from datetime import datetime
from re       import compile as RegExp
from tori.rdb import Entity

class DataTransformer(object):
    re_integer  = RegExp('^\d+$')
    re_float    = RegExp('^\d*\.\d+$')
    re_datetime = RegExp('^\d{4}\.\d{2}\.\d{2}')
    
    def simplify(self, request_arguments):
        arguments = {}
        
        for name, data in request_arguments.iteritems():
            data = len(data) == 1 and data[0] or data
            
            if data.lower() in ['true', 'false']:
                data = data == 'true'
            elif self.re_integer.search(data):
                data = int(data)
            elif self.re_float.search(data):
                data = float(data)
            elif self.re_datetime.search(data):
                try:
                    data = datetime.strptime(data, '%Y.%m.%d %H:%M:%S %z')
                except ValueError:
                    data = datetime.strptime(data, '%Y.%m.%d %H:%M:%S')
            
            arguments[name] = data
        
        return arguments
    
    def convert_entity_to_dict(self, entity):
        converted_content = {
            '_kind': entity.__class__.__name__
        }
        
        for name in dir(entity):
            if name[0] == '_' or name == 'metadata':
                continue
            
            content = entity.__getattribute__(name)
            
            if callable(content):
                continue
            
            if isinstance(content, datetime):
                converted_content[name] = content.strftime('%Y.%m.%d %H:%M:%S %z').strip()
            elif isinstance(content, Entity):
                converted_content[name] = self.convert_entity_to_dict(content)
            else:
                converted_content[name] = content
        
        return converted_content
