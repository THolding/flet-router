import flet as ft
from os import path

from router import Router
from content import IndexViewRouteContext

class PopCultureUI:
	def __init__(self, popCultureRootDir):
		self.popCultureRootDir = popCultureRootDir
		self.schemaDir = path.join(popCultureRootDir, "resources", "schema")
		
	def main(self, page: ft.Page):
		self.page = page
		self.router = Router(IndexViewRouteContext(self, ""), page)
		self.router.go("/")
	
	#One-to-one mapping between route contexts and views. Router calls these when navigation calls for
	# a change of view
	def pop_view(self):
		if len(self.page.views) != 1:
			self.page.views.pop()
	def push_back_view(self, newView):
		self.page.views.append(newView)
	def get_current_view(self):
		return self.page.views[-1]
	