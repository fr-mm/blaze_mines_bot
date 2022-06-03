from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer, StoreImageScreenRegionUseCaseContainer
from domain.services import PrinterService
from domain.ports import ScreenReaderPort, ClickerPort, TyperPort, KeyboardListenerPort, ConfigSetterInterfacePort, \
    PrinterServicePort
from domain.use_cases import LocateImageInScreenUseCase
from domain.use_cases.run_program_use_case import RunProgramUseCase
from domain.value_objects import LocateImageMaxTries, CheckForImageOnSquareMaxTries
from infrastructure.adapters import MouseClickerAdapter, KeyboardTyperAdapter, KeyboardKeyboardListenerAdapter, \
    OpencvMssScreenReaderAdapter, TkinterConfigSetterInterfaceAdapter


class Main:
    __clicker: ClickerPort
    __typer: TyperPort
    __keyboard_listener: KeyboardListenerPort
    __screen_reader: ScreenReaderPort
    __config_setter_interface: ConfigSetterInterfacePort
    __printer: PrinterServicePort

    def __init__(self) -> None:
        self.__clicker = MouseClickerAdapter()
        self.__typer = KeyboardTyperAdapter(
            seconds_between_keystrokes=0.1
        )
        self.__keyboard_listener = KeyboardKeyboardListenerAdapter()
        self.__screen_reader = OpencvMssScreenReaderAdapter()
        self.__config_setter_interface = TkinterConfigSetterInterfaceAdapter(
            default_config=Config()
        )
        self.__printer = PrinterService()

    def run(self) -> None:
        get_image_screen_region_service = self.__build_get_image_screen_region_service()
        run_program_service = self.__build_run_program_service(
            locate_image_in_screen_service=get_image_screen_region_service
        )
        run_program_service.execute()

    def __build_run_program_service(
            self,
            locate_image_in_screen_service: LocateImageInScreenUseCase
    ) -> RunProgramUseCase:
        container = RunProgramUseCaseContainer(
            clicker=self.__clicker,
            typer=self.__typer,
            keyboard_listener=self.__keyboard_listener,
            screen_reader=self.__screen_reader,
            config_setter_interface=self.__config_setter_interface,
            locate_image_in_screen_service=locate_image_in_screen_service,
            check_for_image_on_square_max_tries=CheckForImageOnSquareMaxTries(100),
            printer=PrinterService()
        )
        return RunProgramUseCase(container)

    def __build_get_image_screen_region_service(self) -> LocateImageInScreenUseCase:
        container = StoreImageScreenRegionUseCaseContainer(
            screen_reader=self.__screen_reader,
            printer=self.__printer
        )
        return LocateImageInScreenUseCase(container)
