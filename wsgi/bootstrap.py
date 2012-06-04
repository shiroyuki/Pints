''' App bootstrap '''

from os.path import abspath, dirname, join
from sys     import argv, path

is_production = len(argv) > 1 and 'production' in argv or False

app_path = dirname(abspath(__file__))

def load_dependencies():
    required_modules = ['Kotoba', 'Imagination', 'Tori']
    base_mod_path    = abspath(join(
        app_path,
        (is_production and 'lib' or '../..')
    ))

    for required_module in required_modules:
        mod_path = join(base_mod_path, required_module)
        path.append(mod_path)

if is_production:
    load_dependencies()
