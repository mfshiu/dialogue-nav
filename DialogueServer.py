#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import threading
from threading import Timer
import Speaker
import time

# Flask app should start in global layout
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = response_dialogflow(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def response_dialogflow(req):
    reply_msg = '很抱歉我沒聽懂，請再說一次。'
    query = req.get("queryResult")
    if query.get("action") == "NavStart":
        params = query.get("parameters")
        if params and params.get("location"):
            destination = params.get("location")
            reply_msg = '請稍候，我查一下附近的' + destination
            start_nav(destination)
        else:
            reply_msg = '我沒聽懂地點，請再說一次。'

    Speaker.play(reply_msg)
    res_json = {'fulfillmentText': reply_msg}
    return res_json


def start_nav(destination):
    t = threading.Thread(target=do_start_nav, args=(destination,))
    t.start()


def do_start_nav(destination):
    time.sleep(5)
    Speaker.play("附近有捷運領航站，要我帶您過去嗎？")


def test_timer():
    # t = Timer(5.0, test_timer)
    # t.start()
    Speaker.play("時間到")
    print("hello, world")


def makeWebhookResult(req):
    # askweather的地方是Dialogflow>Intent>Action 取名的內容
    if req.get("queryResult").get("action") != "nav.start":
        return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    # parameters.get("weatherlocation")的weatherlocation是Dialogflow > Entitiy
    # 也就是步驟josn格式中parameters>weatherlocation
    #zone = parameters.get("weatherlocation")
    #先設定一個回應
    #如果是Taipei,cost的位置就回營18
    #cost = {'Taipei':'18', 'Kaohsiung':'20', 'Taichung':'10','Tainan':'25'}
    #speech就是回應的內容
    #speech = "The temperatrue of " + zone + " is " + str(cost[zone])
    speech = "This is a response from webhook."
    print("Response:")
    print(speech)
    #回傳
    return {
      'fulfillmentText': 'This is a response from webhook.',
      "payload": {
        "google": {
          "expectUserResponse": True,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": "Howdy! I can tell you fun facts about almost any number, like 42. What do you have in mind?",
                  "displayText": "Howdy! I can tell you fun facts about almost any number. What do you have in mind?"
                }
              }
            ]
          }
        }
      }
    }


if __name__ == "__main__":
    app.run(debug=True, port=80)
