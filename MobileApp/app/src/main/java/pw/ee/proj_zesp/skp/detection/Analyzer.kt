package pw.ee.proj_zesp.skp.detection


import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import android.graphics.Bitmap
import android.os.CountDownTimer
import android.os.SystemClock
import android.util.Log
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import org.opencv.android.Utils
import org.opencv.core.Algorithm
import org.opencv.tracking.legacy_MultiTracker
import org.opencv.core.Mat
import org.opencv.core.MatOfByte
import org.opencv.core.MatOfFloat
import org.opencv.core.MatOfPoint2f
import org.opencv.core.Point
import org.opencv.core.Rect
import org.opencv.core.Rect2d
import org.opencv.tracking.TrackerKCF
import org.opencv.tracking.legacy_TrackerKCF
import org.opencv.video.Tracker
import org.opencv.tracking.legacy_TrackerMedianFlow
import org.opencv.video.Video
import pw.ee.proj_zesp.skp.track.CustomMultiTracker
//import org.opencv.core.Algorithm
import pw.ee.proj_zesp.skp.utils.addBoxToListIfNewOrBetter
import pw.ee.proj_zesp.skp.utils.isOverlaping
import pw.ee.proj_zesp.skp.utils.preProcess
import pw.ee.proj_zesp.skp.utils.rotate
import pw.ee.proj_zesp.skp.utils.toBitmap
import java.util.*


data class Result_Yolo_v8(
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

    private var imageProxy: ImageProxy? = null
    private var originImage : Bitmap? = null

//    private var tracker = TrackerDaSiamRPN.create()
    private var multiTracker: CustomMultiTracker = CustomMultiTracker()

    private var frameCount: Int = 0
    private var previousFrameCount: Int = 0
    private var currentFPS = 0.0
    private var canBeClose = false

    private var lastResult: Result_Yolo_v8? = null

    private var previousMatImage: Mat? = null;
    private var currentMatImage: Mat? = null;

    // Patameters
    private val currentThreshold = 0.6
    private val desiredFps = 1000
    private var sizeOfImage : Long = 320

    private var detectionEveryXFrame: Int = 3
    private var checkFPSEveryXFrame: Int = 5

    private var factorOfProbabilityInOpticalFlow: Float = 0.9F


    //TODO: Probably need to be reworked
    val processingTimer = object : CountDownTimer(Long.MAX_VALUE, (1000 / desiredFps).toLong()) {
        override fun onTick(millisUntilFinished: Long) {
//            Log.println(Log.INFO,"INFO", "In realAnalyze")
//            realAnalyze()
//            Log.println(Log.INFO, "Frame" ,frameCount.toString())
            val currentFrame = frameCount - previousFrameCount;

            if(currentFrame == checkFPSEveryXFrame){
                endTime = SystemClock.uptimeMillis()
                currentFPS = (checkFPSEveryXFrame*1000).toDouble()/(endTime - startTime).toDouble()
                Log.println(Log.INFO, "FPS" ,currentFPS.toString())
                previousFrameCount = frameCount
                startTime = endTime
            }
            if(canBeClose){
                imageProxy?.close()
                canBeClose=false
            }
        }
        override fun onFinish() {}
    }.apply { start() }

    override fun analyze(image: ImageProxy) {
        frameCount++
        val bitmap = imagePreparation(image);
        val originBitmap = originImage


        if(bitmap == null)
            return
        if(originImage == null)
            return
        if(originBitmap == null)
            return

        if(frameCount % detectionEveryXFrame == 0 || lastResult == null)
            realAnalyze(bitmap)
        else
        {
            //            opticalFlow(bitmap)
            multiTracker.update(originBitmap, originBitmap )
            var result = multiTracker.generateResult()
            callBack(result)
        }

        canBeClose = true
        previousMatImage = currentMatImage;
    }

    private fun trackingObjects(bitmap: Bitmap) {

    }

    private fun opticalFlow(bitmap: Bitmap) {
        if (previousMatImage == null || currentMatImage == null)
            return
        if(lastResult == null)
            return
        if(lastResult!!.boxes.isEmpty())
        {
            callBack(Result_Yolo_v8(0, emptyList(),currentFPS,originImage!!))
            return
        }


        val resultPoints = MatOfPoint2f()
        val status = MatOfByte()
        val err = MatOfFloat()
        Video.calcOpticalFlowPyrLK(
            previousMatImage, currentMatImage,
            calcMatPointsFromResults(lastResult!!),
            resultPoints, status, err)

        val result = calcResultsFromMatPoints(resultPoints, status, lastResult!! )
        lastResult = result

        callBack(result)
    }

    private fun calcMatFromBitmap(bitmap: Bitmap) : Mat
    {
        val mat = Mat()
        val bmp32: Bitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true)
        Utils.bitmapToMat(bmp32, mat)
        return mat
    }

    private fun calcResultsFromMatPoints(points: MatOfPoint2f, status: MatOfByte, prevResult: Result_Yolo_v8) : Result_Yolo_v8
    {
        val newBoxes: MutableList<YoloBox> = mutableListOf()
        val statusArray = status.toArray()
        val pointsArray = points.toArray()
        for(i in 0 until prevResult.boxes.size)
        {
            var p1Index = i*2
            var p2Index = i*2 + 1

            //Status Mat - 1: Found, 0: Lost
            if(statusArray[p1Index].toInt() == 0 || statusArray[p2Index].toInt() == 0)
                continue;

            val oldBoxProbability = prevResult.boxes[i].probability

            val p1 = Point(
                (pointsArray[p1Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
                (pointsArray[p1Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
            val p2 = Point(
                (pointsArray[p2Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
                (pointsArray[p2Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())

            val newWidth = p2.x - p1.x
            val newHeight = p2.y - p1.y

            val newBox = YoloBox(
                p1.x.toFloat(), p1.y.toFloat(),
                newWidth.toFloat(), newHeight.toFloat(),
                oldBoxProbability)

            newBoxes.add(newBox)
        }

        val result = Result_Yolo_v8(newBoxes.size, newBoxes, currentFPS, originImage!!)
        return result
    }

    private fun calcMatPointsFromResults(result: Result_Yolo_v8) : MatOfPoint2f
    {
        //Currently we are taking only 2 points - maybe 4 are better?
        //Left upper corner and right lower corner of box
        val points: MutableList<Point> = mutableListOf()
        for(oldBox in result.boxes)
        {
            val p1 = Point(oldBox.x.toDouble()*result.bitmap_origin.width, oldBox.y.toDouble()*result.bitmap_origin.height)
            val p2 = Point((oldBox.x+oldBox.width).toDouble()*result.bitmap_origin.width, (oldBox.y + oldBox.height).toDouble()*result.bitmap_origin.height)

            points.add(p1)
            points.add(p2)

//            val newProbability = oldBox.probability * factorOfProbabilityInOpticalFlow
//            if(newProbability > currentThreshold)
//            {
//                val newBox = YoloBox(oldBox.x,oldBox.y, oldBox.width,oldBox.height,newProbability)
//                newListOfBoxes.add(newBox)
//            }

//            val newBox = YoloBox(oldBox.x, oldBox.y, oldBox.width, oldBox.height, oldBox.probability)
//            newListOfBoxes.add(newBox)
        }
//        val newResult = Result_Yolo_v8()
        val matPoints = MatOfPoint2f()
        matPoints.fromList(points)
        return  matPoints
    }

    private fun realAnalyze(bitmap: Bitmap)
    {
        Log.println(Log.INFO, "TEST", "I'm in realAnalyze")

        var result = Result_Yolo_v8(bitmap_origin = bitmap)

        Log.println(Log.INFO, "TEST", "I'm before preProcess")

        val imgData = preProcess(bitmap)
        val inputName = ortSession?.inputNames?.iterator()?.next()
        val shape = longArrayOf(1, 3, sizeOfImage, sizeOfImage)
        val env = OrtEnvironment.getEnvironment()

        env.use {
            val tensor = OnnxTensor.createTensor(env, imgData, shape)

            tensor.use {
                val output = ortSession?.run(Collections.singletonMap(inputName, tensor))

                if (output != null) {
                    result = mapToResult(output, currentThreshold, currentFPS, bitmap)
                }
            }
        }
        multiTracker.add(result, originImage!!)
        val trackerResult = multiTracker.generateResult()
        lastResult = trackerResult
        callBack(trackerResult)
    }

    private fun mapToResult(rawOutput: OrtSession.Result, threshold: Double, currentFPS: Double, bitmap: Bitmap): Result_Yolo_v8 {
        Log.println(Log.INFO, "TEST", "I'm in mapping result")
        val output = rawOutput.get(0)
        val tempOutput = output.value as Array<Array<FloatArray>>
        val listOfBoxes: MutableList<YoloBox> = mutableListOf<YoloBox>()
        for (i in 0 until (tempOutput[0][0]).size)
        {
            val x_center = tempOutput[0][0][i]/sizeOfImage
            val y_center = tempOutput[0][1][i]/sizeOfImage
            val width = tempOutput[0][2][i]/sizeOfImage
            val height = tempOutput[0][3][i]/sizeOfImage
            val probability = tempOutput[0][4][i]

            if(probability > threshold)
            {
                val tempBox = YoloBox(x_center - width/2, y_center - height/2, width, height, probability)
                addBoxToListIfNewOrBetter(listOfBoxes, tempBox);
            }
        }
        Log.println(Log.INFO, "Number_Of_Boxes", "Number of Boxes = ${listOfBoxes.size}")
        val toSend : Bitmap = originImage ?: bitmap

        return Result_Yolo_v8(listOfBoxes.size,listOfBoxes,currentFPS, toSend)
    }

    fun imagePreparation(image: ImageProxy) : Bitmap?{
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
        val bitBitmap = stepBitmap?.rotate(90.0F)
        currentMatImage = bitBitmap?.let { calcMatFromBitmap(it) };
        originImage = bitBitmap
        val bitmap = bitBitmap?.let { Bitmap.createScaledBitmap(it, sizeOfImage.toInt(), sizeOfImage.toInt(), false) }
//        val bitmap = rawBitmap?.rotate(90.0F)
//        val bitmap = rawBitmap?.rotate(image.imageInfo.rotationDegrees.toFloat())
        return bitmap;
    }



    // We can switch analyzer in the app, need to make sure the native resources are freed
    protected fun finalize() {
        ortSession?.close()
    }
}