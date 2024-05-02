#### WE NEED TO FIGURE THIS OUT ####

# Phone will receive data directly from user
# Will recieve ultrasound readings, accelerometer readings, and gyroscope readings
# Will send location, severity, type of incident, user confirmation, and ultrasound readings, accelerometer readings, and gyroscope readings.


###  ROUTES  ###
# Implement ASAP:
# /api/postIncident   ### Post request to create a new incident
# /api/getInfo   ### Get information from devices
# /api/userConfirmation   ### Get user confirmation
# location   ### Get user location
# /api/generateSeverity   ### Generate severity
# /api/typeOfIncident   ### Guesses type of incident
# notifyUser

# Later:
# /api/getIncidents   ### Get full list of incidents from webserver
# /api/getIncident/id   ### Get an incident from webserver

# Optional: 
# /api/auth/login   ### POST to authenticate user
# /api/auth/register   ### POST to register new user
# /api/auth/logout   ### Logout