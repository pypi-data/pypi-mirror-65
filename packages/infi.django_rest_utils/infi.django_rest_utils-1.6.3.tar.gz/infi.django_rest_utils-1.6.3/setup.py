
SETUP_INFO = dict(
    name = 'infi.django_rest_utils',
    version = '1.6.3',
    author = 'Roy Belio',
    author_email = 'rbelio@infinidat.com',

    url = 'https://github.com/Infinidat/infi.django_rest_utils',
    license = 'BSD',
    description = """Enhancements to django-rest-framework""",
    long_description = """Enhancements to django-rest-framework""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'capacity',
'djangorestframework',
'docopt',
'setuptools',
'unicodecsv',
'future'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': [
'*.html',
'*.js',
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [
'rest_utils = infi.django_rest_utils.rest_utils:rest_utils'
],
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

