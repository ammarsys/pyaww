from pyaww.webapp import WebApp

my_webapp = WebApp(
    {'id': 123,
     'user': 'sampleuser',
     'domain_name': 'something.com',
     'python_version': '3.8',
     'source_directory': '/home/something/',
     'working_directory': '/home/something/',
     'virtualenv_path': '/home/something/venv',
     'expiry': 'some date',
     'force_https': False
     }
)
# do stuff with the webapp object now
