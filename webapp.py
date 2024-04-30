from fastapi import FastAPI                   # The main FastAPI import
from fastapi.responses import HTMLResponse    # Used for returning HTML responses
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn                                # Used for running the app

# Configuration
app = FastAPI()                   

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Return home page
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("index.html") as html:
    return HTMLResponse(content=html.read())

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
