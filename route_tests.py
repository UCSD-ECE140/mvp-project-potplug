import requests

def post_incident():
    url = "http://localhost:6543/api/addIncident/"
    data = {
        'loc': (12.9715987, 77.5945627),  # longitude, latitude
        'incident': 'Pothole',
        'user': 'User1',
        'severity': 0.7,
        'readings': (10, 5)  # length, depth
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("POST request was successful.")
    else:
        print(f"POST request failed with status code {response.status_code}.")

    print("Response body:")
    print(response.text)
    
post_incident()