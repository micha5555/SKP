package pw.ee.proj_zesp.skp

import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

class SKPRequest {
    fun send(currentLocation: String?, probability: String?, registerPlate: String?) {
        val url = "https://10.0.2.2:5000/books"
        val client: OkHttpClient = OkHttpClient()

        val sdf = SimpleDateFormat("yyyy-dd-MM hh:mm:ss")
        val currentDate = sdf.format(Date())

        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("datetime", currentDate)
            .addFormDataPart("location", currentLocation.toString())
            .addFormDataPart("register_plate", registerPlate.toString())
            .addFormDataPart("probability", probability.toString())
//            .addFormDataPart(
//                "image",
//                "cygan.jpg",
//                RequestBody.create("image/jpeg".toMediaTypeOrNull(), File("pw/ee/proj_zesp/skp/cygan.jpg"))
//            )
            .build()

        val request = Request.Builder()
            .url(url)
            .post(requestBody)
            .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                Log.i("reesponse giiiit", "giiit")
            }
        })

//        client.newCall(request).execute()
//            .use { response ->
//            if (!response.isSuccessful) throw IOException("Unexpected code $response")
//
//            val responseBody = response.body?.string()
//            println(responseBody)
//        }
    }
}