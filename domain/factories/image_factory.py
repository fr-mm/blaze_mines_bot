from domain.entities import Image
from domain.value_objects import ScreenRegion, ImageName, ImagePath


class ImageFactory:
    @staticmethod
    def build(
            name: str,
            path: str,
            location: ScreenRegion = None
    ) -> Image:
        return Image(
            name=ImageName(f'"{name}"'),
            path=ImagePath(path),
            location=location
        )
