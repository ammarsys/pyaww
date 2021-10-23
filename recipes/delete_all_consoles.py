import pyaww

client = pyaww.user.User("...", "...")

consoles = client.consoles()
for console in consoles["personal"]:
    print(f"deleting console with the name {console.name}...")
    console.delete()
