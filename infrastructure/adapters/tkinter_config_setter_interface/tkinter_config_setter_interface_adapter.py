import tkinter
from tkinter import *
from tkinter import ttk
from typing import List
from tkinter import messagebox

from domain.aggregates import Config
from domain.exceptions import SecondsException, MoneyException, MartingaleMultiplierException, MaxMartingalesException
from domain.ports import ConfigSetterInterfacePort
from domain.value_objects import Seconds, Money, MartingaleMultiplier, MaxMartingales
from infrastructure.adapters.tkinter_config_setter_interface.config_parameter_name_enum import ConfigParameterNameEnum
from infrastructure.adapters.tkinter_config_setter_interface.user_entry_formatter import UserEntryFormatter
from infrastructure.adapters.tkinter_config_setter_interface.validations import validate_integer, validate_money, \
    validate_float


class TkinterConfigSetterInterfaceAdapter(ConfigSetterInterfacePort):
    __FONT = ('Arial', 10)
    __root: Tk
    __confirmation_window: Tk
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
    __final_config: Config = None

    def __init__(self, default_config: Config) -> None:
        self.__parameters_count = 0
        self.__default_config = default_config

    def prompt_user_config(self) -> Config:
        self.__build()
        self.__run()
        return self.__final_config

    def __run(self) -> None:
        self.__root.mainloop()

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
            padding=10
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
            text=ConfigParameterNameEnum.SECONDS_BETWEEN_ACTIONS.value,
            validation_command=self.__float_validation,
            variable=self.__seconds_between_actions
        )
        self.__create_entry_parameter(
            text=ConfigParameterNameEnum.STARTING_BET.value,
            validation_command=self.__money_validation,
            variable=self.__starting_bet
        )
        self.__create_entry_parameter(
            text=ConfigParameterNameEnum.MARTINGALE_MULTIPLIER.value,
            validation_command=self.__float_validation,
            variable=self.__martingale_multiplier
        )
        self.__create_entry_parameter(
            text=ConfigParameterNameEnum.MAX_MARTINGALES.value,
            validation_command=self.__integer_validation,
            variable=self.__max_martingales
        )
        self.__create_checkbox_parameter(
            text=ConfigParameterNameEnum.RESET_AFTER_MAX_MARTINGALES.value,
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
            font=self.__FONT,
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
            text='OK',
            command=self.__press_ok_button
        ).grid(
            column=0,
            row=0
        )

    def __press_ok_button(self) -> None:
        self.__format_user_entries()
        invalid_entries_messages = self.__get_invalid_entries_messages()
        if invalid_entries_messages:
            self.__show_invalid_entries_messages(invalid_entries_messages)
        else:
            self.__open_config_confirmation_window()

    def __format_user_entries(self) -> None:
        user_entry_formatter = UserEntryFormatter()

        seconds_between_actions = user_entry_formatter.format_as_float(self.__seconds_between_actions.get())
        starting_bet = user_entry_formatter.format_as_money(self.__starting_bet.get())
        martingale_multiplier = user_entry_formatter.format_as_float(self.__martingale_multiplier.get())
        max_martingales = user_entry_formatter.format_as_integer(self.__max_martingales.get())

        self.__seconds_between_actions.set(seconds_between_actions)
        self.__starting_bet.set(starting_bet)
        self.__martingale_multiplier.set(martingale_multiplier)
        self.__max_martingales.set(max_martingales)

    def __get_invalid_entries_messages(self) -> List[str]:
        invalid_entries_messages = []

        try:
            Seconds.from_string(self.__seconds_between_actions.get())
        except SecondsException:
            invalid_entries_messages.append(ConfigParameterNameEnum.SECONDS_BETWEEN_ACTIONS.value)

        try:
            Money.from_string(self.__starting_bet.get())
        except MoneyException:
            invalid_entries_messages.append(ConfigParameterNameEnum.STARTING_BET.value)

        try:
            MartingaleMultiplier.from_string(self.__martingale_multiplier.get())
        except MartingaleMultiplierException:
            invalid_entries_messages.append(ConfigParameterNameEnum.MARTINGALE_MULTIPLIER.value)

        try:
            MaxMartingales.from_string(self.__max_martingales.get())
        except MaxMartingalesException:
            invalid_entries_messages.append(ConfigParameterNameEnum.MAX_MARTINGALES.value)

        return invalid_entries_messages

    @staticmethod
    def __show_invalid_entries_messages(invalid_entries_messages: List[str]) -> None:
        message = '\n'.join(invalid_entries_messages)
        messagebox.showinfo(
            title='Campos inválidos',
            message=message
        )

    def __create_final_config(self) -> Config:
        return Config(
            seconds_between_actions=Seconds.from_string(self.__seconds_between_actions.get()),
            starting_bet=Money.from_string(self.__starting_bet.get()),
            martingale_multiplier=MartingaleMultiplier.from_string(self.__martingale_multiplier.get()),
            max_martingales=MaxMartingales.from_string(self.__max_martingales.get()),
            reset_after_max_martingales=self.__reset_after_max_martingales.get()
        )

    def __open_config_confirmation_window(self) -> None:
        self.__confirmation_window = Tk()
        self.__confirmation_window.title('Confirmar configurações')
        bool_translation = {
            True: 'sim',
            False: 'não'
        }
        text = f'''
        {ConfigParameterNameEnum.SECONDS_BETWEEN_ACTIONS.value}: {self.__seconds_between_actions.get()}
        {ConfigParameterNameEnum.STARTING_BET.value}: {self.__starting_bet.get()}
        {ConfigParameterNameEnum.MARTINGALE_MULTIPLIER.value}: {self.__martingale_multiplier.get()}
        {ConfigParameterNameEnum.MAX_MARTINGALES.value}: {self.__max_martingales.get()}
        {ConfigParameterNameEnum.RESET_AFTER_MAX_MARTINGALES.value}: {bool_translation[self.__reset_after_max_martingales.get()]}
        '''
        text_frame = ttk.Frame(
            master=self.__confirmation_window,
            padding=10,

        )
        text_frame.grid()
        Label(
            master=text_frame,
            text=text,
            font=self.__FONT
        ).grid(
            column=0,
            row=0
        )
        buttons_frame = ttk.Frame(
            master=self.__confirmation_window,
            padding=10
        )
        buttons_frame.grid()

        ttk.Button(
            master=buttons_frame,
            text='voltar',
            command=self.__refuse_config_confirmation
        ).grid(
            column=1,
            row=0
        )

        ttk.Button(
            master=buttons_frame,
            text='confirmar',
            command=self.__confirm_config
        ).grid(
            column=0,
            row=0
        )

    def __confirm_config(self) -> None:
        self.__final_config = self.__create_final_config()
        self.__confirmation_window.destroy()
        self.__root.destroy()

    def __refuse_config_confirmation(self) -> None:
        self.__confirmation_window.destroy()


if __name__ == '__main__':
    window = TkinterConfigSetterInterfaceAdapter(Config())
    window.prompt_user_config()
