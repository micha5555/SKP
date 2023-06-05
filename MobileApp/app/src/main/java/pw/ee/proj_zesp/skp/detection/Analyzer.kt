package pw.ee.proj_zesp.skp.detection


import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import android.graphics.Bitmap
import android.os.SystemClock
import android.util.Log
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageProxy
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import org.opencv.core.Mat
import pw.ee.proj_zesp.skp.utils.addBoxToListIfNewOrBetter
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

    private var frameCount: Int = 0
    private var previousFrameCount: Int = 0
    private var currentFPS = 0.0
    private var canBeClose = false

    private var lastResult: Result_Yolo_v8? = null

    private var previousMatImage: Mat? = null;
    private var currentMatImage: Mat? = null;

    private var detectionJob: Job? = null;
    private var opticalFLowJob: Job? = null;

    private var queueOfImages: Queue<Bitmap> = LinkedList();

    // Patameters
    private val currentThreshold = 0.3
    private val desiredFps = 1000
    private var sizeOfImage : Long = 320

    private var detectionEveryXFrame: Int = 5
    private var checkFPSEveryXFrame: Int = 5

    private var factorOfProbabilityInOpticalFlow: Float = 0.9F


    //TODO: Probably need to be reworked
//    val processingTimer = object : CountDownTimer(Long.MAX_VALUE, (1000 / desiredFps).toLong()) {
//        override fun onTick(millisUntilFinished: Long) {
////            Log.println(Log.INFO,"INFO", "In realAnalyze")
////            realAnalyze()
////            Log.println(Log.INFO, "Frame" ,frameCount.toString())
//            val currentFrame = frameCount - previousFrameCount;
//
//            if(currentFrame == checkFPSEveryXFrame){
//                endTime = SystemClock.uptimeMillis()
//                currentFPS = (checkFPSEveryXFrame*1000).toDouble()/(endTime - startTime).toDouble()
//                Log.println(Log.INFO, "FPS" ,currentFPS.toString())
//                previousFrameCount = frameCount
//                startTime = endTime
//            }
//            if(canBeClose){
//                imageProxy?.close()
//                canBeClose=false
//            }
//        }
//        override fun onFinish() {}
//    }.apply { start() }

    @OptIn(DelicateCoroutinesApi::class)
    override fun analyze(image: ImageProxy) {
        frameCount++
        val bitmap = imagePreparation(image);
//        canBeClose = true
        imageProxy?.close()

        if(frameCount == checkFPSEveryXFrame)
        {
            GlobalScope.launch(Dispatchers.IO) {
                launch {
                    endTime = SystemClock.uptimeMillis()
                    currentFPS = (checkFPSEveryXFrame*1000).toDouble()/(endTime - startTime).toDouble()
                    startTime = endTime
                    frameCount = 0
                }
            }
        }

        val iterationImage = originImage

        if(bitmap == null)
            return
        if(originImage == null)
            return

        GlobalScope.launch(Dispatchers.IO){
            if(detectionJob?.isCompleted == true || lastResult == null)
            {
                detectionJob = launch { realAnalyze(bitmap) }
                queueOfImages.add(iterationImage)
                if(lastResult != null && opticalFLowJob?.isActive == false)
                {

//                    opticalFLowJob = launch {
                    var prevMat = previousMatImage //TODO: Potential to run queue for optical flow, all the time on diffrent job
                        while (!queueOfImages.isEmpty()) {
                            val imageFromQueue = queueOfImages.remove()
                            val matImage = calcMatFromBitmap(imageFromQueue);
                            val result = opticalFlow(
                                bitmap,
                                prevMat,
                                matImage,
                                lastResult,
                                currentFPS,
                                iterationImage!!
                            )
                            if (result != null) {
                                callBack(result)
                            }
                            lastResult = result
                            prevMat = matImage;
//                        }
                    }
//                    queueOfImages.clear()
                }
            }
//            else if(detectionJob?.isCompleted == true){
//                //Optical Flow
//
//            }
//            else if(iterationImage != null)
//            {
//                val matImage = calcMatFromBitmap(iterationImage)
//                val result = opticalFlow(
//                    bitmap,
//                    previousMatImage,
//                    matImage,
//                    lastResult,
//                    currentFPS,
//                    originImage!!
//                )
//                if (result != null) {
//                    callBack(result)
//                }
//                lastResult = result
//                previousMatImage = matImage
//                queueOfImages.add(iterationImage);
//            }
        }

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
        lastResult = result
        callBack(result)
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