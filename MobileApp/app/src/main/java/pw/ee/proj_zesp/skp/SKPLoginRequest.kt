package pw.ee.proj_zesp.skp

import android.content.Context
import android.util.Log
import android.widget.Toast
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
//import com.fasterxml.jackson.databind.ObjectMapper
//import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
//import com.fasterxml.jackson.module.kotlin.readValue
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.security.SecureRandom
import java.security.cert.X509Certificate
import javax.net.ssl.HostnameVerifier
import javax.net.ssl.SSLContext
import javax.net.ssl.SSLSession
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager

class SKPLoginRequest {

    companion object{
        fun loginRequest(login: String, password: String): Boolean{
//          TODO: różny adres ip w zależności czy emulator czy fizyczne urządzenie
            var url = "https://10.0.2.2:5000/login"
            var isSucces = false

            val requestBody = MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("login", login!!)
                .addFormDataPart("password", password)
                .build()

            val request = Request.Builder()
                .method("POST", requestBody)
                .url(url)
                .build()

            val client = createOkHttpClient()
            client.newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    e.printStackTrace()
                }

                override fun onResponse(call: Call, response: Response) {
                    println(response.code)
                    if (response.code == 200) {
                        println("Succesfully login")
                        Log.i("login result", "Succesfully login")
                        val responseBody: String = response.body?.string()!!
                        val jsonObject = JSONObject(responseBody)
                        User.loggedUser = User(
                            login,
                            jsonObject.getString("auth_token"),
                            jsonObject.getString("refresh_token")
                        )
                        isSucces = true
                    } else {
                        println("Unsuccesfully login")
                        Log.i("login result", "Unsuccesfully login")
                        isSucces = false
                    }
                }
            })
            return isSucces
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
}