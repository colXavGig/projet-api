from model.user_model import User
from model.task import Task
from database import task_collection, user_collection
from bson  import ObjectId

def insert_task(user, body: dict) :
    result = find_user(user_id=user['id'])
    if result is None :
        raise Exception('user not found')
    user = result

    if body['assignedToUid'] == None :
        raise Exception('no uid found')
    
    result = find_user(body['assignedToUid'])
    if result is None :
        return result
    
    assigned_u = result

    task = Task(user['id'], user['name'], assigned_u['id'], 
                assigned_u['name'], body['description'])
    
    result = task_collection.insert_one(task.__dict__)
    
    return result.inserted_id, task

def find_createdBy_tasks(user: dict) :
    tasks = []
    
    for _task in task_collection.find( {"createdByUid" : user['id']} ) :
        _task['id'] = str(_task['_id'])
        del _task['_id']

        tasks.append(_task)
    
    return tasks

def find_assignedTo_tasks(user: dict) :
    tasks = []
    
    for _task in task_collection.find( {"assignedToUid" : user['id']} ) :
        _task['id'] = str(_task['_id'])
        del _task['_id']

        tasks.append(_task)
    
    return tasks
    
def find_user(user_id) :
    result = user_collection.find_one({'_id' : ObjectId(user_id)})
    if result is None :
        return result
    
    user = result 
    user['id'] = str(user['_id'])
    del user['_id']
    return user

def update_task(task_id, user_id, done) :
    task = task_collection.find_one({'_id': ObjectId(task_id)})
    
    if task is None :
        raise Exception('Task not found') 

    if str(task['assignedToUid']) != user_id :
        raise Exception('Users can only change status when task is assigned to them.')
    
    _ = task_collection.update_one(filter= {'_id':task['_id']}, update= {'$set' : {'done': done} })
    return str(task['_id'])
        

def delete_task(task_id, user_id) :
    task = task_collection.find_one({'_id': ObjectId(task_id)})
    
    if task is None :
        raise Exception('Task not found') 

    if str(task['createdByUid']) != user_id :
        raise Exception('Users can only delete when task is created by them.') 
    
    result = task_collection.delete_one(filter= {'_id':ObjectId(task_id)})
    return result.deleted_count