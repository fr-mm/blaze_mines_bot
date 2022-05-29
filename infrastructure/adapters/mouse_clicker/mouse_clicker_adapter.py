import mouse

from domain.ports import ClickerPort
from domain.value_objects import ScreenRegion, Coordinates


class MouseClickerAdapter(ClickerPort):
    def click_on_coordinates(self, coordinates: Coordinates) -> None:
        mouse.move(x=coordinates.x, y=coordinates.y)
        mouse.click()

    def click_on_screen_region(self, screen_region: ScreenRegion) -> None:
        coordinates = self.__get_screen_region_center(screen_region)
        self.click_on_coordinates(coordinates)

    def __get_screen_region_center(self, screen_region: ScreenRegion) -> Coordinates:
        x = self.__get_middle_point(screen_region.top_left.x, screen_region.bottom_right.x)
        y = self.__get_middle_point(screen_region.top_left.y, screen_region.bottom_right.y)
        return Coordinates(x, y)

    @staticmethod
    def __get_middle_point(point_a: int, point_b: int) -> int:
        return round((point_a + point_b) / 2)
