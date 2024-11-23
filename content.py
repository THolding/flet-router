import flet as ft


class IndexViewRouteContext:
    def __init__(self, appInstance, rootRoute: str):
        self.appInstance = appInstance
        self.rootRoute = rootRoute
        self.routeTable = {"/": lambda : self.go_panel(self.viewInstance.build_first_panel),
                           "/second": lambda : self.go_panel(self.viewInstance.build_second_panel),
                           "/third": lambda : self.go_panel(self.viewInstance.build_third_panel),
                           "/about": lambda : self.go_new_view(AboutViewRouteContext(self.appInstance, self.rootRoute+"/about")),
                           }
        self.viewInstance = IndexView(self.appInstance)
    
    def can_match(self, route:str):
        if route.startswith(self.rootRoute):
            if route[len(self.rootRoute):] in self.routeTable:
                return True
        return False

    def set_active_if_view_not_active(self):
        if self.appInstance.get_current_view() != self.viewInstance:
            self.appInstance.push_back_view(self.viewInstance)

    def go_panel(self, build_func:callable):
        self.set_active_if_view_not_active()
        build_func()
    
    def go_new_view(self, newRouteContext):
        self.appInstance.router.new_route_context(newRouteContext)




class IndexView(ft.View):
    def __init__(self, appInstance):
        super().__init__()
        self.appInstance = appInstance
    

    def add_index_view_title(self):
        self.controls.append(ft.Text("==This is the index view=="))
        self.controls.append(ft.Row([ft.TextButton(text="go first", on_click=lambda _: self.appInstance.router.go_relative("/")),
                                     ft.TextButton(text="go second", on_click=lambda _: self.appInstance.router.go_relative("/second")),
                                     ft.TextButton(text="go third", on_click=lambda _: self.appInstance.router.go_relative("/third")),
                                     ft.TextButton(text="go about view", on_click=lambda _: self.appInstance.router.go_relative("/about")),
                                     ]))
    
    def add_back_button(self):
        self.controls.append(ft.TextButton(text="go back?", on_click=lambda _: self.appInstance.router.go_back()))


    def build_first_panel(self):
        self.controls.clear()
        self.add_index_view_title()
        self.controls.append(ft.Text("These are the index (first) controls"))
        self.add_back_button()

    def build_second_panel(self):
        self.controls.clear()
        self.add_index_view_title()
        self.controls.append(ft.Text("These are the index (second) controls"))
        self.add_back_button()

    def build_third_panel(self):
        self.controls.clear()
        self.add_index_view_title()
        self.controls.append(ft.Text("These are the index (third) controls"))
        self.add_back_button()


class AboutViewRouteContext:
    def __init__(self, appInstance, rootRoute: str):
        self.appInstance = appInstance
        self.rootRoute = rootRoute
        self.routeTable = {"": lambda : self.go_panel(self.viewInstance.build_controls),
                           "/version": lambda : self.go_panel(self.viewInstance.build_version_controls),
                           }
        self.viewInstance = AboutView(appInstance)
    
    def can_match(self, route:str):
        if route.startswith(self.rootRoute):
            if route[len(self.rootRoute):] in self.routeTable:
                return True
        return False

    def set_active_if_view_not_active(self):
        if self.appInstance.get_current_view() != self.viewInstance:
            self.appInstance.push_back_view(self.viewInstance)

    def go_panel(self, build_func:callable):
        self.set_active_if_view_not_active()
        build_func()
    
    def go_new_view(self, newRouteContext):
        self.appInstance.router.new_route_context(newRouteContext)


class AboutView(ft.View):
    def __init__(self, appInstance):
        super().__init__()
        self.appInstance = appInstance
    
    def build_back_button(self):
        self.controls.append(ft.TextButton(text="go back?", on_click=lambda _: self.appInstance.router.go_back()))

    def build_controls(self):
        self.controls.clear()
        self.controls.append(ft.Text("==About=="))
        self.controls.append(ft.TextButton("View version number", on_click=lambda _: self.appInstance.router.go_relative("/version")))
        self.build_back_button()
    
    def build_version_controls(self):
        self.controls.clear()
        self.controls.append(ft.Text("==About=="))
        self.controls.append(ft.Text("version = 0.0.1"))
        self.build_back_button()