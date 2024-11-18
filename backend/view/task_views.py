from http import HTTPStatus
from flask import Blueprint, request, jsonify
from helpers.token_validation import validate_token
import control.task_control as task_con

task_bp = Blueprint("task", __name__)

#######################################

@task_bp.route("/tasks/", methods = ["POST"])
def create_task(*args,**kargs) :
    try :
        req = request
        
        result = validate_token()
        if result is int :
            if result == 400: 
                return jsonify({"error": 'Token is missing in the request, please try again'}), HTTPStatus.UNAUTHORIZED
            if result == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), HTTPStatus.FORBIDDEN
        user_info = result        

        if req.content_type != 'application/json':
            return jsonify({ 'error':'wrong content-type'}), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        body = req.json
        if "description" not in body or "assignedToUid" not in body :
            raise  Exception("Error validating form")

        result = task_con.insert_task(user_info, body)
        if result is None :
            return jsonify( {'error' : 'could not find specified id'} ), HTTPStatus.BAD_REQUEST
        inserted_id, _ = result

    except Exception as e:
        return jsonify( {'error' : f"{e}"} ), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify({ 'id' : str(inserted_id)}), HTTPStatus.CREATED

##########################################

@task_bp.route("/tasks/createdby/", methods = ["GET"])
def get_created_task(*args, **kwargs) :    
    try :
        result = validate_token()
        if result is int :
            if result == 400: 
                return jsonify({"error": 'Token is missing in the request, please try again'}), HTTPStatus.UNAUTHORIZED
            if result == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), HTTPStatus.FORBIDDEN
        user_info = result
        tasks = task_con.find_createdBy_tasks(user_info)


        return jsonify({'tasks' : tasks}), HTTPStatus.OK
    except Exception as e :
        print(e)
        return jsonify({'error':f"{e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    
##########################################

@task_bp.route("/tasks/assignedto/", methods = ["GET"])
def get_assigned_task() : 
    try:
        result = validate_token()
        if result is int :
            if result == 400: 
                return jsonify({"error": 'Token is missing in the request, please try again'}), HTTPStatus.UNAUTHORIZED
            if result == 401:
                return jsonify({"error": 'Invalid authentication token, please login again'}), HTTPStatus.FORBIDDEN
        user_info = result

        tasks = task_con.find_assignedTo_tasks(user_info)

        return jsonify( {'tasks':tasks} ), HTTPStatus.OK
    except Exception as e :
        return jsonify( {'error':f"{e}"} ), HTTPStatus.INTERNAL_SERVER_ERROR

##########################################################

@task_bp.route("/tasks/<taskUid>", methods = ["PATCH", "DELETE"])
def task_management(taskUid) :
    result = validate_token()
    if result is int :
        if result == 400: 
            return jsonify({"error": 'Token is missing in the request, please try again'}), HTTPStatus.UNAUTHORIZED
        if result == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), HTTPStatus.FORBIDDEN
    user_info = result
    
    req = request

    if (req.method == "PATCH") :
        try :
            if req.content_type != 'application/json' :
                return jsonify( {'error':'Invalid content-type'} ), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            body = req.json
            
            if 'done' not in body :
                return jsonify({"error": 'Status done not found in the request'}), HTTPStatus.BAD_REQUEST

            upserted_id  = task_con.update_task(taskUid, user_info['id'], body['done'])
            
            return jsonify({'taskUid': upserted_id}), HTTPStatus.OK
        except Exception as e :
            return jsonify({'error':f"{e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    elif (req.method == "DELETE") : 
        try :
            upserted_id  = task_con.delete_task(taskUid, user_info['id'])
            return jsonify({'taskUid': upserted_id}), HTTPStatus.OK
        except Exception as e :
            return jsonify({'error':f"{e}"}), HTTPStatus.INTERNAL_SERVER_ERROR