import json, os

from flask import request, Response, jsonify, render_template, Flask
from pywebpush import webpush
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PRIVATE_KEY_PATH = os.path.join(os.getcwd(), "private_key.txt")
PUBLIC_KEY_PATH = os.path.join(os.getcwd(), "public_key.txt")

VAPID_PRIVATE_KEY = None
VAPID_PUBLIC_KEY = None

with open(PRIVATE_KEY_PATH, "r+", encoding='utf-8') as file:
    VAPID_PRIVATE_KEY = file.readline().strip("\n")
with open(PUBLIC_KEY_PATH, "r+", encoding='utf-8') as file:
    VAPID_PUBLIC_KEY = file.read().strip("\n")

# more info about vapid claims: https://github.com/web-push-libs/vapid/tree/main/python


def send_web_push(subscription_information, message_body):
    aud_url = '/'.join(subscription_information['endpoint'].split('/')[0:3])

    return webpush(subscription_info=subscription_information,
                   data=message_body,
                   vapid_private_key=VAPID_PRIVATE_KEY,
                   vapid_claims={
                       "sub": "mailto:develop@raturi.in",
                       "aud": aud_url
                   })


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/notifications/subscription", methods=["GET"])
def subscription():
    """
        GET returns vapid public key which clients uses to send around push notification
    """

    return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
                    headers={"Access-Control-Allow-Origin": "*"},
                    content_type="application/json")


@app.route("/notifications/push", methods=['POST'])
def push_v1():
    """
        POST gets the payload for push notificacion and sends it
    """
    try:
        if not request.json or not request.json.get('subscription_info'):
            return Response(status=400)

        subscription_json = request.json.get('subscription_info')
        subscription_info = json.loads(subscription_json)
        send_web_push(subscription_info, "Push Test v1")
        return Response(status=200)

    except Exception as e:
        return jsonify({'failed': str(e)})


if __name__ == "__main__":
    app.run()
