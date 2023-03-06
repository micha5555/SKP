package pw.ee.proj_zesp.skp

import android.Manifest.permission.*
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.Camera
import android.hardware.camera2.CameraCharacteristics
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.SurfaceView
import android.view.WindowManager.LayoutParams.FLAG_FORCE_NOT_FULLSCREEN
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import org.opencv.android.*
import org.opencv.core.CvType
import org.opencv.core.Mat

//Permission vars:
private const val REQUEST_CODE_PERMISSIONS = 111
private val REQUIRED_PERMISSIONS = arrayOf(CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, RECORD_AUDIO, ACCESS_FINE_LOCATION)

class MainActivity : AppCompatActivity(), CameraBridgeViewBase.CvCameraViewListener2 {

    private val viewFinder by lazy { findViewById<JavaCamera2View>(R.id.CameraView) }
//    lateinit var cvBaseLoaderCallback: BaseLoaderCallback
    lateinit var imageMat: Mat
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

//        window.clearFlags(FLAG_FORCE_NOT_FULLSCREEN)

        setContentView(R.layout.sample_camera)

        ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS)
        if (allPermissionsGranted()) {
            checkOpenCV(this)
        } else {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS)
        }

        viewFinder.setCameraPermissionGranted()
        viewFinder.visibility = SurfaceView.VISIBLE
        viewFinder.setCameraIndex(CameraCharacteristics.LENS_FACING_FRONT)
        viewFinder.setCvCameraViewListener(this)
        viewFinder.enableView()


//        cvBaseLoaderCallback = object : BaseLoaderCallback(this){
//            override fun onManagerConnected(status: Int) {
//                when(status){
//                    SUCCESS -> {
//                        lgi(OPENCV_SUCCESSFUL)
//                        shortMsg(this@MainActivity, OPENCV_SUCCESSFUL)
//                        viewFinder.enableView()
//                    }
//                    else -> super.onManagerConnected(status)
//                }
//            }
//        }
    }

    override fun onPause() {
        super.onPause()
        viewFinder?.let {viewFinder.disableView()}
    }

    override fun onDestroy() {
        super.onDestroy()
        viewFinder?.let {viewFinder.disableView()}
    }

    override fun onResume() {
        super.onResume()
//        OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION, this, cvBaseLoaderCallback)
        checkOpenCV(this)
        viewFinder?.let{viewFinder.enableView()}
    }

    override fun onCameraViewStarted(width: Int, height: Int) {
        imageMat = Mat(width,height,CvType.CV_8UC4)
    }

    override fun onCameraViewStopped() {
        imageMat.release()
    }

    override fun onCameraFrame(inputFrame: CameraBridgeViewBase.CvCameraViewFrame?): Mat {
        imageMat = inputFrame!!.rgba()
        return imageMat
    }

    private fun checkOpenCV(context: Context) =
        if (OpenCVLoader.initDebug()) {
            shortMsg(
                context,
                OPENCV_SUCCESSFUL
            )
            viewFinder.enableView()
        }

        else shortMsg(context, OPENCV_FAIL)

    private fun allPermissionsGranted() =
        REQUIRED_PERMISSIONS.all {
            ContextCompat.checkSelfPermission(baseContext, it) == PackageManager.PERMISSION_GRANTED
        }

    companion object {
        val TAG = "MYLOG " + MainActivity::class.java.simpleName
        fun lgd(s: String) = Log.d(TAG, s)
        fun lge(s: String) = Log.e(TAG, s)
        fun lgi(s: String) = Log.i(TAG, s)
        fun shortMsg(context: Context, s: String) =
            Toast.makeText(context, s, Toast.LENGTH_SHORT).show()


        // mesasages:
        private const val OPENCV_SUCCESSFUL = "OpenCV Loaded Successfully!"
        private const val OPENCV_FAIL = "Could not load OpenCV!!!"
        private const val OPENCV_PROBLEM = "There's a problem in OpenCV."
        private const val PERMISSION_NOT_GRANTED = "Permissions not granted by the user."

    }

}

