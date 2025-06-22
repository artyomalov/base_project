import base64
from io import BytesIO
from PIL import Image
from config import settings
from aiofiles import open as aio_open


async def save_image(path: str, image: memoryview) -> None:
    async with aio_open(path, "wb") as file:
        await file.write(image)


async def save_base64_image_to_fs(
    base64_string: str, path_to_fs_directory: str, image_name: str
) -> None:
    """
    :param base64_string: base64 encoded image
    :param path_to_fs_directory: folder, where image will be saved
    :param image_name: name that will be used to save image
    """

    image_format, image_string = base64_string.split(";base64,")
    image_extension = image_format.split("/")[-1]
    img = Image.open(BytesIO(base64.decodebytes(bytes(image_string, "utf-8"))))
    # media_root = settings.MEDIA_ROOT.read_text()

    buffer = BytesIO()
    img.save(buffer, format="JPEG")

    await save_image(
        path=f"/main_app/files\\media/avatar/'{image_name}'.{image_extension}",
        image=buffer.getbuffer(),
    )
