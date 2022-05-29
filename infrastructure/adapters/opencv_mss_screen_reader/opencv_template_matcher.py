import cv2
import numpy

from domain.exceptions import ImageNotInScreenException
from domain.value_objects import ImagePath, ScreenRegion, Coordinates
from infrastructure.adapters.opencv_mss_screen_reader.value_objects import Match, MatchValue, MatchLocation, MatchSize


class OpencvTemplateMatcher:
    __THRESHOLD = 0.001
    __METHOD = cv2.TM_SQDIFF_NORMED
    __COLOR = cv2.IMREAD_GRAYSCALE

    def locate_template_in_screenshot(self, template: ImagePath, screenshot: ImagePath) -> ScreenRegion:
        match = self.__get_match(
            template=template,
            screenshot=screenshot
        )
        self.__validate_match(match)
        return self.__get_screen_region(match)

    def template_is_in_screenshot(self, template: ImagePath, screenshot: ImagePath) -> bool:
        try:
            self.locate_template_in_screenshot(
                template=template,
                screenshot=screenshot
            )
            return True
        except ImageNotInScreenException:
            return False

    def __get_match(self, template: ImagePath, screenshot: ImagePath) -> Match:
        parsed_template = self.__read_image(template)
        parsed_screenshot = self.__read_image(screenshot)
        match_data = cv2.matchTemplate(parsed_screenshot, parsed_template, self.__METHOD)
        min_value, max_value, min_location, max_location = cv2.minMaxLoc(match_data)
        size = parsed_template.shape[::-1]
        return Match(
            value=MatchValue(min_value, max_value),
            location=MatchLocation(min_location, max_location),
            size=MatchSize(width=size[0], height=size[1])
        )

    def __read_image(self, image: ImagePath) -> numpy.ndarray:
        return cv2.imread(image.value, self.__COLOR)

    def __validate_match(self, match: Match) -> None:
        if match.value.min > self.__THRESHOLD:
            raise ImageNotInScreenException()

    @staticmethod
    def __get_screen_region(match: Match) -> ScreenRegion:
        top_left_x, top_left_y = match.location.min
        return ScreenRegion(
            top_left=Coordinates(
                x=top_left_x,
                y=top_left_y
            ),
            bottom_right=Coordinates(
                x=top_left_x + match.size.width,
                y=top_left_y + match.size.height
            )
        )
