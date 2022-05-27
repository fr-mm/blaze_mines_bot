from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer, GetImageScreenRegionUseCaseContainer
from domain.ports import ScreenReaderPort, ClickerPort, TyperPort, KeyboardListenerPort, ConfigSetterInterfacePort
from domain.use_cases import GetImageScreenRegionUseCase
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

    def run(self) -> None:
        get_image_screen_region_service = self.__build_get_image_screen_region_service()
        run_program_service = self.__build_run_program_service(
            get_image_screen_region_service=get_image_screen_region_service
        )
        run_program_service.execute()

    def __build_run_program_service(
            self,
            get_image_screen_region_service: GetImageScreenRegionUseCase
    ) -> RunProgramUseCase:
        container = RunProgramUseCaseContainer(
            clicker=self.__clicker,
            typer=self.__typer,
            keyboard_listener=self.__keyboard_listener,
            screen_reader=self.__screen_reader,
            config_setter_interface=self.__config_setter_interface,
            get_image_screen_region_service=get_image_screen_region_service,
            check_for_image_on_square_max_tries=CheckForImageOnSquareMaxTries(100)
        )
        return RunProgramUseCase(container)

    def __build_get_image_screen_region_service(self) -> GetImageScreenRegionUseCase:
        container = GetImageScreenRegionUseCaseContainer(
            screen_reader=self.__screen_reader,
            max_tries=LocateImageMaxTries(100)
        )
        return GetImageScreenRegionUseCase(container)
