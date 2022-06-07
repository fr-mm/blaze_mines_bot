from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer, LocateImageInScreenUseCaseContainer, \
    ClickOnImageUseCaseContainer, ImageIsInRegionUseCaseContainer
from domain.services import PrinterService
from domain.use_cases import LocateImageInScreenUseCase, ClickOnImageUseCase, ImageIsInRegionUseCase
from domain.use_cases.run_program_use_case import RunProgramUseCase
from infrastructure.adapters import MouseClickerAdapter, KeyboardTyperAdapter, KeyboardKeyboardListenerAdapter, \
    OpencvMssScreenReaderAdapter, TkinterConfigSetterInterfaceAdapter


class Main:
    @staticmethod
    def build_run_program_service() -> RunProgramUseCase:
        clicker = MouseClickerAdapter()
        typer = KeyboardTyperAdapter(
            seconds_between_keystrokes=0.1
        )
        keyboard_listener = KeyboardKeyboardListenerAdapter()
        screen_reader = OpencvMssScreenReaderAdapter()
        config_setter_interface = TkinterConfigSetterInterfaceAdapter(
            default_config=Config()
        )
        printer = PrinterService()
        locate_image_in_screen_service = LocateImageInScreenUseCase(
            container=LocateImageInScreenUseCaseContainer(
                screen_reader=screen_reader,
                printer=printer
            )
        )
        image_is_in_region_service = ImageIsInRegionUseCase(
            container=ImageIsInRegionUseCaseContainer(
                locate_image_in_screen_service=locate_image_in_screen_service,
                screen_reader=screen_reader
            )
        )
        click_on_image_service = ClickOnImageUseCase(
            container=ClickOnImageUseCaseContainer(
                clicker=clicker,
                locate_image_in_screen_service=locate_image_in_screen_service,
                image_is_in_region_service=image_is_in_region_service
            )
        )
        run_program_service = RunProgramUseCase(
            container=RunProgramUseCaseContainer(
                clicker=clicker,
                typer=typer,
                keyboard_listener=keyboard_listener,
                screen_reader=screen_reader,
                printer=printer,
                config_setter_interface=config_setter_interface,
                locate_image_in_screen_service=locate_image_in_screen_service,
                click_on_image_service=click_on_image_service
            )
        )
        return run_program_service

    def run(self) -> None:
        run_program_service = self.build_run_program_service()
        run_program_service.execute()
