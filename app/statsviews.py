from flask import render_template, flash, request, redirect, session, url_for
from app import app
from .models import User, MoodItem, Mood, Team
from bson.json_util import dumps


@app.route("/stats/perso")
def statspersojson():
    result = Mood._get_collection().aggregate([{"$lookup": {"from": "mood_item", "localField": "mood", "foreignField": "_id", "as": "mood"}},
                                               {"$unwind": "$mood"},
                                               {"$group": {"_id": {"name": "$mood.name", "color": "$mood.color"}, "count": {"$sum": 1}}}])
    return dumps(result)
