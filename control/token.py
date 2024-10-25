from http import HTTPStatus
from flask import jsonify, request as req

class validateToken : 
    # TODO: implement validate token
    def __init__(self):
        pass
    
    def requireToken(func) :
        tokens = [] # TODO: use real token
        def warpper(*args,**kwargs) :
            currToken = kwargs["token"]

            if currToken == None :
                return jsonify( 
                    {"error":"Token is missing in the request, please try" +
                     " again"}), HTTPStatus.BAD_REQUEST # http 400

            elif currToken not in tokens :
               return jsonify( 
                    {"error":"Invalid authentication token, please login" +
                     " again"}), HTTPStatus.UNAUTHORIZED # http 401

            elif currToken in tokens : 
                return func(args, kwargs)

            
