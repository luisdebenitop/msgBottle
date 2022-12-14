from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB
from uuid import uuid4
from datetime import datetime


class DB:
    _instance = None

    def __init__(self):
        self.db = TinyDB("db.json")

    def instance():
        if DB._instance == None:
            DB._instance = DB()
        return DB._instance.db


class Response:
    def ok(data):
        return (
            data,
            200,
            {"Content-Type": "application/json"},
        )

    def error(msg, code):
        return ({"err": msg}, code, {"Content-Type": "application/json"})


app = Flask(__name__)
cors = CORS(app)


class Validator:
    def keys_in_object(keys, object):
        for key in keys:
            if key not in object.keys():
                return False
            if object[key] is None:
                return False
        return True

    def array_is_empty(object):
        try:
            return len(object) <= 0
        except:
            return True

    def obj_is_empty(object):
        try:
            return len(object.keys()) <= 0
        except:
            return True


@app.route("/message", methods=["POST"])
def create_msg():
    body = request.json
    if Validator.obj_is_empty(body) or not Validator.keys_in_object(
        ["msg", "lat", "lng"], body
    ):
        return Response.error("Missing keys", 400)
    if not isinstance(body, list) or len(body) <= 0:
        return Response.error("Body must be at least 1 question", 400)

    obj = {"msg": body["msg"], "lat": body["lat"], "lng": body["lng"]}
    try:
        DB.instance().insert(obj)
    except Exception:
        return Response.error("There was a problem inserting object", 500)

    return Response.ok(obj)


@app.route("/message", methods=["GET"])
def get_msgs():
    try:
        msg = DB.instance().all()
    except Exception as exc:
        return Response.error("Error retrieving messages", 500)

    return Response.ok({"res": msg})


@app.route("/message/<id>", methods=["PUT"])
def edit_msg(id):

    return Response.ok(id)
