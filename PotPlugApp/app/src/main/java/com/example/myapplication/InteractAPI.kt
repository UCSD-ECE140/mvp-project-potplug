package com.example.myapplication
import android.util.Log
import android.widget.Toast
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
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
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import android.app.Activity
import android.content.Context
import android.location.Criteria
import android.location.LocationManager
import android.location.LocationRequest
import android.os.Build
import androidx.annotation.RequiresApi
import androidx.core.content.ContextCompat.getSystemService
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices


public class InteractAPI(aStream: InputStream?, anActivity: Activity) : Runnable {

    var theActivity: Activity = anActivity
    val fusedLocationProviderClient: FusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(theActivity)
    var theStream: InputStream = aStream!!
    var incoming : String = ""
    var theData : String = ""
    var incident : String = ""
    var severity : String = ""
    var dataMap : MutableMap<String, List<Float>> = mutableMapOf()

    @Serializable
    data class Incident(
        val loc: Pair<Double, Double>,
        val incident: String,
        val user: String,
        val severity: Double,
        val readings: Map<String, List<Float>>
    )

    suspend fun post(postBody : Incident) : String {
        val client = HttpClient() {
            install(JsonFeature) {
                serializer = KotlinxSerializer()
            }
        }

        val response: HttpResponse = client.post("http://172.21.16.1:6543/api/addIncident/") {
            contentType(ContentType.Application.Json)
            body = postBody
        }

        if(response.status.value != HttpStatusCode.OK.value){
            Log.e("HTTP Error", response.toString())
            return response.readText()
        }
        Log.d("Response", response.readText())
        return response.readText()
    }

    suspend fun uploadData(){
        try {
            val loc: Pair<Double, Double> = Pair(32.8812, -117.2344)
            val user: String = "Henri Schulz"
            val postBody: Incident = Incident(loc, incident, user, severity.toDouble(), dataMap)
            post(postBody)
        } catch (e : Exception) {
            Log.e("HTTP Error", e.toString())
        }
    }


    fun process() : Boolean {
        Log.d("BT Data", incoming)
        if(incoming.isNotEmpty()){

            val data : List<String> = incoming.trim().split("\n")

            // Parse the data into a map
            for (row in data) {
                if (row.trim().split(":").size == 3) {
                    val (row_header, _, row_body) = row.split(":")
                    dataMap[row_header] = row_body.split(",").map { it.toFloat() }
                } else {
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

            theActivity.runOnUiThread { Toast.makeText(theActivity, "Incident Detected\n" + this.incident + " - " + this.severity, Toast.LENGTH_LONG).show() }
            
            Log.d("Incident", incident)
            Log.d("Severity", severity.toString())
            return true
        }
        return false
    }

    fun receiveData(): String {
        val buffer = ByteArray(1024)
        val bytes: Int = theStream.read(buffer)
        val message: String = String(buffer,0,bytes)
        return message
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




}