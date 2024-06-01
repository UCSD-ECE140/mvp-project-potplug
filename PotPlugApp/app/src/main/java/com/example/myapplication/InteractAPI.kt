package com.example.myapplication
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.io.InputStream

enum class DataType{
    Accelx, Accely, Accelz, GYT, Rotx, Roty, Rotz, End, None
}

public class InteractAPI : Runnable {


    lateinit var theStream: InputStream
    var incoming : String = ""
    var theData : String = ""
    var currType: DataType = DataType.None
    var incident : String = ""
    var severity : String = ""


    constructor(aStream: InputStream) {
        theStream = aStream
    }

    fun uploadData(){
        var loc : List<String> = listOf("", "")
        var user : String = "PlaceholderName"


        var postBody : String = "{loc: " + loc + ", incident: " + incident + ", user: " + user + ", severity: " + severity + "readings: {" + theData + "}}"
        val request = Request.Builder()
                    .url("http://192.168.1.148:6543/api/addIncident")
                    .post(postBody.toRequestBody())
                    .build()
        val client = OkHttpClient()
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) throw IOException("Unexpected code $response")
            else {
                println(response.body?.string())
            }
        }
    }

    fun process(){
        if(!incoming.isEmpty()){
            val data: List<Int> = incoming.split(",").map{ it.trim().toInt() }

            //Perform processing on data
        }
    }

    fun tokenize(header: String){
        when(header){
            "ACX" -> currType = DataType.Accelx
            "ACY" -> currType = DataType.Accely
            "ACZ" -> currType = DataType.Accelz
            "GYT" -> currType = DataType.GYT
            "RTX" -> currType = DataType.Rotx
            "RTY" -> currType = DataType.Roty
            "RTZ" -> currType = DataType.Rotz
            "End" -> currType = DataType.None
            else -> currType = DataType.None
        }
        //Tokenize the 3 letter header, set the current type
    }

    fun receiveData(): String {
        val buffer = ByteArray(1024)
        val bytes: Int = theStream.read(buffer)
        var message: String = String(buffer,0,bytes)
        return message
    }

    override fun run(){
        while(true){
            var theMessage: String = receiveData()
            if(theMessage!=null) {
                val header: String = theMessage.substring(0,3)
                if(null == header.toDoubleOrNull()){
                    tokenize(header)
                    theMessage = theMessage.substring(3)
                    process()
                    if(!incoming.isEmpty()) theData.plus(incoming + "], ")
                    theData += header +": ["
                    incoming = ""
                }
                if(currType == DataType.End){
                    uploadData()
                    theData = ""
                }
                else{
                    incoming += theMessage
                }
            }
        }
    }




}