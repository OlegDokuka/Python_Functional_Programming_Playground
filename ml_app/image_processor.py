import dataclasses
from typing import Iterable, AsyncGenerator

from ml_app.image_fetcher import Image


async def process_image() -> AsyncGenerator[Image, Image]:
