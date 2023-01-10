from flask import Flask, Blueprint, request

api = Blueprint('api', __name__)

@api.route('/add', methods=['POST'])
def add_artist():
  print(request.json)
  return request.json