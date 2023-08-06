
SETUP_INFO = dict(
    name = 'infi.django_http_hooks',
    version = '0.2.5',
    author = 'Itay Galea',
    author_email = 'igalea@infinidat.com',

    url = 'https://github.com/Infinidat/infi.django_http_hooks',
    license = 'BSD',
    description = """a plugin to support sending http requests for any registered model""",
    long_description = """""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'setuptools',
'gevent',
'requests',
'lxml',
'django-admin-list-filter-dropdown'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

