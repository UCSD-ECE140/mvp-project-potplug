from fastapi import FastAPI                   # The main FastAPI import
from fastapi.responses import HTMLResponse    # Used for returning HTML responses
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn                                # Used for running the app



##########################################
#            Global Variables            #
##########################################

# Configuration
app = FastAPI()         

# I'm thinking we have severity be on a scale of 0 to 1
# Data Format: id: int, incident: str, loc: tuple, severity: int, readings: list
loc_sample = (32.86295324078554, -117.2259359279765)
sample_data = [0, "Pothole", loc_sample, .35, None] #Not sure what the readings will look like

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")



##########################################
#                 Routes                 #
##########################################

# Return home page
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("index.html") as html:
    return HTMLResponse(content=html.read())

# Return Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("dashboard.html") as html:
    return HTMLResponse(content=html.read())
  
# Login page
@app.get("/login", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("login.html") as html:
    return HTMLResponse(content=html.read())
  
# Settings page
@app.get("/settings", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("settings.html") as html:
    return HTMLResponse(content=html.read())
  
# Forgot Password Page
@app.get("/forgot_password", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("forgot_password.html") as html:
    return HTMLResponse(content=html.read())

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
@app.get("/api/incidents")
def get_incidents():
    #TODO: Get Incidents from database 
    #NOTE: This Function Will Likely Run Right After /dashboard is called.
    print("Get incidents not yet implemented")
    return []

#Add One Specific Incident to Database
@app.put("/api/incidents/{id}")
def update_incident(id: int, incident: str, loc: tuple, severity: int, readings: list):
    #TODO: Put One New Incident in Database
    type_of_incident(incident, loc, severity, readings) #Does Behavior of Incident Type or any Backprocessing
    return None

#Delete Incident
@app.delete("/api/incidents/{id}")
def delete_incident(id: int):
    # Logic to delete an incident
    return {"Deleted: not yet implemented"}

# Dashboard Data
@app.get("/api/dashboard")
def get_dashboard_data():
    #TODO
    # Will likely need to call incidents and update graph?
    return {"Not yet implemented"}

   

##########################################
#             Authentication             #
##########################################

### NOTE: I Am Going To Work On This Next, Once Ethan Sets Up Schemas
# Route To Log User Out
@app.post("/api/auth/logout")
def logout_user():
    #TODO: Implement
    return {"Logged out; not yet implemented."}

#Route to Log User In:
@app.post("/api/auth/login")
def login_user():
    #TODO: Implement
    return {"Logged in; not yet implemented."}

#Create User:
@app.put("/api/auth/register")
def register_user():
   #TODO: Implement
   return {"Created account; not yet implemented."}



##########################################
#                  Main                  #
##########################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)



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
