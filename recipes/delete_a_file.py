import pyaww

client = pyaww.user.User("...", "...")

file = client.get_file_by_path("/home/yourname/yoursite/somefile.py")
file.delete()
