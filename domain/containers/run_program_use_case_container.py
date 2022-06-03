from dataclasses import dataclass

from domain.services import PrinterService
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    LocateImageInScreenUseCasePort
from domain.value_objects import CheckForImageOnSquareMaxTries


@dataclass(frozen=True)
class RunProgramUseCaseContainer:
    clicker: ClickerPort
    typer: TyperPort
    keyboard_listener: KeyboardListenerPort
    screen_reader: ScreenReaderPort
    config_setter_interface: ConfigSetterInterfacePort
    locate_image_in_screen_service: LocateImageInScreenUseCasePort
    check_for_image_on_square_max_tries: CheckForImageOnSquareMaxTries
    printer: PrinterService
