import flet as ft

class Router:
    def __init__(self, firstRouteContext, page: ft.Page):
        self.page = page
        self.routeContexts = [firstRouteContext]
        self.routeHistory = []

    def go(self, route: str):
        print("Routing to: ", route)
        self.routeHistory.append(route)
        self._do_routing()
        self.page.update()
    
    #Convenience function which prepends the current route context's root route to the route
    def go_relative(self, subroute: str):
        route = self.routeContexts[-1].rootRoute+subroute
        self.go(route)

    def go_back(self):
        if len(self.routeHistory) == 1:
            print("Warning: Trying to route back but there is no previous routes.")
            return
        
        self.routeHistory.pop()
        if not self.routeContexts[-1].can_match(self.routeHistory[-1]):
            #This previous route must have been handled by the previous route context, so pop the current one
            self.routeContexts.pop()
            #Also pop the view, since each there is a one-to-one mapping between views and route contexts
            self.page.views.pop()
        
        self._do_routing()
        self.page.update()
    
    #Routes to the top route in route history using the top route context
    def _do_routing(self):
        if self.routeContexts[-1].can_match(self.routeHistory[-1]) == False:
            raise RuntimeError("Trying to route to '"+self.routeHistory[-1]+"' but this route cannot be matched by the current route context.")
        subroute = self.get_subroute(self.routeHistory[-1])
        self.routeContexts[-1].routeTable[subroute]()
    
    #Handles a change in router context. Handled here so that
    def new_route_context(self, newRouteContext):
        if self.routeContexts[-1] == newRouteContext:
            print("Warning: Trying to add new route context which is the same instance as the current route context.")
        self.routeContexts.append(newRouteContext)
        self._do_routing() #Note: route should already be added to the history
    
    def get_subroute(self, route: str) -> str:
        if not route.startswith(self.routeContexts[-1].rootRoute):
            raise RuntimeError("Can't get subroute from a route which doesn't have the current root route")
        else:
            return route[len(self.routeContexts[-1].rootRoute):]



###TODO: generatic route context
class RouteContext:
    def __init__(self, routerInstance: Router, WrappedViewType: ft.View, routeTable: dict):
        pass




class PopCultureUIRouteContext(RouteContext):
    def __init__(self, popCultureAppInstance, routerInstance: Router, WrappedViewType: ft.View, routeTable: dict):
        super().__init__(routerInstance, WrappedViewType, routeTable)
        self.appInstance = popCultureAppInstance