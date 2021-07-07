for console in client.consoles():
    print(f'deleting console with the name {console.name}...')
    console.delete()
