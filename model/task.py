class Task :
    
    
    def __init__(self, createdByUid: str, createdByName: str,
                 assignedToUid: str, assignedToName: str,
                 description: str) :
        self.createdByUid = createdByUid
        self.createdByname = createdByName
        self.assignedToUid = assignedToUid
        self.assignedToName = assignedToName
        self.description = description
        self.done = False
