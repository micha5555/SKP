package pw.ee.proj_zesp.skp.utils

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Bundle
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class NavigationUtils {

    companion object {

        public fun requestLocationPermissions(context: Context) {
            if (ContextCompat.checkSelfPermission(context,
                    Manifest.permission.ACCESS_FINE_LOCATION
                ) !==
                PackageManager.PERMISSION_GRANTED) {
                if (ActivityCompat.shouldShowRequestPermissionRationale(
                        context as Activity,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    )) {
                    ActivityCompat.requestPermissions(context,
                        arrayOf(
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                        ), 1)
                } else {
                    ActivityCompat.requestPermissions(context,
                        arrayOf(
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                        ), 1)
                }
            }
        }
        @SuppressLint("MissingPermission")
        fun getLocation(context: Context): String? {
            // Get the location manager and check if location services are enabled
            val locationManager =
                context.getSystemService(Context.LOCATION_SERVICE) as LocationManager

            val locationListener = object : LocationListener {
                override fun onLocationChanged(location: Location) {
                    // Handle updated location data here
                }

                override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}

                override fun onProviderEnabled(provider: String) {}

                override fun onProviderDisabled(provider: String) {}
            }

            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                0L,
                0f,
                locationListener
            )

            if (!locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
                Toast.makeText(context, "GPS is not enabled", Toast.LENGTH_SHORT).show()
                return null
            }

            val providers = locationManager.getProviders(true)
            // Get the last known location and return it as a string
            var bestLocation: Location? = null
            for (provider in providers) {
                val l: Location? = locationManager.getLastKnownLocation(provider)
                if (l == null) {
                    continue
                }

                if (bestLocation == null || l.accuracy < bestLocation.accuracy) {
                    bestLocation = l
                }

                if (bestLocation != null) {
                    val latitude = bestLocation.latitude
                    val longitude = bestLocation.longitude
                    return "$latitude,$longitude"
                }
            }
            return null
        }

    }
}