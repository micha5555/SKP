// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

package ai.onnxruntime.example.imageclassifier

import ai.onnxruntime.*
import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.graphics.*
import android.hardware.camera2.CameraMetadata
import android.hardware.camera2.CaptureRequest
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.util.Size
import android.view.Surface
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.camera2.Camera2Config
import androidx.camera.camera2.interop.Camera2Interop
import androidx.camera.camera2.interop.Camera2Interop.Extender
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.constraintlayout.solver.widgets.Rectangle
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

    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)


//        ProcessCameraProvider.configureInstance(
//            CameraXConfig.Builder.fromConfig(Camera2Config.defaultConfig())
//                .build()
//
//        );
        cameraProviderFuture.addListener(Runnable {
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            // Preview
            imagePreview = Preview.Builder()
//                    .setTargetAspectRatio(AspectRatio.RATIO_16_9)
                    .setTargetResolution(Size(1080,1920))
                    .build()
                    .also {
                        it.setSurfaceProvider(viewFinder.surfaceProvider)
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
                    .setTargetResolution(Size(1080,1920))
//                    .setTargetRotation(Surface.ROTATION_0)
                    .build()

            try {
                cameraProvider.unbindAll()

                cameraProvider.bindToLifecycle(
                        this, cameraSelector, imagePreview, imageCapture, imageAnalysis
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

//    @SuppressLint("UnsafeOptInUsageError")
//    fun buildImageAnalysis() : ImageAnalysis {
//        val builder = ImageAnalysis.Builder()
//        val camera2InterOp = Extender(builder)
//        camera2InterOp.setCaptureRequestOption(CaptureRequest.SENSOR_FRAME_DURATION, 2500000000)
////        camera2InterOp.setCaptureRequestOption(CaptureRequest.SENSOR_EXPOSURE_TIME, EXPOSURE_TIME_LIMIT_NS)
//        return builder.build()
//    }

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
            //Draw boxes
            val imageBitmap = viewFinder.bitmap ?: return@runOnUiThread
            newBackgroundView.setImageBitmap(result.bitmap_origin)

            Log.println(Log.INFO, "viewFinder", "height = ${viewFinder.height}, width = ${viewFinder.width}")
            Log.println(Log.INFO, "viewFinder", "height = ${viewFinder.bitmap!!.height}, width = ${viewFinder.bitmap!!.width}")

//            val newBitmap = Bitmap.createBitmap(imageBitmap.width,imageBitmap.height, Bitmap.Config.ARGB_8888,true)
            val canvas = Canvas(result.bitmap_origin)

            val listRect : MutableList<RectF> = mutableListOf()


            if (result.number_of_boxes == 0) {
                customView.drawBoxes(listRect)
                customView.draw(canvas)
                return@runOnUiThread
            }

            var dstSize = result.bitmap_origin.width

//                dstSize = if(imageBitmap.width > imageBitmap.height) {
//                    imageBitmap.height
//                } else {
//                    imageBitmap.width
//                }
                // Creating boxes
                for(i in 0 until result.number_of_boxes){
                    val box = result.boxes[i]

                    var left = box.getX1() * dstSize
                    var top = box.getY1() * dstSize
                    var right = box.getX2() * dstSize
                    var bottom = box.getY2() * dstSize

//                    if(imageBitmap.width > imageBitmap.height)
//                    {
//                        left += imageBitmap.height / 2
//                        right += imageBitmap.height / 2
//                    }
//                    else
//                    {
//                        top += imageBitmap.width / 2
//                        bottom += imageBitmap.height / 2
//                    }


                    Log.println(Log.INFO, "Caught box", "x = ${box.x}, y = ${box.y}, width = ${box.width}, height = ${box.height}, probability = ${box.probability}")

                    Log.println(Log.INFO, "INFO",
                        "$i. left = $left, top = $top, right  = $right, bottom = $bottom"
                    )

                    //TODO: Move plane

                    val rect = RectF(left, top, right, bottom)
                    listRect.add(rect)
//                canvas.drawRect(rect,paint)
                }

                Log.println(Log.INFO,"INFO", "Number of boxes: " + result.number_of_boxes)

//                inference_time_value.text = "%.2f".format(result.currentFPS ) + " FPS"
                customView.drawBoxes(listRect)
                customView.draw(canvas)
            }


        }

//        runOnUiThread {
//            percentMeter.progress = (result.detectedScore[0] * 100).toInt()
////            detected_item_1.text = labelData[result.detectedIndices[0]]
//            detected_item_value_1.text = "%.2f%%".format(result.detectedScore[0] * 100)
//
//            if (result.detectedIndices.size > 1) {
////                detected_item_2.text = labelData[result.detectedIndices[1]]
//                detected_item_value_2.text = "%.2f%%".format(result.detectedScore[1] * 100)
//            }
//
//            if (result.detectedIndices.size > 2) {
////                detected_item_3.text = labelData[result.detectedIndices[2]]
//                detected_item_value_3.text = "%.2f%%".format(result.detectedScore[2] * 100)
//            }
//
//            inference_time_value.text = "%.2f".format(result.rateFPS ) + " FPS"
//        }


    // Read MobileNet V2 classification labels
    private fun readLabels(): List<String> {
        return resources.openRawResource(R.raw.imagenet_classes).bufferedReader().readLines()
    }

    // Read ort model into a ByteArray, run in background
    private suspend fun readModel(): ByteArray = withContext(Dispatchers.IO) {
        val modelID =
            if (enableQuantizedModel) R.raw.yolov8_best else R.raw.yolov8_best
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
