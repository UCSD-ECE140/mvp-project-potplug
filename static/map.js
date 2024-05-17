// Create the script tag, set the appropriate attributes
var script = document.createElement('script');
script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCenQtBD0vngzEW0PE8dd_klQfms7QHWAo&callback=initMap';
script.async = true;

// Attach your callback function to the `window` object
window.initMap = function() {
    const { Map } = google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8,
    });
};

// Append the 'script' element to 'head'
document.head.appendChild(script);