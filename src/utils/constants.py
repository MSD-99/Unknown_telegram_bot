from types import SimpleNamespace

from src.utils.keyboard import Create_Keyboard

Keys = SimpleNamespace(
    random_connect=':bust_in_silhouette: Random Connect',
    settings=':gear: Settings',
    exit=':cross_mark: Exit'
)


Keyboards = SimpleNamespace(
    main=Create_Keyboard(Keys.random_connect, Keys.settings),
    exit=Create_Keyboard(Keys.exit),
)


States = SimpleNamespace(
    random_connect='RANDOM_CONNECT',
    main="MAIN",
    connected="CONNECTED",
)
