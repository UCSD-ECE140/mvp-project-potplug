from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from functools import wraps
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import smtplib
import databaseSample.db_utility as db
import datetime


##########################################
#            Global Variables            #
##########################################

# Configuration
app = Flask(__name__)
app.static_folder = 'static'

# Setting Up Authentication Stuff
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

# For Sending Messages
CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}



##########################################
#              Sample Data               #
##########################################

# I'm thinking we have severity be on a scale of 0 to 1
# Data Format: id: int, incident: str, loc: tuple, severity: int, readings: list (length, depth) - cm
loc_sample = (32.86295324078554, -117.2259359279765)
pothole_data = [30, 5]
sample_data = [0, "Pothole", loc_sample, .35, pothole_data] 



##########################################
#             Authentication             #
##########################################

# Checks if User is Authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # If user is not logged in, redirect to the login page
        if 'user' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Gets unique user identifier.
def getCurrentUserIdentifier():
    try:
        userId = session['user']['userinfo']['sub']
        return userId
    except:
        return {"message": "Had error"}
    
# Gets Username.
def getUserName():
    try:
        userId = session['user']['userinfo']['nickname']
        return userId
    except:
        return {"message": "Had error"}

# TODO: Implement Once database is done
def add_user(userIdentifier, username):
    print("Adding User", userIdentifier, username) # Example is google-oauth2|117344724568847202933
    return {"message" : "Not implemented yet."}

# Redirects to Auth0 Login Page
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# Redirects from Auth0 Login Page to Dashboard After Logged In
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    add_user(getCurrentUserIdentifier(), getUserName())
    return redirect("/dashboard")

# Redirects to Home Page After Logging Out
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

# Home Route
@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'), 
                           pretty=json.dumps(session.get('user'), indent=4))

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

# TODO: Update once we have db updated.
def potholeDetected(loc, incident, user_id, date, time, severity, readings):
   db.report_pothole(loc[0], loc[1])

# Should probably be using a user and then get userInfo characteristics from that.
#Can switch to twilio potentially but need to find carrier
def messageEmergencyContact(location, userInfo):
    phone_email = f"{userInfo['phoneNum']}" + CARRIERS[userInfo['carrier']]
    message = f"{userInfo['user']} has experienced a car incident at {location}"

    # Email server configuration
    sender_email = "potplugtesting@gmail.com"  # Normal Email - pass is Testing123~
    password = "pwrplsmoecjduvnr"  # App Password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() 
        
        server.login(sender_email, password)
        
        # Send the email
        server.sendmail(sender_email, phone_email, message)
        print("Text message sent successfully!")
    except Exception as e:
        print(f"Error sending text message: {e}")
    finally:
        server.quit()

# TODO: Implement logging once speedbump functionality is added.
def speedbumpDetected(loc, incident, user_id, date, time, severity, readings):
    return {"message" : "Need to add speedbump functionality later."}

# TODO: Once user database is implemented, replace getUserName() with get user.
# TODO: Update crash logging
def crashDetected(loc, incident, user_id, date, time, severity, readings):
    messageEmergencyContact(loc, getUserName()) # Replace with User Name, instead of username.
    db.report_incident(loc[0], loc[1], user_id, date, time, severity)
    return {}



##########################################
#              API Functions             #
##########################################

# Get All Incidents From Database
# TODO : Implement pulling from database.
@app.route("/api/incidents")
def get_incidents():
    
    print("All stuff in db: ", db.get_all_incidents())  #We will need to eventually use this to access db.

    test_data = {
        "id": 0,
        "incident": "Pothole",
        "loc": loc_sample,
        "severity": 0.35,
        "readings": pothole_data
    } 

    # Return the incident data as JSON
    return jsonify([test_data])

# Delete Incident
# TODO: Implement once db delete function is done.
@app.route("/api/incidents/<int:id>", methods=["DELETE"])
def delete_incident(id):
    # Logic to delete an incident
    return {"message": "Incident deleted successfully"}

# Gets the user info
# TODO: Need to implement this once we have user info storing.
@app.route("/api/getUserInfo/",)
def get_user():
    try:
        getCurrentUserIdentifier()
        return None
    except:
        return {"message": "Had error"}

# Adds the user info
# TODO: Need to implement this once we have users existing.
@app.route("/api/updateUser/", methods=["POST"])
def update_user():
    user = getCurrentUserIdentifier()

    data = request.json

    emergency_contact_name = data.get('emergency_contact_name')
    emergency_contact_phone = data.get('emergency_contact_phone')
    emergency_contact_carrier = data.get('emergency_contact_carrier')
    user_phone = data.get('user_phone')
    user_carrier = data.get('user_carrier')
    user_name = data.get('user_name')
    sensitivity = data.get('sensitivity')
    city_government = data.get('city_government')

    if not all([user, emergency_contact_name, emergency_contact_phone, emergency_contact_carrier, 
                user_phone, user_carrier, user_name, sensitivity, city_government]):
        #Should create user with None filling all of the missing fields.
        return jsonify({"error": "Missing required fields"}), 400

# Calls Respective Incident Type In Case We Need It:
@app.route("/api/addIncident/", methods=["POST"])
def type_of_incident(incident, loc, severity, user_id, readings):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()

    if(incident == "Pothole"):
       potholeDetected(loc, incident, user_id, date, time, severity, readings)
    if(incident == "Speedbump"):
       speedbumpDetected(loc, incident, user_id, date, time, severity, readings)
    if(incident == "Crash"):
        crashDetected(loc, incident, user_id, date, time, severity, readings)



##########################################
#                  Main                  #
##########################################

if __name__ == "__main__":
    #userInfo = {"user":"Adrian", "phoneNum":8582618935, "carrier":"tmobile","sensitivity":6,"emergencyContact":"Adrian", "emergencyContactPhoneNumber":8582618935}
    #messageEmergencyContact(loc_sample, userInfo)
    app.run(host="0.0.0.0", port=6543)
