import flet as ft
from os import path

from router import Router
from content import IndexViewRouteContext

class ExampleApp:
	def __init__(self):
		pass
		
	def main(self, page: ft.Page):
		self.router = Router(page)
		self.router.set_initial_route_context(IndexViewRouteContext(self.router, ""))
		self.router.go("/")
	

appInstance = ExampleApp()
ft.app(appInstance.main)
