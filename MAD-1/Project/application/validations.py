from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class UserNotFoundError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class BusinessValidationError(HTTPException):

	def __init__(self,status_code,error_code,error_message):
		message = {
		"error_code": error_code,
		"error_message": error_message
		}
		self.response = make_response(json.dumps(message),status_code)


class UserExistError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class TrackerExistError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)

class TrackerNotFoundError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)


class LogNotFoundError(HTTPException):

	def __init__(self,status_code):
		self.response = make_response('',status_code)