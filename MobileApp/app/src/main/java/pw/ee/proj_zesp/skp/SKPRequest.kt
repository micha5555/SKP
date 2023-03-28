package pw.ee.proj_zesp.skp

import android.os.AsyncTask


import android.graphics.Bitmap
import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL

//class SKPRequest(datetime_a: String, location_a: String, registerPlate_a: String, probability_a: String, image_a: Bitmap) {
class SKPRequest(private val apiEndpoint: String) : AsyncTask<Void, Void, String>() {
//    private var datetime: String?
//    private var location: String?
//    private var registerPlate: String?
//    private var probability: String?
//    private var image: Bitmap? = null
//
//    private var client: OkHttpClient?
//    private var request: Request?
////    private val requestBody: MultipartBody?
//    private val url: String?
//    private var response: String? = null

//    init {
//        datetime = datetime_a
//        location = location_a
//        registerPlate = registerPlate_a
//        probability = probability_a
//        client = OkHttpClient()
//        image = image_a
//        url = "https://example.com/api/endpoint"
//        val file = File("")
//
//        println(file.name)
//
//        val byteArrayOutputStream = ByteArrayOutputStream()
//        image!!.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream)
//        val imageByteArray = byteArrayOutputStream.toByteArray()
////
//        val builder = MultipartBody.Builder().setType(MultipartBody.FORM)
////        requestBody = MultipartBody.Builder()
////            .setType(MultipartBody.FORM)
//            .addFormDataPart("datetime", datetime.toString())
//            .addFormDataPart("location", location.toString())
//            .addFormDataPart("register_plate", registerPlate.toString())
//            .addFormDataPart("probability", probability.toString())
////            .addFormDataPart(
////                "image",
////                "image.jpg",
////                imageByteArray.toRequestBody("image/png".toMediaTypeOrNull())
////            )
//
//        Log.i("bld", builder.build().toString())
//
//        request = Request.Builder()
//            .url(url)
//            .post(builder.build())
//            .build()
//    }

//    fun send() {
//        Log.i("rq", request.toString())
////        client?.newCall(request!!)?.execute().use { response ->
////            if (!response?.isSuccessful!!) throw IOException("Unexpected code $response")
////
////            val responseBody = response.body?.string()
////            println(responseBody)
////        }
//        response = request?.let { OkHttpClient().newCall(it).execute().toString() }
//    }
//
//    fun sendGet() {
//        val url = URL("https://www.google.com/")
//
//        with(url.openConnection() as HttpURLConnection) {
//            requestMethod = "GET"  // optional default is GET
//
////            println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")
////            Log.i("sent, result", "\nSent 'GET' request to URL : $url; Response Code : $responseCode")
//            inputStream.bufferedReader().use {
//                it.lines().forEach { line ->
//                    println(line)
//                }
//            }
//        }
//    }
//
//    fun sendGetRequest(apiEndpoint: String): String {
//        val url = URL(apiEndpoint)
//        val connection = url.openConnection() as HttpURLConnection
//        connection.requestMethod = "GET"
//        connection.setRequestProperty("Content-Type", "application/json")
//
//        val responseCode = connection.responseCode
//        if (responseCode == HttpURLConnection.HTTP_OK) {
//            val inputStream = connection.inputStream
//            val response = inputStream.bufferedReader().use { it.readText() }
//            inputStream.close()
//            return response
//        } else {
//            throw Exception("Failed to send GET request. Response code: $responseCode")
//        }
//    }
//
//
//    fun getResponse(): String? {
//        return response
//    }
//
//    fun getDatetime(): String? {
//        return datetime
//    }
//
//    fun getLocation(): String? {
//        return location
//    }
//
//    fun getRegisterPlate(): String? {
//        return registerPlate
//    }
//
//    fun getProbability(): String? {
//        return probability
//    }



    override fun doInBackground(vararg params: Void?): String {
        val url = URL(apiEndpoint)
        val connection = url.openConnection() as HttpURLConnection
        connection.requestMethod = "GET"
        connection.setRequestProperty("Content-Type", "application/json")

        val responseCode = connection.responseCode
        if (responseCode == HttpURLConnection.HTTP_OK) {
            val inputStream = connection.inputStream
            val response = inputStream.bufferedReader().use { it.readText() }
            inputStream.close()
            return response
        } else {
            throw Exception("Failed to send GET request. Response code: $responseCode")
        }
    }

    override fun onPostExecute(result: String?) {
        super.onPostExecute(result)
        Log.i("rest result", result.toString())
    }
}