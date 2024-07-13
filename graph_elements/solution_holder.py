class Solution_Holder():
    def __init__(self, fromStop:int, toStop:int) -> None:
        self.fromStop = fromStop
        self.toStop = toStop
        self.changes = []
        self.travellingTime = 0
        
        
    def addRoute(self, route):
        self.route = route
    
    def addChange(self, fromStop, toStop, route, time):
        changeStructure = Solution_Holder(fromStop, toStop)
        changeStructure.addRoute(route)
        changeStructure.add_travelling_time(time)
        self.changes.append([changeStructure])
        
    def addChangeDict(self, newPart):
        self.changes.append(newPart)
        
    def getRoutes(self) -> list:
        routesIndividual = set()
        for changeSet in self.changes:
            for change in changeSet:
                for changeElement in change:
                    routesIndividual.add(changeElement["route-id"])
            
        return sorted(routesIndividual)
        
    def create_inner_dict(self) -> list:
        changesList = []
        for changes in self.changes:
            changeSetList = []
            for change_element in changes:
                changeSetList.append(
                    {
                        "from-stop-partial" : change_element.fromStop,
                        "to-stop-partial" : change_element.toStop,
                        "route-id" : change_element.route,
                        "travelling-time-mins" : change_element.travellingTime
                    }
                )
            changesList.append(changeSetList)
        
        return changesList
    
    def to_dictionary(self) -> dict:
        data =  {
            "from-id" : self.fromStop,
            "to-id" : self.toStop,
        }
        if len(self.changes):
            data["changes"] = self.create_inner_dict()
            
        return data
    
    def get_header(self) -> tuple:
        return (self.fromStop, self.toStop)
    
    def add_travelling_time(self, time_in_mins: int):
        self.travellingTime += time_in_mins