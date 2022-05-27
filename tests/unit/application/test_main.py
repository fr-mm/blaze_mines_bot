from unittest import TestCase

from mockito import unstub, when, verify

from application import Main
from domain.use_cases.run_program_use_case import RunProgramUseCase


class TestMain(TestCase):
    def tearDown(self) -> None:
        unstub()

    def test_init_WHEN_called_THEN_returns_instance(self) -> None:
        Main()

    def test_run_WHEN_called_THEN_calls_run_program_service_execute(self) -> None:
        when(RunProgramUseCase).execute()
        main = Main()

        main.run()

        verify(RunProgramUseCase).execute()
