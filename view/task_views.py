from flask import Blueprint, request 
from control.token import validateToken

task = Blueprint("task")
validator = validateToken()

@task.route("/tasks/", methods = ["POST"])
@validator.requireToken()
def create_task() :
    # TODO : create task implementation
    req = request
    if req.json["description"] == None or req.json["assignedToUid"] == None :
        raise  Exception("Error validating form")
    pass

@task.route("/tasks/createdby/", methods = ["GET"])
def get_created_task() :
    # TODO : implement created task getter
    return

@task.route("/tasks/assignedto/", methods = ["GET"])
def get_assigned_task() : 
    # TODO : implement assigned task getter
    return

@task.routes("/tasks/:taskUid", methods = ["PATCH", "DELETE"])
def task_management() :
    if (request.method == "PATCH") :
        # TODO: update route implementation
        return
    elif (request.method == "DELETE") : 
        # TODO: delete route implementation
        return

    return


