from uuid import uuid4


def generate_image_uuid_name(image_type: str) -> str:
    return f"{image_type}_{uuid4().hex}"
