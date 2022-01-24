import pyaww

client = pyaww.user.User("...", "...")

my_webapp = pyaww.WebApp(
    {
        "id": 123,
        "user": "sampleuser",
        "domain_name": "something.com",
        "python_version": "3.8",
        "source_directory": "/home/something/",
        "working_directory": "/home/something/",
        "virtualenv_path": "/home/something/venv",
        "expiry": "some date",
        "force_https": False,
    },
    client,
)
