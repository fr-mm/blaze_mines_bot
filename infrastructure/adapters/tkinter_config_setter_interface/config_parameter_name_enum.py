from enum import Enum


class ConfigParameterNameEnum(Enum):
    SECONDS_BETWEEN_ACTIONS = 'Segundos entre ações'
    STARTING_BET = 'Aposta inicial'
    MARTINGALE_MULTIPLIER = 'Multiplicador Martingale'
    MAX_MARTINGALES = 'Limite de vezes do Martingale'
    RESET_AFTER_MAX_MARTINGALES = 'Resetar ao passar do limite'
