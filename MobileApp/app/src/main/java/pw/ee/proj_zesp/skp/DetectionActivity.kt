package pw.ee.proj_zesp.skp

import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Rect
import android.graphics.RectF
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.util.Size
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.AspectRatio
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageCapture
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.common.InputImage
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import com.googlecode.tesseract.android.TessBaseAPI
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Dispatchers.IO
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.opencv.android.Utils
import org.opencv.core.Core
import org.opencv.core.CvType
import org.opencv.core.CvType.CV_32F
import org.opencv.core.Mat
import org.opencv.core.MatOfFloat
import org.opencv.core.MatOfPoint
import org.opencv.core.Scalar
import org.opencv.imgproc.Imgproc
import pw.ee.proj_zesp.skp.detection.ORTAnalyzer
import pw.ee.proj_zesp.skp.detection.Result_Yolo_v8
import pw.ee.proj_zesp.skp.ocr.OCR_util
import pw.ee.proj_zesp.skp.ocr.OCR_util.Companion.checkBoxProportions
import pw.ee.proj_zesp.skp.ocr.OCR_util.Companion.parseOCRResults
import pw.ee.proj_zesp.skp.utils.*
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors


class DetectionActivity : AppCompatActivity(){
    private val backgroundExecutor: ExecutorService by lazy { Executors.newSingleThreadExecutor() }
    private val scope = CoroutineScope(Job() + Dispatchers.Main)

    private var ortEnv: OrtEnvironment? = null
    private var imageCapture: ImageCapture? = null
    private var imageAnalysis: ImageAnalysis? = null
    private var imagePreview: Preview? = null
    private var enableQuantizedModel: Boolean = false
    private var textBox : TextView? = null

    private var newBackgroundView : ImageView? = null
    private var boxView : ImageView? = null

    private lateinit var tess : TessBaseAPI
    private var startTime = System.currentTimeMillis()

    val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)


    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.detection_window)
        ortEnv = OrtEnvironment.getEnvironment()

        Navigation.navigation = NavigationUtils(this)

        // Request Camera permission
        if (allPermissionsGranted()) {
            startCamera()
        } else {
            ActivityCompat.requestPermissions(
                this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS
            )
        }
        textBox = findViewById<TextView>(R.id.textView5)
        newBackgroundView = findViewById(R.id.newBackgroundView)
        boxView = findViewById(R.id.boxView)

    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener(Runnable {
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            // Preview
            imagePreview = Preview.Builder()
//                    .setTargetAspectRatio(AspectRatio.RATIO_16_9)
                .setTargetResolution(Size(1080,1920))
                .build()
                .also {
//                        it.setSurfaceProvider(viewFinder.surfaceProvider)
                }

            imageCapture = ImageCapture.Builder()
                .setTargetAspectRatio(AspectRatio.RATIO_16_9)
//                    .setTargetResolution(Size(1080,1920))
//                .setTargetRotation(Surface.ROTATION_90)
                .build()

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            imageAnalysis = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
//                .setTargetAspectRatio(AspectRatio.RATIO_16_9)
                .setTargetResolution(Size(3840,2160))
//                    .setTargetRotation(Surface.ROTATION_0)
                .build()

            try {
                cameraProvider.unbindAll()

                cameraProvider.bindToLifecycle(
                    this, cameraSelector, imageCapture, imageAnalysis
                )
            } catch (exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }

            setORTAnalyzer()
        }, ContextCompat.getMainExecutor(this))
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all() {
        ContextCompat.checkSelfPermission(baseContext, it) == PackageManager.PERMISSION_GRANTED
    }

    override fun onDestroy() {
        super.onDestroy()
        backgroundExecutor.shutdown()
        ortEnv?.close()
    }

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                startCamera()
            } else {
                Toast.makeText(
                    this,
                    "Permissions not granted by the user.",
                    Toast.LENGTH_SHORT
                ).show()
                finish()
            }

        }
    }

    @SuppressLint("SetTextI18n")
    @RequiresApi(Build.VERSION_CODES.O)
    private fun updateUI(result: Result_Yolo_v8) {
        runOnUiThread{
            var timeNow = System.currentTimeMillis()
            var fps = 1.0/((timeNow - startTime).toDouble()/1000.0)
            startTime = timeNow
            textBox?.text = "FPS: "+ fps
//            val imageBitmap = viewFinder.bitmap ?: return@runOnUiThread
            val bitmapDrawable = result.bitmap_origin.copy(Bitmap.Config.ARGB_8888, true)
            val boxBitmap = Bitmap.createBitmap(bitmapDrawable.width, bitmapDrawable.height, Bitmap.Config.ARGB_8888, true);
//            val bit : Bitmap = Bitmap.createBitmap(bitmapDrawable.width, bitmapDrawable.height, Bitmap.Config.ALPHA_8, true)
            newBackgroundView?.setImageBitmap(bitmapDrawable)
            boxView?.setImageBitmap(boxBitmap)

//            Log.println(Log.INFO, "viewFinder", "height = ${viewFinder.height}, width = ${viewFinder.width}")
//            Log.println(Log.INFO, "viewFinder", "height = ${viewFinder.bitmap!!.height}, width = ${viewFinder.bitmap!!.width}")

            val canvas = Canvas(boxBitmap)
            val listRect : MutableList<RectF> = mutableListOf()

            if (result.number_of_boxes == 0) {
                return@runOnUiThread
            }

            var dstSize = result.bitmap_origin.width
            // Creating boxes
            for(i in 0 until result.number_of_boxes){
                val box = result.boxes[i]

                var left = box.getX1() * dstSize
                var top = box.getY1() * dstSize
                var right = box.getX2() * dstSize
                var bottom = box.getY2() * dstSize



                Log.println(Log.INFO, "Caught box", "x = ${box.x}, y = ${box.y}, width = ${box.width}, height = ${box.height}, probability = ${box.probability}")

                Log.println(Log.INFO, "INFO",
                    "$i. left = $left, top = $top, right  = $right, bottom = $bottom"
                )

                val rect = RectF(left, top, right, bottom)
                listRect.add(rect)
            }

            Log.println(Log.INFO,"INFO", "Number of boxes: " + result.number_of_boxes)

//                customView.drawBoxes(listRect, canvas)
            val paint = Paint().apply {
                color = Color.RED  // Set the box color to red
                style = Paint.Style.STROKE  // Set the paint style to stroke
                strokeWidth = 5f  // Set the stroke width to 4 pixels
            }

            for (rect in listRect)
            {
                canvas.drawRect(rect, paint)
            }
        }
    }

    // Read ort model into a ByteArray, run in background
    private suspend fun readModel(): ByteArray = withContext(Dispatchers.IO) {
        val modelID =
            if (enableQuantizedModel) R.raw.yolov8_320 else R.raw.yolov8_320
        resources.openRawResource(modelID).readBytes()
    }

    // Create a new ORT session in background
    private suspend fun createOrtSession(): OrtSession? = withContext(Dispatchers.Default) {
        ortEnv?.createSession(readModel())
    }

    // Create a new ORT session and then change the ImageAnalysis.Analyzer
    // This part is done in background to avoid blocking the UI
    @RequiresApi(Build.VERSION_CODES.O)
    private fun setORTAnalyzer(){
        scope.launch {
            imageAnalysis?.clearAnalyzer()
            imageAnalysis?.setAnalyzer(
                backgroundExecutor,
                ORTAnalyzer(createOrtSession(), ::updateUI)
            )
        }
    }

    companion object {
        public const val TAG = "Analyzer"
        private const val REQUEST_CODE_PERMISSIONS = 10
        private val REQUIRED_PERMISSIONS = arrayOf(android.Manifest.permission.CAMERA)
    }

}