package com.example.myapplication
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.io.InputStream

public class InteractAPI : Runnable {

//    constructor(aStream: InputStream) {
//        theStream = aStream
//    }

//    fun receiveData(): String {
//        val buffer = ByteArray(1024)
//        var bytes: Int
//        bytes = theStream.read(buffer)
//        var message: String = String(buffer,0,bytes)
//        return message
//    }

    override fun run(){
//        while(true){
//            var theMessage: String = receiveData()
//            if(theMessage!=null) {
                val postBody = """
                incident: "Pothole",
                loc: [12,33],
                severity: "Very very bad",
                user_id: 1,
                readings: "arbitrary"
            """.trimIndent()

                println(postBody)

                val client = OkHttpClient()

                val request = Request.Builder()
                    .url("http://192.168.1.148:6543/api/addIncident")
                    .post(postBody.toRequestBody())
                    .build()
                client.newCall(request).execute().use { response ->
                    if (!response.isSuccessful) throw IOException("Unexpected code $response")
                    else {
                        println("Top")
                        println(response.body?.string())
                        println("Bottom")
                    }
                }
            }
//        }
//    }

//    lateinit var theStream: InputStream



}