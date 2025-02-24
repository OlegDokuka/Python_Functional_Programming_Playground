import dataclasses
from typing import Iterable, AsyncGenerator


@dataclasses.dataclass
class Image:
    image_path: str
    data: bytes

async def fetch_image(image_path: str) -> Image:
    pass

async def fetch_images(images: Iterable[str]) -> AsyncGenerator[Image]:
    for image in images:
        yield await fetch_image(image)