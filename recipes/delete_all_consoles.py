import pyaww

client = pyaww.User("...", "...")


async def kill_all_personal_consoles() -> None:
    consoles = await client.consoles()
    for console in consoles:
        print(f"deleting console with the name {console.name}...")
        await console.delete()
