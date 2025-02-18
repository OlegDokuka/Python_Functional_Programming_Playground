import dataclasses



@dataclasses.dataclass
class Image:
    image_path: str
    data: bytes

def fetch_image(image_path: str) -> Image:
    pass