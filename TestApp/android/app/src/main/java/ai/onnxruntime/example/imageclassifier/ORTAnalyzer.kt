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


internal data class Result(
        var detectedIndices: List<Int> = emptyList(),
        var detectedScore: MutableList<Float> = mutableListOf<Float>(),
        var rateFPS: Double = 0.0
) {}



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


    private var startTime = SystemClock.uptimeMillis()
    private var endTime = startTime

    private var savedImage: Bitmap? = null
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
    // Get index of top 3 values
    // This is for demo purpose only, there are more efficient algorithms for topK problems
    private fun getTop3(labelVals: FloatArray): List<Int> {
        var indices = mutableListOf<Int>()
        for (k in 0..2) {
            var max: Float = 0.0f
            var idx: Int = 0
            for (i in 0..labelVals.size - 1) {
                val label_val = labelVals[i]
                if (label_val > max && !indices.contains(i)) {
                    max = label_val
                    idx = i
                }
            }

            indices.add(idx)
        }

        return indices.toList()
    }

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
            Log.println(Log.INFO, "TEST", "I'm before env use")
            env.use {
                val tensor = OnnxTensor.createTensor(env, imgData, shape)
                Log.println(Log.INFO, "TEST", "I'm before tensor use")
                tensor.use {
                    val output = ortSession?.run(Collections.singletonMap(inputName, tensor))
//                    OnnxTensorLike = output?.get(0)
                    Log.println(Log.INFO, "TEST", "I'm before output check")
                    if (output != null) {
                        Log.println(Log.INFO, "TEST", "I'm before mapping result")
                        result = mapToResult(output, 0.6, currentFPS, bitmap)
                    }
//                    output.use {
//
//
////                        endTime = SystemClock.uptimeMillis()
////                        result.rateFPS = (1000.0)/(endTime - startTime)
////                        startTime = endTime
////                        @Suppress("UNCHECKED_CAST")
////                        val rawOutput = ((output?.get(0)?.value) as Array<FloatArray>)[0]
//////                        val probabilities = softMax(rawOutput[0])
////                        result.detectedIndices = getTop3(probabilities)
////                        for (idx in result.detectedIndices) {
////                            result.detectedScore.add(probabilities[idx])
////                        }
//                    }
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
            if(tempOutput[0][4][i] > threshold)
            {
                var tempBox = YoloBox(tempOutput[0][0][i]/640,tempOutput[0][1][i]/640,tempOutput[0][2][i]/640,tempOutput[0][3][i]/640,tempOutput[0][4][i])
                listOfBoxes.add(tempBox)
            }
        }
        Log.println(Log.INFO, "Number_Of_Boxes", "Number of Boxes = ${listOfBoxes.size}")


        if(listOfBoxes.size > 0)
        {
            var box = listOfBoxes[0]
            var x : Int
            var y : Int
            var width : Int
            var height : Int

            x = (box.x*640).toInt()
            y = (box.y*640).toInt()

            if(x + (box.width*640).toInt() > bitmap.width) { width = bitmap.width - x }
            else { width = (box.width*640).toInt() }

            if(y + (box.height*640).toInt() > bitmap.height) { height = bitmap.height - y}
            else { height = (box.height*640).toInt() }

            var newBitmap = Bitmap.createBitmap(bitmap, x, y, width, height)

            return Result_Yolo_v8(listOfBoxes.size,listOfBoxes,currentFPS, newBitmap)
        }

        return Result_Yolo_v8(listOfBoxes.size,listOfBoxes,currentFPS, bitmap)
    }


    // Calculate the SoftMax for the input array
    private fun softMax(modelResult: FloatArray): FloatArray {
        val labelVals = modelResult.copyOf()
        val max = labelVals.max()
        var sum = 0.0f

        // Get the reduced sum
        for (i in labelVals.indices) {
            labelVals[i] = exp(labelVals[i] - max!!)
            sum += labelVals[i]
        }

        if (sum != 0.0f) {
            for (i in labelVals.indices) {
                labelVals[i] /= sum
            }
        }

        return labelVals
    }

    // Rotate the image of the input bitmap
    fun Bitmap.rotate(degrees: Float): Bitmap {
        val matrix = Matrix().apply { postRotate(degrees) }
        return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
    }

    override fun analyze(image: ImageProxy) {
//        canBeClose = false
        frameCount++

        // Convert the input image to bitmap and resize to 224x224 for model input
        imageProxy = image
        Log.println(Log.INFO, "Image details - before changes", "Height = ${image.height}, Width = ${image.width}")

        val imgBitmap = image.toBitmap()
        //calculete start y and calculate sizes
        var startX = 0
        var startY = 0
        var dstSize = 0
        if(image.width > image.height){
            dstSize = image.height
            startY = 0
            startX = image.width/2 - dstSize/2
        }
        else
        {
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