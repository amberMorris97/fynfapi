from flask import Flask, Blueprint, request, jsonify, make_response
from dotenv import dotenv_values
import psycopg2

api = Blueprint('api', __name__)

def get_env(var):
  return dotenv_values(".env")[var]

def get_db_connection():
  conn = psycopg2.connect(
          host='localhost',
          database=get_env("DB"),
          user=get_env("DB_USERNAME"),
          password=get_env("DB_PASSWORD"))
  return conn

@api.route('/test', methods=['POST'])
def test_request():
  print('hello world')
  response = make_response(jsonify({ "status": 200, "data": "hi" }))
  return response


@api.route('/add', methods=['POST'])
def add_artist():
  conn = get_db_connection()
  cur = conn.cursor()

  name = request.json['artist']
  url = request.json['url']
  uri = request.json['uri']
  id = request.json['id']
  match_1 = request.json['match1']
  match_2 = request.json['match2']
  match_3 = request.json['match3']

  cur.execute('INSERT INTO public.artist_matches (spotify_id, name, spotify_url, spotify_uri, match_1, match_2, match_3)'
           'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id', (id, name, url, uri, match_1, match_2, match_3))

  conn.commit()

  artists = cur.fetchall()

  if artists is None:
    return jsonify({"status": "500"})

  cur.close()
  conn.close()

  response = make_response(jsonify({ "status": 200, "data": name }))

  return response

@api.route('/add_email', methods=['POST'])
def add_email():
  conn = get_db_connection()
  cur = conn.cursor()

  email = request.json['email']

  cur.execute('INSERT INTO public.emails (email)'
              'VALUES (%s) RETURNING email', (email,))

  conn.commit()

  email_added = cur.fetchall()

  if email_added is None:
    return jsonify({"status": "500"})

  cur.close()
  conn.close()

  response = make_response(jsonify({ "status": 200, "data": email }))

  return response