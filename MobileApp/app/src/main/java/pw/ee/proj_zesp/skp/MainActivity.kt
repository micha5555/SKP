package pw.ee.proj_zesp.skp

import android.content.Intent
import android.graphics.drawable.Drawable
import android.os.Build
import android.os.Bundle
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.TextView

import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.content.ContextCompat

import pw.ee.proj_zesp.skp.utils.NavigationUtils

import java.io.*
import java.util.*

import kotlin.concurrent.schedule


class MainActivity : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        NavigationUtils.requestLocationPermissions(this)
        getSupportActionBar()?.hide()
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_menu)

        val aboutAppButton: ImageButton = findViewById<ImageButton>(R.id.about_system_button)
        val startControlButton: ImageButton = findViewById<ImageButton>(R.id.start_control_button_on_menuview)
        val button: Drawable = ContextCompat.getDrawable(this, R.drawable.button_shape)!!
        aboutAppButton.setBackgroundDrawable(button)
        startControlButton.setBackgroundDrawable(button)
        aboutAppButton.setOnClickListener {
            val intent = Intent(this, AboutAppActivity::class.java)
            this.startActivity(intent)
        }

        val doge: Drawable = ContextCompat.getDrawable(this, R.drawable.doge)!!

        val srequest = SKPRequest(false, doge, "90.111111,-160.222222", "098.20", "BZ4567", "2023-05-11T21:10:10Z")
//        srequest.send(NavigationUtils.getLocation(this), )
        srequest.send()
    }
}
