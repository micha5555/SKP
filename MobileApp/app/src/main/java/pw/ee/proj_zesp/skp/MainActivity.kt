package pw.ee.proj_zesp.skp

import android.Manifest.permission.ACCESS_COARSE_LOCATION
import android.Manifest.permission.ACCESS_FINE_LOCATION
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.ImageButton
import android.widget.ImageView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import java.io.*
import java.util.*


class MainActivity : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {

        requestLocation()
        getSupportActionBar()?.hide()
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_menu)

        val displayMetrics = resources.displayMetrics
        val screenWidthPx = displayMetrics.widthPixels
        val desiredDrawableWidthPx = screenWidthPx / 10

        Log.i("sizes1", displayMetrics.toString())
        Log.i("sizes2", desiredDrawableWidthPx.toString())

        val aboutAppButton: ImageButton = findViewById<ImageButton>(R.id.about_system_button)
//        val sth: ImageView = findViewById<ImageButton>(R.id.imageView6)
//        val drawable = aboutAppButton.drawable
      val drawable: Drawable = ContextCompat.getDrawable(this, R.drawable.button_shape)!!
//        aboutAppButton.setImageDrawable(sth.drawable)

//        val resized = Bitmap.createScaledBitmap((drawable as BitmapDrawable).bitmap, 400, 400, true)
//        aboutAppButton.setImageBitmap(resized)

//        drawable.setBounds(0, 0, desiredDrawableWidthPx, desiredDrawableWidthPx)
//        aboutAppButton.setBackgroundResource(0)
        aboutAppButton.setBackgroundDrawable(drawable)
//        Log.i("newsize", aboutAppButton.drawable.)

        val location = NavigationUtils.getLocation(this)
//        Log.i("current localisation", location.toString())
        aboutAppButton.setOnClickListener {
            val intent = Intent(this, AboutAppActivity::class.java)
            this.startActivity(intent)
        }
        val srequest = SKPRequest()
        srequest.send(NavigationUtils.getLocation(this), "98.2", "WA92829")
    }
    private fun requestLocation() {
        if (ContextCompat.checkSelfPermission(this,
                ACCESS_FINE_LOCATION) !==
            PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(this,
                    arrayOf(ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION), 1)
            } else {
                ActivityCompat.requestPermissions(this,
                    arrayOf(ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION), 1)
            }
        }
    }
}
