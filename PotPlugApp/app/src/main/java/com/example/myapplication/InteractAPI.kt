package com.example.myapplication
import android.util.Log
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.io.InputStream

public class InteractAPI(aStream: InputStream) : Runnable {


    var theStream: InputStream = aStream
    var incoming : String = ""
    var theData : String = ""
    var incident : String = ""
    var severity : String = ""
    var dataMap : MutableMap<String, List<Float>> = mutableMapOf()


    fun uploadData(){
        try {
            var loc: List<String> = listOf("Test", "Location")
            var user: String = "Henri Schulz"

            var postBody: String =
                "{loc: " + loc + ", incident: " + incident + ", user: " + user + ", severity: " + severity + "readings: {" + theData + "}}"
            val request = Request.Builder()
                .url("https://arosing.pythonanywhere.com/api/addIncident")
                .post(postBody.toRequestBody())
                .build()
            val client = OkHttpClient()
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) throw IOException("Unexpected code $response")
                else {
                    Log.d("HTML response", response.body.toString())
                }
            }
        }
        catch (e: Exception){
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
                        uploadData()
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