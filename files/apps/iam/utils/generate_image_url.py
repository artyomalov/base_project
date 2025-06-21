from config import settings


def generate_image_url(
    image_type: str,
    image_name: str,
) -> str:
    return f"{settings.media_url}/{image_type}/{image_name}"
