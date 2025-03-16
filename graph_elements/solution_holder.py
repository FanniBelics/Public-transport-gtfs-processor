class Solution_Holder():
    def __init__(self, fromStop:int, toStop:int) -> None:
        self.fromStop = fromStop
        self.toStop = toStop
        self.changes = []
        self.travellingTime = 0
        
    def Solution_Holder(self, fromStop:int, fromStopName:str , toStop:int, toStopName:str) -> None:
        self.fromStop = fromStop
        self.fromStopName = fromStopName
        self.toStop = toStop
        self.toStopName = toStopName
        self.travellingTime = 0
        
    def addRoute(self, route):
        self.route = route
    
    def addChange(self, fromStop, fromStopName, toStop, toStopName, routeId, routeName,time, departureTime, arrivalToNextStop):
        changeStructure = Solution_Holder(fromStop, toStop)
        changeStructure.addFromStopPartName(fromStopName)
        changeStructure.addToStopPartName(toStopName)
        changeStructure.addRoute(routeId)
        changeStructure.addRouteName(routeName)
        changeStructure.add_travelling_time(time)
        changeStructure.addDepartureTime(departureTime)
        changeStructure.addArrivalToNextStop(arrivalToNextStop)
        self.changes.append([changeStructure])
        
    def addChangeDict(self, newPart):
        self.changes.append(newPart)
        
    def addFromStopPartName(self, stop):
        self.fromStop["stop-name"] = stop
        
    def addToStopPartName(self, stop):
        self.toStop["stop-name"] = stop
        
    def addRouteName(self, routeName):
        self.routeName = routeName    
        
    def addFromStopName(self, name):
        self.fromStopName = name
    
    def addToStopName(self, name):
        self.toStopName = name
        
    def getRoutes(self) -> list:
        routesIndividual = set()
        for changeSet in self.changes:
            for change in changeSet:
                    routesIndividual.add(change["route-id"])
            
        return sorted(routesIndividual)
        
    def create_inner_dict(self) -> list:
        changesList = []
        for changes in self.changes:
            changeSetList = []
            for change_element in changes:
                if type(change_element) == dict:
                    changesList = self.changes
                    return changesList
                
                changeSetList.append(
                    {
                        "from-stop-partial" : change_element.fromStop,
                        "to-stop-partial" : change_element.toStop,
                        "route-id" : change_element.route,
                        "route-name" : change_element.routeName,
                        "travelling-time-mins" : change_element.travellingTime
                    }
                )
            changesList.append(changeSetList)
        
        return changesList
    
    def to_dictionary(self) -> dict:
        data =  {
            "from-id" : self.fromStop,
            "to-id" : self.toStop,
            "from-stop-name" : self.fromStopName,
            "to-stop-name" : self.toStopName
        }
        if len(self.changes):
            data["changes"] = self.create_inner_dict()
            
        return data
    
    def get_header(self) -> tuple:
        return (self.fromStop, self.toStop)
    
    def add_travelling_time(self, time_in_mins: int):
        self.travellingTime += time_in_mins
        
    def addDepartureTime(self, time):
        self.departure_h = time['hour']
        self.departure_m = time['minute']
        self.departure_s = time['second']
        
    def addArrivalToNextStop(self, time):
        self.arrival_h = time['hour']
        self.arrival_m = time['minute']
        self.arrival_s = time['second']