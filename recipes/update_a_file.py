file = client.get_file_by_path(...)

with open('supersecretdocument.txt', 'r') as f:
   file.update(f)
