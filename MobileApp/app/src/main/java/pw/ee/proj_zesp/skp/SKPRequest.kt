package pw.ee.proj_zesp.skp

import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.util.Log
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import pw.ee.proj_zesp.skp.utils.CommonUtils
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.text.SimpleDateFormat
import java.util.*
import javax.net.ssl.*

val AUTHORIZATION_HEADER = "Authorization"
class SKPRequest(isProblematic: Boolean, photo: ByteArray, currentLocation: String, probability: String, registerPlate: String, currentDate: String): Thread() {

    val isProblematic: Boolean = isProblematic
        get() {
            return field
        }

    val photo: ByteArray = photo
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

    public override fun run() {
        var url: String? = null
        if(isProblematic) {
            url = "https://172.25.0.1:5000/problematicCase/add"
            if(CommonUtils.isEmulator()) {
                url = "https://10.0.2.2:5000/problematicCase/add"
            }
        } else {
            url = "https://172.25.0.1:5000/notPaidCase/add"
            if(CommonUtils.isEmulator()) {
                url = "https://10.0.2.2:5000/notPaidCase/add"
            }
        }
        println("url")
        println(url)
        val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")
        if(currentDate == null || currentDate.isEmpty()) {
            currentDate = sdf.format(Date())
        }

        val requestBody = createMultipartRequestBody(currentDate, currentLocation, registerPlate, probability, photo)
        val client = createOkHttpClient()

        val request = Request.Builder()
            .url(url)
            .addHeader(AUTHORIZATION_HEADER, "Bearer " + User.loggedUser?.accessToken)
            .post(requestBody)
            .build()
        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                println("Request failed")
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                println(response)
                println(response.message)
                println(response.code)
                if(response.code < 200 || response.code >= 300) {
                    FailedRequest.addFailedRequest(FailedRequest(isProblematic, photo, currentLocation, probability, registerPlate, currentDate))
                    FailedRequest.printFailedRequests()
                }
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

}