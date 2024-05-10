from fastapi import FastAPI                   # The main FastAPI import
from fastapi.responses import HTMLResponse    # Used for returning HTML responses
from fastapi.staticfiles import StaticFiles   # Used for serving static files
from flask import Flask, render_template, request, redirect, session, url_for
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from functools import wraps
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

import uvicorn                                # Used for running the app



##########################################
#            Global Variables            #
##########################################

# Configuration
app = Flask(__name__)         

# I'm thinking we have severity be on a scale of 0 to 1
# Data Format: id: int, incident: str, loc: tuple, severity: int, readings: list
loc_sample = (32.86295324078554, -117.2259359279765)
sample_data = [0, "Pothole", loc_sample, .35, None] #Not sure what the readings will look like

# Mount the static directory
app.static_folder = 'static'

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


#https://pythonhosted.org/Flask-OAuth/
#https://manage.auth0.com/dashboard/us/dev-ufswkzdksg6jljvi/applications/Fgw7QIGnvOOccgy4lafr7FKNOBWZmfng/quickstart

app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)



##########################################
#             Authentication             #
##########################################

# Checks if User is Authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        print(session)  #-  We may be able to add settings once we detect user

        if 'user' not in session:
            # If user is not logged in, redirect to the login page
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )



##########################################
#                 Routes                 #
##########################################

@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

# Dashboard Page.
@app.route("/dashboard")
@login_required   #Requires Being Logged In.
def dashboard():
    return render_template("dashboard.html")

# Settings page
@app.route("/settings")
@login_required    #Requires Being Logged In.
def settings():
    return render_template("settings.html")



##########################################
#            Helper Functions            #
##########################################

def potholeDetected(loc, severity, readings):
   return

### IF WE LIKE THIS STRUCTURE THEN WE MAY NEED TO MAKE A FUNCTION FOR EVERY OTHER
### INCIDENT TYPE.

# Calls Respective Incident Type In Case We Need It:
def type_of_incident(incident, loc, severity, readings):
   if(incident == "Pothole"):
      potholeDetected(loc, severity, readings)




##########################################
#              API Functions             #
##########################################

# Get All Incidents From Database   ###NOTE WE MAY WANT TO MAKE IT ONLY GET LOCAL INCIDENTS.
@app.route("/api/incidents")
def get_incidents():
    # TODO: Get Incidents from database
    # NOTE: This Function Will Likely Run Right After /dashboard is called.
    print("Get incidents not yet implemented")
    return []

# Add One Specific Incident to Database
@app.route("/api/incidents/<int:id>", methods=["PUT"])
def update_incident(id):
    # TODO: Put One New Incident in Database
    incident = "Pothole"  # Example incident, you need to get this from request data
    loc = (0.0, 0.0)  # Example location, you need to get this from request data
    severity = 0  # Example severity, you need to get this from request data
    readings = []  # Example readings, you need to get this from request data
    type_of_incident(incident, loc, severity, readings)  # Does Behavior of Incident Type or any Backprocessing
    return {"message": "Incident updated successfully"}

# Delete Incident
@app.route("/api/incidents/<int:id>", methods=["DELETE"])
def delete_incident(id):
    # Logic to delete an incident
    return {"message": "Incident deleted successfully"}

# Dashboard Data
@app.route("/api/dashboard")
def get_dashboard_data():
    # TODO
    # Will likely need to call incidents and update graph?
    return {"message": "Dashboard data retrieved successfully"}



##########################################
#                  Main                  #
##########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6543)



##########################################
#                 Notes                  #
##########################################

# Steps
# Website Must Be Able To:
# 1) Receives Data From Phone: location, severity, type of incident, user confirmation, ultrasound readings, accelerometer readings, gyroscope readings.
# 2) Display Data to Users Via Dashboard & Ultimately Phone
# 3) Store Data  -  Eddie
# 4) Track Users Using The Website  - Later

# ROUTES FOR EACH STEP:
########  1  ##########
# Pothole Detected      --->  Step 3
# Speedbump Detected    --->  Step 3
# Crash Detected        --->  Step 3
# Damage Detected       --->  Step 3
# Crash Detected        --->  Step 3

########  2  ##########
# Create Login Routes (Optional)
# Create Basic Text Display of Data on Dashboard  --->  Ultimately Will Tie to Google Plugin
