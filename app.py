import os
import datetime
import pathlib
from datamanager import get_user_info, check_user_in, check_user_out, breakfast_collected, lunch_collected, on_campus
import requests
from flask import Flask, session, abort, redirect, request, render_template, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from functools import wraps


app = Flask("Google Login App")
app.secret_key = os.getenv("GOOGLE_CLIENT_SECRET") # make sure this matches with that's in client_secret.json
app.authorised_users = os.getenv("AUTHORISED_USERS")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://127.0.0.1:5000/callback"
)


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs)
    return wrapper

def authorized_user_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        elif session["google_id"] not in app.authorised_users:
            return "Unauthorized Access", 403
        else:
            return function(*args, **kwargs)
    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(session["google_id"])
    if session["google_id"] in app.authorised_users:
        return redirect("/select")
    else:
        return "Unauthorised ID"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/select")
@login_is_required
@authorized_user_required
def select():
    return render_template("selection.html")

@app.route("/campus")
@login_is_required
@authorized_user_required
def campus():
    return render_template("campus.html")

@app.route("/meals")
@login_is_required
@authorized_user_required
def meals():
    return render_template("meals.html")


@app.route("/players")
@login_is_required
@authorized_user_required
def players():
    return render_template("players.html", players=on_campus())

# Endpoint to fetch user details
@app.route('/get-user-details', methods=['POST'])
def get_user_details():
    data = request.json
    qr_code = data.get('qrCode')
    if not qr_code:
        return jsonify({"error": "QR code is missing!"}), 400
    return jsonify(get_user_info(qr_code))

# Endpoint to process check-in and check-out
@app.route('/process-action-campus', methods=['POST'])
def process_action_campus():
    data = request.json
    action = data.get('action')
    qr_code = data.get('qrCode')
    name = data.get('name')
    sport = data.get('sport')

    if not qr_code or not action:
        return jsonify({"error": "Missing data!"}), 400

    # Replace this with actual action handling logic
    if action == "check-in":
        return jsonify({"message": check_user_in(qr_code)})
    elif action == "check-out":
        return jsonify({"message": check_user_out(qr_code)})
    else:
        return jsonify({"error": "Invalid action!"}), 400


# Endpoint to process meals
@app.route('/process-action-meals', methods=['POST'])
def process_action_meals():
    data = request.json
    action = data.get('action')
    qr_code = data.get('qrCode')
    name = data.get('name')
    sport = data.get('sport')

    if not qr_code or not action:
        return jsonify({"error": "Missing data!"}), 400

    # Replace this with actual action handling logic
    if action == "collected":
        now = datetime.datetime.now().hour
        if now >= 13 and now <= 24:
            return jsonify({"message": lunch_collected(qr_code), "qrCode": qr_code})
        elif now >= 8 and now <=11:
            return jsonify({"message": breakfast_collected(qr_code), "qrCode": qr_code})
        else:
            return jsonify({"message": "Meals not started yet", "qrCode": qr_code})
    else:
        return jsonify({"error": "Invalid action!"}), 400

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc', threaded=True)