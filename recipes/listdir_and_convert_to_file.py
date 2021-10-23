import pyaww

client = pyaww.user.User("...", "...")

data = client.listdir("/home/mysite/")
files = [client.get_file_by_path(path) for path in data]
# or
files = [pyaww.file.File(path, client) for path in data]
