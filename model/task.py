class Task :
    
    
    def __init__(self, id, createdByUid: str, createdByName: str,
                 assignedToUid: str, assignedToName: str,
                 description: str) :
        self.id = id
        self.createdByUid = createdByUid
        self.createdByname = createdByName
        self.assignedToUid = assignedToUid
        self.assignedToName = assignedToName
        self.description = description
        self.done = False
