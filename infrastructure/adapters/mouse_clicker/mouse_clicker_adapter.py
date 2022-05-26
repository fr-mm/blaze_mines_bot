import mouse

from domain.ports import ClickerPort
from domain.value_objects import ScreenRegion, Coordinates


class MouseClickerAdapter(ClickerPort):
    def click_on_coordinates(self, coordinates: Coordinates) -> None:
        mouse.move(Coordinates.x, Coordinates.y)
        mouse.click()

    def click_on_screen_region(self, screen_region: ScreenRegion) -> None:
        coordinates = self.__get_screen_region_center(screen_region)
        self.click_on_coordinates(coordinates)

    @staticmethod
    def __get_screen_region_center(screen_region: ScreenRegion) -> Coordinates:
        x = screen_region.bottom_right.x - screen_region.top_left.x
        y = screen_region.bottom_right.y - screen_region.top_left.y
        return Coordinates(x, y)
