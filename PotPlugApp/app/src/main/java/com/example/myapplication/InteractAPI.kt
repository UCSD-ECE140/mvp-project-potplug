package com.example.myapplication
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.io.InputStream

enum class DataType{
    Accelx, Accely, Accelz, GYT, Rotx, Roty, Rotz, None
}

public class InteractAPI : Runnable {


    lateinit var theStream: InputStream
    var incoming : String = ""
    var postBody : 
    var currType: DataType = DataType.None

    constructor(aStream: InputStream) {
        theStream = aStream
    }

    fun tokenize(header: String){
        //Tokenize the 3 letter header, set the current type, and append a new section to the json message.
    }

    fun receiveData(): String {
        val buffer = ByteArray(1024)
        val bytes: Int = theStream.read(buffer)
        val message: String = String(buffer,0,bytes)
        val header: String = message.substring(0,3)
        if(null == header.toDoubleOrNull()){
            tokenize(header)
        }
        //Take the chunk of message and tokenize all the values into a list of strings, convert those strings into numerical values for processing and append them to a global list for the current data set.
        return message
    }

    override fun run(){
        while(true){
            var theMessage: String = receiveData()
            if(theMessage!=null) {

                //format the message for posting.

//
//                val request = Request.Builder()
//                    .url("http://192.168.1.148:6543/api/addIncident")
//                    .post(postBody.toRequestBody())
//                    .build()
//                client.newCall(request).execute().use { response ->
//                    if (!response.isSuccessful) throw IOException("Unexpected code $response")
//                    else {



//                val client = OkHttpClient()
//                        println("Top")
//                        println(response.body?.string())
//                        println("Bottom")
//                    }
//                }
            }
        }
    }




}