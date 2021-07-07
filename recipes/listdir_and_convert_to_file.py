from pyaww.file import File

data = client.listdir('/home/mysite/')
data = [client.get_file_by_path(path) for path in data]
# or
data = [File(path, client) for path in data]
   
