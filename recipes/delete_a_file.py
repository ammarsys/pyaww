import pyaww

client = pyaww.User("...", "...")


async def delete_file_by_path(path: str) -> None:
    file = await client.get_file_by_path(path)
    await file.delete()
