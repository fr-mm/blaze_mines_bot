import time
from domain.ports import ScreenReaderPort
from domain.sets import ImagePathSet
from domain.value_objects import ImagePath, ScreenRegion
from infrastructure.adapters.opencv_mss_screen_reader.mss_screenshooter import MssScreenshooter
from infrastructure.adapters.opencv_mss_screen_reader.opencv_template_matcher import OpencvTemplateMatcher


class OpencvMssScreenReaderAdapter(ScreenReaderPort):
    __screenshooter: MssScreenshooter
    __template_matcher: OpencvTemplateMatcher

    def __init__(self) -> None:
        self.__screenshooter = MssScreenshooter()
        self.__template_matcher = OpencvTemplateMatcher()

    def get_image_location(self, image_path: ImagePath) -> ScreenRegion:
        screenshot = self.__screenshooter.take_full_screenshot()
        return self.__template_matcher.locate_template_in_screenshot(
            template=image_path,
            screenshot=screenshot
        )

    def image_is_in_region(self, image_path: ImagePath, screen_region: ScreenRegion) -> bool:
        screenshot = self.__screenshooter.take_screenshot_from_region(screen_region)
        return self.__template_matcher.template_is_in_screenshot(
            template=image_path,
            screenshot=screenshot
        )


if __name__ == '__main__':
    time.sleep(1)
    o = OpencvMssScreenReaderAdapter()
    o.get_image_location(ImagePathSet.BOMB)
