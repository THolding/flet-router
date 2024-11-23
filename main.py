import flet as ft
from os import path

from pop_culture_ui import PopCultureUI


popCultureDir = path.abspath(path.join("..", "PopCulture-dummy"))

appInstance = PopCultureUI(popCultureDir)
ft.app(appInstance.main)
