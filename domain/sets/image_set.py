from domain.factories import ImageFactory


class ImageSet:
    START_GAME = ImageFactory.build(
        name='começar jogo',
        path='comecar_jogo.jpg'
    )
    MONEY_SIGN = ImageFactory.build(
        name='campo de aposta',
        path='money_sign.jpg'
    )
    SQUARE = ImageFactory.build(
        name='quadrado',
        path='square.jpg'
    )
    DIAMOND = ImageFactory.build(
        name='diamante',
        path='diamond.jpg'
    )
    BOMB = ImageFactory.build(
        name='bomba',
        path='bomb.jpg'
    )
    WITHDRAW_MONEY = ImageFactory.build(
        name='retirar prêmio',
        path='retirar.jpg'
    )
