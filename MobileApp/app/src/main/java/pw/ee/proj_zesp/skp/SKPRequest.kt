package pw.ee.proj_zesp.skp

import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.text.SimpleDateFormat
import java.util.*
import javax.net.ssl.*

val AUTHORIZATION_HEADER = "Authorization"
class SKPRequest(isProblematic: Boolean, photo: Drawable, currentLocation: String, probability: String, registerPlate: String, currentDate: String) {

    val isProblematic: Boolean = isProblematic
        get() {
            return field
        }

    val photo: Drawable = photo
        get() {
            return field
        }

    val currentLocation: String = currentLocation
        get() {
            return field
        }

    val probability: String = probability
        get() {
            return field
        }

    val registerPlate: String = registerPlate
        get() {
            return field
        }

    var currentDate: String = currentDate
        get() {
            return field
        }

    fun send() {
        var url: String? = null
        if(isProblematic) {
            url = "https://10.0.2.2:5000/problematicCase/add"
        } else {
            url = "https://10.0.2.2:5000/notPaidCase/add"
        }

        val sdf = SimpleDateFormat("yyyy-dd-MM hh:mm:ss")
        if(currentDate == null) {
            currentDate = sdf.format(Date())
        }

        val photoAsByteArray: ByteArray = convertDrawableToByteArray(photo)
        val requestBody = createMultipartRequestBody(currentDate, currentLocation, registerPlate, probability, photoAsByteArray)
        val client = createOkHttpClient()

        val request = Request.Builder()
            .url(url)
            .addHeader(AUTHORIZATION_HEADER, "Bearer " + User.loggedUser?.accessToken)
            .post(requestBody)
            .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
//                throw Exception("Request failed")
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                println(response)
                println(response.message)

                Log.i("reesponse giiiit", "giiit")
            }
        })
    }

    private fun createMultipartRequestBody(currentDate: String, currentLocation: String, registerPlate: String, probability: String, photoAsByteArray: ByteArray): MultipartBody {
        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("datetime", currentDate!!)
            .addFormDataPart("location", currentLocation)
            .addFormDataPart("register_plate", registerPlate)
            .addFormDataPart("probability", probability)
            .addFormDataPart(
                "image",
                "n",
                RequestBody.create("image/jpeg".toMediaTypeOrNull(), photoAsByteArray!!)
            )
            .build()
        return requestBody
    }

    private fun createOkHttpClient(): OkHttpClient {
        val sslContext = SSLContext.getInstance("SSL")
        sslContext.init(null, trustAllCerts(), SecureRandom())

        val builder = OkHttpClient.Builder()
        builder.sslSocketFactory(sslContext.socketFactory, trustAllCerts()[0] as X509TrustManager)
        builder.hostnameVerifier(HostnameVerifier { hostname: String?, session: SSLSession? -> true })

        val client: OkHttpClient = builder.build()

        return client
    }
    private fun trustAllCerts(): Array<TrustManager> {
        return arrayOf<TrustManager>(
            object : X509TrustManager {
                override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {}

                override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {}

                override fun getAcceptedIssuers(): Array<X509Certificate> = emptyArray()
            }
        )
    }

    private fun convertDrawableToByteArray(drawable: Drawable): ByteArray {
        val bitmap = (drawable as BitmapDrawable).bitmap
        val stream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
        val byteArray = stream.toByteArray()
        return byteArray
    }
}