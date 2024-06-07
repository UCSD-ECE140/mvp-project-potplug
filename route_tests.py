import requests

def post_incident():
    url = "https://arosing.pythonanywhere.com/api/addIncident/"
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
    print(response.json())

def get_incidents():
  url = "https://arosing.pythonanywhere.com/api/incidents"
  response = requests.get(url)
  if response.status_code == 200:
    print("GET request was successful.")
  else:
    print(f"GET request failed with status code {response.status_code}.")
  print("Response body:")
  print(response.json())

if __name__ == "__main__":
  original_content = get_incidents()
  post_incident()
  new_content = get_incidents()
  print("\n\n")
  print("Success!" if original_content != new_content else "Failure!")
