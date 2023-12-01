from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if id is None:
        return jsonify({"error": "ID not provided"}), 400
    for picture in data:
        if picture['id'] == id:
            return picture
    return jsonify({"Message":"ID not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json
    for photo in data:
        if new_pic["id"] == photo['id']:
            return {"Message": f"picture with id {new_pic['id']} already present"}, 302
    data.append(new_pic)
    return jsonify(new_pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_pic = request.json
    for photo in data:
        if photo['id'] == id:
            photo["pic_url"] = updated_pic.get("pic_url", photo["pic_url"])
            photo["event_country"] = updated_pic.get("event_country", photo["event_country"])
            photo["event_state"] = updated_pic.get("event_state", photo["event_state"])
            photo["event_city"] = updated_pic.get("event_city", photo["event_city"])
            photo["event_date"] = updated_pic.get("event_date", photo["event_date"])
            return {"message": f"Picture with ID {id} updated successfully"}, 200
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for photo in data:
        if photo['id'] == id:
            data.remove(photo)
            return {}, 204
    return {"message": "picture not found"}, 404
