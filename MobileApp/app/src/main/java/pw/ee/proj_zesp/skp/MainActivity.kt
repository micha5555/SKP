package pw.ee.proj_zesp.skp

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.Settings
import android.util.Log
import android.view.View
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.location.LocationManagerCompat.getCurrentLocation
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import java.io.*
import java.time.LocalTime

class MainActivity : AppCompatActivity() {

//    private lateinit var fusedLocationProvideClient : FusedLocationProviderClient
    private lateinit var tvLatitude : TextView
    private lateinit var tvLongitude : TextView

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {

        getSupportActionBar()?.hide()
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_menu)

        tvLatitude = findViewById(R.id.textView2)
        tvLongitude = findViewById(R.id.textView3)
        Log.i("localisat", NavigationUtils.getLocation(this ).toString())
        tvLatitude.text = NavigationUtils.getLocation(this )

        val testlocalisation: ImageButton = findViewById(R.id.start_control_button_on_menuview)
        testlocalisation.setOnClickListener {
            val localisation : String = NavigationUtils.getLocation(this ).toString()
            Log.i("localisat", localisation)
            tvLatitude.text = localisation

            writeToFile(this, "example5.txt", localisation + "  " + LocalTime.now() + "\n")
            Log.i("content of file", readFromFile(this, "example5.txt"))
            println(readFromFile(this, "example5.txt"))
        }

        val aboutAppButton: ImageButton = findViewById<ImageButton>(R.id.about_system_button)
        aboutAppButton.setOnClickListener {
            val intent = Intent(this, AboutAppActivity::class.java)
            this.startActivity(intent)
        }
    }


    fun writeToFile(context : Context, fileName: String, data: String) {
        val file = File(context.filesDir, fileName)
        if (!file.exists()) {
            file.createNewFile()
        }
        FileOutputStream(file, true).use {
            it.write(data.toByteArray())
        }
    }

    fun readFromFile(context : Context, fileName: String): String {
        val file = File(context.filesDir, fileName)
        val reader = BufferedReader(FileReader(file))
        val stringBuilder = StringBuilder()
        var line: String?
        while (reader.readLine().also { line = it } != null) {
            stringBuilder.append(line)
        }
        reader.close()
        return stringBuilder.toString()
    }

}
