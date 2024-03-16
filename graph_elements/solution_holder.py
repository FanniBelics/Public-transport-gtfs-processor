class Solution_Holder():
    def __init__(self, fromStop, toStop, route = "") -> None:
        self.fromStop = fromStop
        self.toStop = toStop
        self.route = route
        self.changes = []
        
    def addChange(self, changeStructure: list["Solution_Holder"]):
        self.changes.append(changeStructure)
        
    def create_inner_dict(self) -> dict:
        changesList = []
        for changes in self.changes:
            changeSetList = []
            for change_element in changes:
                changeSetList.append(
                    {
                        "from-stop-partial" : change_element.fromStop,
                        "to-stop-partial" : change_element.toStop,
                        "route-id" : change_element.route
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