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


@api.route('/add', methods=['POST'])
def add_artist():
  conn = get_db_connection()
  cur = conn.cursor()

  genre = request.json['genre']
  name = request.json['artist']
  url = request.json['url']

  cur.execute('INSERT INTO public.artists (genre_id, name, spotify_url)'
           'VALUES (%s, %s, %s) RETURNING id', (genre, name, url))

  conn.commit()

  artists = cur.fetchall()

  if artists is None:
    return jsonify({"status": "500"})

  cur.close()
  conn.close()

  response = make_response(jsonify({ "status": 200, "data": name }))

  return response