from dataclasses import dataclass

from domain.services import PrinterService
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    LocateImageInScreenUseCasePort, ClickOnImageUseCasePort


@dataclass(frozen=True)
class RunProgramUseCaseContainer:
    clicker: ClickerPort
    typer: TyperPort
    keyboard_listener: KeyboardListenerPort
    screen_reader: ScreenReaderPort
    printer: PrinterService
    config_setter_interface: ConfigSetterInterfacePort
    locate_image_in_screen_service: LocateImageInScreenUseCasePort
    click_on_image_service: ClickOnImageUseCasePort
