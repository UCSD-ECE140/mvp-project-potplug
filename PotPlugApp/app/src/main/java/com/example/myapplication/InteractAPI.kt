package com.example.myapplication
import android.util.Log
import android.widget.Toast
import java.io.InputStream
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*
import io.ktor.client.statement.HttpResponse
import io.ktor.client.statement.readText
import io.ktor.http.ContentType
import io.ktor.http.HttpStatusCode
import io.ktor.http.contentType
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import android.app.Activity
import android.content.pm.PackageManager
import android.location.Location
import androidx.core.content.ContextCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.tasks.Task
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.withContext
import android.Manifest
import android.annotation.SuppressLint
import androidx.core.app.ActivityCompat


public class InteractAPI(aStream: InputStream?, anActivity: Activity) : Runnable {

    var theActivity: Activity = anActivity
    var theStream: InputStream = aStream!!
    var incoming : String = ""
    var theData : String = ""
    var incident : String = ""
    var severity : Int = 0
    var dataMap : MutableMap<String, List<Float>> = mutableMapOf()
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    init {
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(theActivity)
    }

    @Serializable
    data class Incident(
        val loc: List<Double>,
        val incident: String,
        val user: String,
        val severity: Double,
        val readings : List<Double> // [length, depth]
    )

    suspend fun post(postBody : Incident) : String {
        val client = HttpClient() {
            install(JsonFeature) {
                serializer = KotlinxSerializer()
            }
        }

        val response: HttpResponse = client.post("https://arosing.pythonanywhere.com/api/addIncident/") {
            contentType(ContentType.Application.Json)
            body = postBody
        }

        if(response.status.value != HttpStatusCode.OK.value){
            Log.e("HTTP Error", response.toString())
            return response.readText()
        }
        Log.d("HTTP Response", response.readText())
        return response.readText()
    }

    suspend fun uploadData(){
        Log.d("Upload", "Uploading data")
        try {
            Log.d("My Location", "Getting location")
            val location = requestLocation()
            val loc: List<Double> = listOf(location!!.latitude, location.longitude)
            Log.d("My Location for post", loc.toString())
            val user: String = "henritschulz"
            val length : Double = 1.0
            val depth : Double = 5.0
            val postBody: Incident = Incident(loc, incident, user, severity.toDouble(), listOf(length, depth))
            Log.d("Post body", postBody.toString())
            post(postBody)
        } catch (e : Exception) {
            Log.e("HTTP Error", e.stackTraceToString())
        }
    }


    fun process() : Boolean {
        try {
        Log.d("BT Data", incoming)
        if(incoming.isNotEmpty()){

            val data : List<String> = incoming.trim().split("\n")

            // Parse the data into a map
            for (row in data) {
                if (row.trim().split(":").size == 3) {
                    val (row_header, _, row_body) = row.split(":")
                    dataMap[row_header] = row_body.split(",").map { it.toFloat()}
                } else
                    Log.w("Data", "Row $row is not formatted correctly")
                }
            }

            Log.d("Data", dataMap.toString())
            Log.d("Data", "Length: ${dataMap.size}")

            // Classify the incident
            val process = Process(dataMap)
            val classification = process.classifyIncident()
            if(classification == null){
                Log.d("Incident", "No incident detected")
                return false
            }
            this.incident = classification.first
            this.severity = classification.second

            theActivity.runOnUiThread { Toast.makeText(theActivity, "Incident Detected\n" + this.incident, Toast.LENGTH_LONG).show() }
            
            Log.d("Incident", incident)
            Log.d("Severity", severity.toString())
            return true
        }
        catch (e : Exception){
            Log.e("Process Error", e.stackTraceToString())
        }
        return false
    }

    fun receiveData(): String {
        try {
            val buffer = ByteArray(1024)
            val bytes: Int = theStream.read(buffer)
            val message: String = String(buffer, 0, bytes)
            return message
        }
        catch (e : Exception){
            Log.e("Bluetooth Error", e.toString())
        }
        return ""
    }

    override fun run(){
        while(true){
            val theMessage: String = receiveData()
            if(theMessage.isNotEmpty()){
                if(theMessage.contains("END")){
                    incoming += theMessage.substring(0, theMessage.indexOf("END"))
                    if(process()) {
                        val coroutineScope = CoroutineScope(Dispatchers.IO)
                        coroutineScope.launch {
                            uploadData()
                        }
                    }
                    incoming = ""
                }
                if(theMessage.contains("BGD")){
                    incoming = theMessage.substring(theMessage.indexOf("BGD") + 3, theMessage.length)
                }
                else{
                    incoming += theMessage
                }
            }
        }
    }

    fun hasLocationPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            theActivity,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED && ContextCompat.checkSelfPermission(
            theActivity,
            Manifest.permission.ACCESS_COARSE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }

    fun requestLocationPermission() {
        ActivityCompat.requestPermissions(
            theActivity,
            arrayOf(
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ),
            120
        )
    }
    @SuppressLint("MissingPermission")
    suspend fun requestLocation(): Location? {
        return withContext(Dispatchers.IO) {
            try {
                Log.d("My Location", "Requesting location")
                if (hasLocationPermission()) {
                    Log.d("My Location", "Permission granted")
                    val locationResult: Task<Location> = fusedLocationClient.lastLocation
                    Log.d("My Location", "Awaiting location")
                    val location: Location = locationResult.await()
                    Log.d("My Location", "Location received")
                    Log.d("My Location", location.toString())
                    location
                }
                else {
                    Log.d("My Location", "No permission yet")
                    requestLocationPermission()
                    null
                }
            } catch (e: Exception) {
                Log.e("Location Error", e.toString())
                null
            }
        }
    }


}