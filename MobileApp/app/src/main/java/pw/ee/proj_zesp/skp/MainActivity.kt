package pw.ee.proj_zesp.skp

import android.content.Intent
import android.graphics.drawable.Drawable
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ImageButton
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatDelegate
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import androidx.core.content.ContextCompat
import java.io.*

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
    }
}
