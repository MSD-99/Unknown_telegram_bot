from types import SimpleNamespace

from src.utils.keyboard import Create_Keyboard

Keys = SimpleNamespace(
    random_connect = ':bust_in_silhouette: Random Connect',
    settings = ':gear: Settings',
)


Keyboards = SimpleNamespace(
    main = Create_Keyboard(Keys.random_connect, Keys.settings),
)
