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
from decimal import Decimal


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
    try: 
        db.add_user(getCurrentUserIdentifier(), getUserName())
        print("Added user: ", getUserName())
    except:
        print("User Exists.")
    return render_template("dashboard.html")

# Settings page
@app.route("/settings")
@login_required    #Requires Being Logged In.
def settings():
    return render_template("settings.html")

@app.route("/map")
@login_required
def map():
    return render_template("map.html")



##########################################
#            Helper Functions            #
##########################################

# Reports Pothole 
def potholeDetected(loc, incident, user_id, severity, readings):
    db.report_pothole(loc[0], loc[1], readings[0], readings[1], severity, date_time=None) # TODO: Update - was using incorrect number of arguments.

# Should probably be using a user and then get userInfo characteristics from that.
# Can switch to twilio potentially but need to find carrier
def messageEmergencyContact(location, userInfo):
    try:
        # Access Stuff
        phone_email = f"{userInfo[3]}" + CARRIERS[userInfo[4]]
        message = f"{userInfo[1]} has experienced a car incident at {location}"

        # Email server configuration
        sender_email = "potplugtesting@gmail.com"  # Normal Email - pass is Testing123~
        password = "pwrplsmoecjduvnr"  # App Password
    except:
        print("Failed to find user.")
        return {"User Not Found."}

    # Sends Message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls() 
        
        server.login(sender_email, password)
        server.sendmail(sender_email, phone_email, message)
        print("Text message sent successfully!")
    except Exception as e:
        print(f"Error sending text message: {e}")
    finally:
        server.quit()

# NOTE: Implement logging once speedbump functionality is added.
def speedbumpDetected(loc, incident, user_id, date, time, severity, readings):
    return {"message" : "Need to add speedbump functionality later."}

# Sends message to emergency contact and adds incident to database - Severity 0 to 5 for now.
def crashDetected(loc, incident, user_id, date, time, severity, readings):
    messageEmergencyContact(loc, user_id)
    db.report_incident(loc[0], loc[1], user_id[0], date, time, severity * 5, incident)
    return {"Worked Successfully"}

# Formats Incident Type Based off Of Incident Data
# NOTE: We may want to 
def format_incident(incident_data):
    id, lat, lon, user_id, date, time, severity, incident_type = incident_data
    loc_sample = (float(lat), float(lon))

    incident_description = {
        'pothole': f"Pothole at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}.",
        'Pothole': f"Pothole at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}.",
        'Speedbump': f"Speed bump at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}.",
        'speed bump': f"Speed bump at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}.",
        'crash': f"Crash at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}.",
        'Crash': f"Crash at location {loc_sample} with a severity of {severity}. Occured at {date}, {time}."
    }

    return {
        "id": id,
        "incident": incident_description[incident_type],
        "loc": loc_sample,
        "severity": severity,
        "readings": None
    }

##########################################
#              API Functions             #
##########################################

# Get All Incidents & Format From Database
@app.route("/api/incidents")
def get_incidents():
    """ Gets All Incidents From Database, Returning a Formatted List of Incidents """
    # Fetch all incidents from the database
    incidents = db.get_all_incidents()
    
    # Format the incidents
    formatted_incidents = [format_incident(incident) for incident in incidents]

    return jsonify(formatted_incidents)


@app.route("/api/potholes")
def get_potholes():
    """ Gets All Incidents From Database, Returning a Formatted List of Incidents """
    # Fetch all incidents from the database
    potholes = db.get_all_potholes()

    return jsonify(potholes)

# Delete Incident - Probably not used
@app.route("/api/incidents/<int:id>", methods=["DELETE"])
def delete_incident(id):
    db.delete_pothole(id)
    return {"message": "Incident deleted successfully"}

# Gets the user info
@app.route("/api/getUserInfo/")
def get_user():
    ''' Returns Current User Details:

    (unique_user_id, username, emergency_contact_name, emergency_contact_phone, emergency_contact_carrier, user_phone, user_carrier, sensitivity, city_government) 
    '''
    try:
        return db.get_user(getCurrentUserIdentifier())
    except:
        return {"message": "Had error"}

# Updates the user info
@app.route("/api/updateUser/", methods=["POST"])
def update_user():
    ''' Call To Update User:
    
    Post From Form:
        'emergency_contact_name' (String) : Max 255 Char Name
        'emergency_contact_phone' (String) : (xxx)-xxx-xxxx - must be American
        'emergency_contact_carrier' (Long) : att, tmobile, sprint, verizon 
        'user_phone' : (xxx)-xxx-xxxx - must be American
        'user_carrier' : att, tmobile, sprint, verizon 
        'user_name' : Max 255 Char Name
        'sensitivity' (float) : 0 to 1 
        'user_city' (String) : Max 255 Chars

    Currently used in settings. Can Update/Change If Necessary
    '''

    # Check if user exists: This will need to be changed to the get method from database.
    user = get_user() 

    try:
        if user is None or user == getCurrentUserIdentifier():  # Remove or
            db.add_user(getCurrentUserIdentifier(), getUserName())
    except:
        print("Line 259 Failed.")
    
    data = request.form.to_dict()

    required_fields = ['emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_carrier',
                       'user_phone', 'user_carrier', 'user_name', 'sensitivity', 'user_city']
    
    print(data)

    for field in required_fields:
        if field not in data:
            # Should create user with None filling all of the missing fields.
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    db.update_user(getCurrentUserIdentifier(), data['user_name'], data['emergency_contact_name'],
                data['emergency_contact_phone'], data['emergency_contact_carrier'],
                data['user_phone'], data['user_carrier'], data['sensitivity'], data['user_city'])
    return redirect(url_for('dashboard'))

# Calls Respective Incident Type In Case We Need It:
@app.route("/api/addIncident/", methods=["POST"]) # TODO: Updated route to make it work
def type_of_incident():
    ''' Call To Add & Enact Any Incident (Pothole, Speedbump, or Crash):
    
    Parameters:
        loc (tuple): (longitude, latitude)
        incident (string): Should be either "Pothole", "Speedbump", or "Crash"
        user (any): Currently not used.
        severity (float): any number from 0 to 1.
        readings (tuple): (length, depth, all other information)
    '''
    data = request.get_json()
    loc = data['loc']
    incident = data['incident']
    severity = data['severity']
    readings = data['readings']
    user_id = get_user()

    if(incident == "Pothole"):
        potholeDetected(loc, incident, user_id, severity, readings)
    if(incident == "Speedbump"):
        speedbumpDetected(loc, incident, user_id, severity, readings)
    if(incident == "Crash"):
        crashDetected(loc, incident, user_id, severity, readings)
    
    return jsonify({"message": "Success"})



##########################################
#                Testing                 #
##########################################

@app.route('/test-func', methods=['POST'])
def testFunc():
    type_of_incident((34.1, 34.1), "Crash", getCurrentUserIdentifier(), .8, (None))
    return jsonify({"message": "Success"})



##########################################
#                  Main                  #
##########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6543)
