// Create the script tag, set the appropriate attributes
var script = document.createElement('script');
script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCenQtBD0vngzEW0PE8dd_klQfms7QHWAo&callback=initMap';
script.async = true;

let map;

window.initMap = function() {
  console.log("test");
    const { Map } = google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8,
    });

    // Fetch and display potholes
    fetchPotholes();
};

// Fetch potholes from the database and display them on the map
async function fetchPotholes() {
    try {
        const response = await fetch('/api/potholes');  // Adjust the endpoint as needed
        const potholes = await response.json();


        const userLocation = { lat: 32.861016, lng: -117.209321 };  // Example user location, replace with actual

        potholes.forEach(pothole => {
            const potholeLocation = { lat: pothole.latitude, lng: pothole.longitude };
            console.log(potholeLocation);
            if (isWithinDistance(userLocation, potholeLocation, 10)) {  // 10 miles distance example
                displayPothole(potholeLocation);
            }
        });
    } catch (error) {
        console.error('Error fetching potholes:', error);
    }
}

// Check if a location is within a certain distance from the user's location
function isWithinDistance(userLocation, potholeLocation, distance) {
    const userLatLng = new google.maps.LatLng(userLocation.lat, userLocation.lng);
    const potholeLatLng = new google.maps.LatLng(potholeLocation.lat, potholeLocation.lng);
    const distanceInMeters = google.maps.geometry.spherical.computeDistanceBetween(userLatLng, potholeLatLng);
    const distanceInMiles = distanceInMeters / 1609.34;  // Convert meters to miles
    return distanceInMiles <= distance;
}

// Display pothole on the map
function displayPothole(location) {
    new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 5,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: location,
        radius: 30  // Adjust the radius of the circle as needed
    });
}

// Append the 'script' element to 'head'
document.head.appendChild(script);
