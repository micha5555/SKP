package pw.ee.proj_zesp.skp.utils

import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.os.Build
import java.io.ByteArrayOutputStream

class CommonUtils {

    companion object {
        fun isEmulator(): Boolean {
            return (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                    || Build.FINGERPRINT.startsWith("generic")
                    || Build.FINGERPRINT.startsWith("unknown")
                    || Build.HARDWARE.contains("goldfish")
                    || Build.HARDWARE.contains("ranchu")
                    || Build.MODEL.contains("google_sdk")
                    || Build.MODEL.contains("Emulator")
                    || Build.MODEL.contains("Android SDK built for x86")
                    || Build.MANUFACTURER.contains("Genymotion")
                    || Build.PRODUCT.contains("sdk_google")
                    || Build.PRODUCT.contains("google_sdk")
                    || Build.PRODUCT.contains("sdk")
                    || Build.PRODUCT.contains("sdk_x86")
                    || Build.PRODUCT.contains("sdk_gphone64_arm64")
                    || Build.PRODUCT.contains("vbox86p")
                    || Build.PRODUCT.contains("emulator")
                    || Build.PRODUCT.contains("simulator");
        }

        fun convertDrawableToByteArray(drawable: Drawable): ByteArray {
            val bitmap = (drawable as BitmapDrawable).bitmap
            val stream = ByteArrayOutputStream()
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            val byteArray = stream.toByteArray()
            return byteArray
        }

        fun convertBitmapToByteArray(bitmap: Bitmap): ByteArray {
            val stream = ByteArrayOutputStream()
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            return stream.toByteArray()
        }

        fun parseProbabilityToRequestFormat(probability: Double): String {
            var probabilityDouble = probability * 100
            var probabilityString = probabilityDouble.toString()
            if(probabilityDouble >= 10 && probabilityDouble < 100) {
                probabilityString = "0$probabilityString"
            } else if(probabilityDouble < 10) {
                probabilityString = "00$probabilityString"
            }

            if(probabilityString.length < 6) {
                for(i in 1..6-probabilityString.length) {
                    probabilityString += "0"
                }
            } else if(probabilityString.length > 6) {
                probabilityString = probabilityString.substring(0, 6)
            }

            return probabilityString
        }
    }
}