// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

package ai.onnxruntime.example.imageclassifier

import ai.onnxruntime.*
import ai.onnxruntime.example.imageclassifier.Analyzer.ORTAnalyzer
import ai.onnxruntime.example.imageclassifier.Analyzer.Result_Yolo_v8
import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.*
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.util.Size
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.*
import java.lang.Runnable
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {
    private val backgroundExecutor: ExecutorService by lazy { Executors.newSingleThreadExecutor() }
    private val labelData: List<String> by lazy { readLabels() }
    private val scope = CoroutineScope(Job() + Dispatchers.Main)

    private var ortEnv: OrtEnvironment? = null
    private var imageCapture: ImageCapture? = null
    private var imageAnalysis: ImageAnalysis? = null
    private var imagePreview: Preview? = null
    private var enableQuantizedModel: Boolean = false
    private var textBox : TextView? = null;

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        ortEnv = OrtEnvironment.getEnvironment()

        // Request Camera permission
        if (allPermissionsGranted()) {
            startCamera()
        } else {
            ActivityCompat.requestPermissions(
                    this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS
            )
        }
        textBox = findViewById<TextView>(R.id.textView5);

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

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
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
            textBox?.text = "FPS: "+ result.currentFPS.toString();
//            val imageBitmap = viewFinder.bitmap ?: return@runOnUiThread
            val bitmapDrawable = result.bitmap_origin.copy(Bitmap.Config.ARGB_8888, true)
            val boxBitmap = Bitmap.createBitmap(bitmapDrawable.width, bitmapDrawable.height, Bitmap.Config.ARGB_8888, true);
//            val bit : Bitmap = Bitmap.createBitmap(bitmapDrawable.width, bitmapDrawable.height, Bitmap.Config.ALPHA_8, true)
            newBackgroundView.setImageBitmap(bitmapDrawable)
            boxView.setImageBitmap(boxBitmap)

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

    // Read MobileNet V2 classification labels
    private fun readLabels(): List<String> {
        return resources.openRawResource(R.raw.imagenet_classes).bufferedReader().readLines()
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
        public const val TAG = "ORTImageClassifier"
        private const val REQUEST_CODE_PERMISSIONS = 10
        private val REQUIRED_PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
