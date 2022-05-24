import tkinter
from tkinter import *
from tkinter import ttk

from domain.aggregates import Config
from domain.ports import ConfigSetterInterfacePort
from infrastructure.adapters.tkinter_config_setter_interface.validations import validate_integer, validate_money, \
    validate_float


class TkinterConfigSetterInterfaceAdapter(ConfigSetterInterfacePort):
    __PADDING = 10
    __root: Tk
    __main_frame: ttk.Frame
    __parameters_frame: ttk.Frame
    __ok_button_frame: ttk.Frame
    __parameters_count: int
    __integer_validation: (str, str)
    __float_validation: (str, str)
    __money_validation: (str, str)
    __seconds_between_actions: tkinter.StringVar
    __starting_bet: tkinter.StringVar
    __martingale_multiplier: tkinter.StringVar
    __max_martingales: tkinter.StringVar
    __reset_after_max_martingales: tkinter.BooleanVar
    __default_config: Config
    __result_config: Config = None

    def __init__(self, default_config: Config) -> None:
        self.__parameters_count = 0
        self.__default_config = default_config

    def prompt_user_config(self) -> Config:
        self.__build()
        self.__run()
        return self.__result_config

    def __build(self) -> None:
        self.__create_root()
        self.__create_parameter_variables()
        self.__set_default_values()
        self.__register_validations()
        self.__create_frames()
        self.__create_parameters()
        self.__create_ok_button()

    def __create_parameter_variables(self) -> None:
        self.__seconds_between_actions = tkinter.StringVar()
        self.__starting_bet = tkinter.StringVar()
        self.__martingale_multiplier = tkinter.StringVar()
        self.__max_martingales = tkinter.StringVar()
        self.__reset_after_max_martingales = tkinter.BooleanVar()

    def __set_default_values(self) -> None:
        self.__seconds_between_actions.set(self.__default_config.seconds_between_actions.to_string())
        self.__starting_bet.set(self.__default_config.starting_bet.to_string())
        self.__martingale_multiplier.set(self.__default_config.martingale_multiplier.to_string())
        self.__max_martingales.set(self.__default_config.max_martingales.to_string())
        self.__reset_after_max_martingales.set(self.__default_config.reset_after_max_martingales)

    def __create_root(self) -> None:
        self.__root = Tk()
        self.__root.title('Configurações')

    def __register_validations(self) -> None:
        self.__integer_validation = (self.__root.register(validate_integer), '%P')
        self.__money_validation = (self.__root.register(validate_money), '%P')
        self.__float_validation = (self.__root.register(validate_float), '%P')

    def __create_frames(self) -> None:
        self.__main_frame = ttk.Frame(
            master=self.__root,
            padding=self.__PADDING
        )
        self.__main_frame.grid()
        self.__parameters_frame = ttk.Frame(
            master=self.__main_frame
        )
        self.__parameters_frame.grid()
        self.__ok_button_frame = ttk.Frame(
            master=self.__main_frame
        )
        self.__ok_button_frame.grid()

    def __create_parameters(self) -> None:
        self.__create_entry_parameter(
            text='Segundos entre ações',
            validation_command=self.__float_validation,
            variable=self.__seconds_between_actions
        )
        self.__create_entry_parameter(
            text='Aposta inicial',
            validation_command=self.__money_validation,
            variable=self.__starting_bet
        )
        self.__create_entry_parameter(
            text='Multiplicador Martingale',
            validation_command=self.__float_validation,
            variable=self.__martingale_multiplier
        )
        self.__create_entry_parameter(
            text='Limite de vezes do Martigale',
            validation_command=self.__integer_validation,
            variable=self.__max_martingales
        )
        self.__create_checkbox_parameter(
            text='Resetar ao passar do limite',
            variable=self.__reset_after_max_martingales
        )

    def __create_entry_parameter(
            self,
            text: str,
            validation_command: (str, str),
            variable: tkinter.StringVar
    ) -> None:
        self.__create_parameter_label(
            text=text,
            column=0,
            row=self.__parameters_count
        )
        self.__create_parameter_entry(
            column=1,
            row=self.__parameters_count,
            validation_command=validation_command,
            variable=variable
        )
        self.__parameters_count += 1

    def __create_parameter_label(
            self,
            text: str,
            column: int,
            row: int
    ) -> None:
        ttk.Label(
            master=self.__parameters_frame,
            text=text,
            font=('Arial', 10),
            padding=2,
            anchor='e'
        ).grid(
            column=column,
            row=row
        )

    def __create_parameter_entry(
            self,
            column: int,
            row: int,
            validation_command: (str, str),
            variable: tkinter.Variable
    ) -> None:
        Entry(
            master=self.__parameters_frame,
            validate='key',
            validatecommand=validation_command,
            textvariable=variable
        ).grid(
            column=column,
            row=row
        )

    def __create_checkbox_parameter(
            self,
            text: str,
            variable: tkinter.BooleanVar
    ) -> None:
        self.__create_parameter_label(
            text=text,
            column=0,
            row=self.__parameters_count
        )
        ttk.Checkbutton(
            master=self.__parameters_frame,
            takefocus=False,
            variable=variable
        ).grid(
            column=1,
            row=self.__parameters_count
        )
        self.__parameters_count += 1

    def __create_ok_button(self) -> None:
        ttk.Button(
            master=self.__ok_button_frame,
            text='OK'
        ).grid(
            column=0,
            row=0
        )

    def __press_ok_button(self) -> None:
        pass

    def __run(self) -> None:
        self.__root.mainloop()


t = TkinterConfigSetterInterfaceAdapter(Config())
t.prompt_user_config()
