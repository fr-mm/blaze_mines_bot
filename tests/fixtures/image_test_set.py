from domain.factories import ImageFactory


class ImageTestSet:
    START_GAME_NOT_FOUND = ImageFactory.build(
        name='start game not found',
        path='test_comecar_jogo_not_found.jpg'
    )
    MONEY_SIGN_NOT_FOUND = ImageFactory.build(
        name='money sign not found',
        path='test_money_sign_not_found.jpg'
    )
    SQUARE_NOT_FOUND = ImageFactory.build(
        name='square not found',
        path='test_square_not_found.jpg'
    )
    INITIAL_SCREEN = ImageFactory.build(
        name='initial screen',
        path='test_initial_screen.jpg'
    )
    BOMB_AND_DIAMOND = ImageFactory.build(
        name='bomb and diamond',
        path='test_bomb_and_diamond.jpg'
    )
    FULL_SCREENSHOT = ImageFactory.build(
        name='full screenshot',
        path='test_full_screenshot.jpg'
    )
