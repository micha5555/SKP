package pw.ee.proj_zesp.skp

import android.content.Intent

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.Drawable
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ImageButton
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.content.res.ResourcesCompat
import java.util.*

import android.os.Build
import androidx.annotation.RequiresApi
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import java.io.*

class MainActivity : AppCompatActivity() {

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {

//        var req: SKPRequest = SKPRequest("date and time", "location in the middle of nowhere", "WA54RT", "45.6")
//        Log.i("dt", req.getDatetime().toString())
//        Log.i("lt", req.getLocation().toString())
//        Log.i("rp", req.getRegisterPlate().toString())
//        Log.i("pb", req.getProbability().toString())
//        req.send()
//        Log.i("rsp", req.getResponse().toString())

//        var drawable = ContextCompat.getDrawable(this, R.drawable.image)
//        val drawable = BitmapFactory.decodeResource(resources, R.drawable.psiel)


        val drawable: Drawable? =
            ResourcesCompat.getDrawable(resources, R.drawable.psiel, null)

        var bitmap: Bitmap = Bitmap.createBitmap(
            drawable!!.intrinsicWidth,
            drawable!!.intrinsicHeight,
            Bitmap.Config.ARGB_8888
        )
        val canvas = Canvas(bitmap)
        drawable.setBounds(0, 0, canvas.width, canvas.height)
        drawable.draw(canvas)


//        Log.i("imvie", "ggg")

        getSupportActionBar()?.hide()
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_menu)

//        val req: SKPRequest = SKPRequest("some date", "some location", "some plate", "some probability", bitmap)
//        val imv: ImageView= findViewById<ImageView>(R.id.ttt);
//        req.send()
//        req.sendGet()
//        Log.i("resp", req.getResponse().toString())


//        Log.i("drawbl", drawable.toString())
//        val response = req.sendGetRequest("https://example.com/api/endpoint")
//        Log.d("REST response", response)

//        val restRequestTask = SKPRequest("https://stackoverflow.com/questions/46177133/http-request-in-android-with-kotlin")
//        restRequestTask.execute()

//        System.out.println(" C DATE is  "+currentDate)
        val currentLocation = NavigationUtils.getLocation(this)
//        val sr = SKPRequest()
//        sr.send(currentLocation, "123", "123")

        val aboutAppButton: ImageButton = findViewById<ImageButton>(R.id.about_system_button)
//        aboutAppButton.setImageBitmap(bitmap)

        aboutAppButton.setOnClickListener {
            val intent = Intent(this, AboutAppActivity::class.java)
            this.startActivity(intent)

        }
    }
}
