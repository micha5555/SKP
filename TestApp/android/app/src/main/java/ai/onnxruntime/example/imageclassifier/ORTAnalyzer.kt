// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

package ai.onnxruntime.example.imageclassifier

import ai.onnxruntime.*
import android.graphics.Bitmap
import android.graphics.Matrix
import android.os.CountDownTimer
import android.os.SystemClock
import android.util.Log
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import java.util.*
import kotlin.math.exp

internal data class Result_Yolo_v8(
    var number_of_boxes: Int = 0,
    var boxes: List<YoloBox> = emptyList(),
    var currentFPS: Double = 0.0,
    var bitmap_origin: Bitmap
)

internal class ORTAnalyzer(
    private val ortSession: OrtSession?,
    private val callBack: (Result_Yolo_v8) -> Unit
) : ImageAnalysis.Analyzer {

    // Patameters
    private val CurrentThreshold = 0.5

    private var startTime = SystemClock.uptimeMillis()
    private var endTime = startTime

    private var imageProxy: ImageProxy? = null

    private var frameCount: Int = 0

    private val desiredFps = 50

    private var currentFPS = 0.0
    private var canBeClose = false


    val processingTimer = object : CountDownTimer(Long.MAX_VALUE, (1000 / desiredFps).toLong()) {
        override fun onTick(millisUntilFinished: Long) {
//            Log.println(Log.INFO,"INFO", "In realAnalyze")
//            realAnalyze()
//            Log.println(Log.INFO, "Frame" ,frameCount.toString())

            if(frameCount == desiredFps){
                endTime = SystemClock.uptimeMillis()
                currentFPS = (desiredFps*1000).toDouble()/(endTime - startTime).toDouble()
                Log.println(Log.INFO, "FPS" ,currentFPS.toString())
                frameCount=0
                startTime = endTime
            }
            if(canBeClose){
                imageProxy?.close()
                canBeClose=false
            }


        }

        override fun onFinish() {}
    }.apply { start() }

    private fun realAnalyze(bitmap: Bitmap?)
    {
        Log.println(Log.INFO, "TEST", "I'm in realAnalyze")

        if (bitmap != null) {
            var result = Result_Yolo_v8(bitmap_origin = bitmap)

            Log.println(Log.INFO, "TEST", "I'm before preProcess")

            val imgData = preProcess(bitmap)
            val inputName = ortSession?.inputNames?.iterator()?.next()
            val shape = longArrayOf(1, 3, 640, 640)
            val env = OrtEnvironment.getEnvironment()

            env.use {
                val tensor = OnnxTensor.createTensor(env, imgData, shape)

                tensor.use {
                    val output = ortSession?.run(Collections.singletonMap(inputName, tensor))

                    if (output != null) {
                        result = mapToResult(output, CurrentThreshold, currentFPS, bitmap)
                    }
                }
            }
            callBack(result)
        }
    }

    private fun mapToResult(rawOutput: OrtSession.Result, threshold: Double, currentFPS: Double, bitmap: Bitmap): Result_Yolo_v8{
        Log.println(Log.INFO, "TEST", "I'm in mapping result")
        var output = rawOutput.get(0)
        var tempOutput = output.value as Array<Array<FloatArray>>
        var listOfBoxes: MutableList<YoloBox> = mutableListOf<YoloBox>()
        for (i in 0 until (tempOutput[0][0]).size)
        {
            val x_center = tempOutput[0][0][i]/640
            val y_center = tempOutput[0][1][i]/640
            val width = tempOutput[0][2][i]/640
            val height = tempOutput[0][3][i]/640
            val probability = tempOutput[0][4][i]

            if(probability > threshold)
            {
                var tempBox = YoloBox(x_center - width/2, y_center - height/2, width, height, probability)
                listOfBoxes.add(tempBox)
            }
        }
        Log.println(Log.INFO, "Number_Of_Boxes", "Number of Boxes = ${listOfBoxes.size}")

//      This code returns croped image of origin bitmap to first boundingbox
//        if(listOfBoxes.size > 0)
//        {
//            var box = listOfBoxes[0]
//            var x : Int
//            var y : Int
//            var width : Int
//            var height : Int
//
//            x = (box.x*640).toInt()
//            y = (box.y*640).toInt()
//
//            if(x + (box.width*640).toInt() > bitmap.width) { width = bitmap.width - x }
//            else { width = (box.width*640).toInt() }
//
//            if(y + (box.height*640).toInt() > bitmap.height) { height = bitmap.height - y}
//            else { height = (box.height*640).toInt() }
//
//            var newBitmap = Bitmap.createBitmap(bitmap, x, y, width, height)
//
//            return Result_Yolo_v8(listOfBoxes.size,listOfBoxes,currentFPS, newBitmap)
//        }

        return Result_Yolo_v8(listOfBoxes.size,listOfBoxes,currentFPS, bitmap)
    }

    // Rotate the image of the input bitmap
    fun Bitmap.rotate(degrees: Float): Bitmap {
        val matrix = Matrix().apply { postRotate(degrees) }
        return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
    }

    override fun analyze(image: ImageProxy) {
        frameCount++

        // Convert the input image to bitmap and resize to 640x640 for model input
        imageProxy = image
        Log.println(Log.INFO, "Image details - before changes", "Height = ${image.height}, Width = ${image.width}")

        val imgBitmap = image.toBitmap()

        var startX = 0
        var startY = 0
        var dstSize = 0
        if(image.width > image.height){
            dstSize = image.height
            startY = 0
            startX = image.width/2 - dstSize/2
        }
        else {
            dstSize = image.width
            startX = 0
            startY = image.height/2 - dstSize/2
        }

        Log.println(Log.INFO, "Crop Details", "dstSize = ${dstSize}, startX = ${startX}, startY = $startY")

        val stepBitmap = imgBitmap?.let { Bitmap.createBitmap(it, startX, startY,dstSize,dstSize) }
        val rawBitmap = stepBitmap?.let { Bitmap.createScaledBitmap(it, 640, 640, false) }
        val bitmap = rawBitmap?.rotate(90.0F)
//        val bitmap = rawBitmap?.rotate(image.imageInfo.rotationDegrees.toFloat())
        canBeClose = true

        realAnalyze(bitmap)

    }

    // We can switch analyzer in the app, need to make sure the native resources are freed
    protected fun finalize() {
        ortSession?.close()
    }
}