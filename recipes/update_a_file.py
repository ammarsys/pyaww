import pyaww

client = pyaww.User(..., ...)


async def update_file(path: str) -> None:
    file = await client.get_file_by_path(path)

    with open("supersecretdocument.txt", "r+") as f:
        await file.update(f)
