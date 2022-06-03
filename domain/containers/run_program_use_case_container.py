from dataclasses import dataclass

from domain.services import PrinterService
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    GetImageScreenRegionUseCasePort
from domain.value_objects import CheckForImageOnSquareMaxTries


@dataclass(frozen=True)
class RunProgramUseCaseContainer:
    clicker: ClickerPort
    typer: TyperPort
    keyboard_listener: KeyboardListenerPort
    screen_reader: ScreenReaderPort
    config_setter_interface: ConfigSetterInterfacePort
    get_image_screen_region_service: GetImageScreenRegionUseCasePort
    check_for_image_on_square_max_tries: CheckForImageOnSquareMaxTries
    printer: PrinterService
