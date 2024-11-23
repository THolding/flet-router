import flet as ft

class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routeHistory = []
        self.routeContexts = []

    def set_initial_route_context(self, firstRouteContext):
         self.routeContexts = [firstRouteContext]
         self.routeHistory = []
    

    def go(self, route: str):
        if len(self.routeContexts) == 0:
            raise RuntimeError("Error: Trying to route to '"+route+"' but no initial route context was set.")
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
            self.pop_view()
        
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
    

    #Convenience function to remove the root route from a route, based on the current route context
    def get_subroute(self, route: str) -> str:
        if not route.startswith(self.routeContexts[-1].rootRoute):
            raise RuntimeError("Can't get subroute from a route which doesn't have the current root route")
        else:
            return route[len(self.routeContexts[-1].rootRoute):]
        
    #One-to-one mapping between route contexts and views. Router calls these when navigation calls for
	# a change of view
    def pop_view(self):
        if len(self.page.views) != 1:
            self.page.views.pop()
    def push_back_view(self, newView):
        self.page.views.append(newView)
    def get_current_view(self):
        return self.page.views[-1]



#Route context performs the mapping between a subroutes (within a single view) and changes to the view's controls
class RouteContext:
    def __init__(self, routerInstance: Router, rootRoute: str, WrappedViewType: ft.View, routeTable: dict):
        self.router = routerInstance
        self.rootRoute = rootRoute
        self.routeTable = routeTable
        #Create the view instance which this route context corresponds to
        self.viewInstance = WrappedViewType(self.router)
    
    def can_match(self, route:str):
        if route.startswith(self.rootRoute):
            if route[len(self.rootRoute):] in self.routeTable:
                return True
        return False

    def set_active_if_view_not_active(self):
        if self.router.get_current_view() != self.viewInstance:
            self.router.push_back_view(self.viewInstance)

    def go_panel(self, build_func:callable):
        self.set_active_if_view_not_active()
        build_func()
    
    def go_new_view(self, newRouteContext):
        self.router.new_route_context(newRouteContext)
