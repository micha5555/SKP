package pw.ee.proj_zesp.skp.track

import android.graphics.Bitmap
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Dispatchers.Main
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import pw.ee.proj_zesp.skp.SKPRequest
import pw.ee.proj_zesp.skp.detection.YoloBox
import pw.ee.proj_zesp.skp.ocr.OCR_util
import pw.ee.proj_zesp.skp.utils.CommonUtils
import pw.ee.proj_zesp.skp.utils.Navigation
import pw.ee.proj_zesp.skp.utils.cropBoundingBox

class Track(
    public var Probability: Float,
    public var Box: TrackBox,
    public var OriginalImage: Bitmap
//    public var
) {
    public var OCR: TrackOCR = TrackOCR()

    companion object{
        public fun createTrack(bitmap: Bitmap, box: YoloBox) : Track{
            var cropped = cropBoundingBox(bitmap, box)
            val trackBox = TrackBox(cropped, (box.x*bitmap.width).toInt(), (box.y*bitmap.height).toInt())
            return Track(box.probability, trackBox, bitmap)
        }
    }

    public fun lost(){
        while(!OCR.ToBeOCRed.isEmpty())
        {
            OCR.ProceedOCR()
        }
        var bestPlate = OCR.getVotedPlate()
        var avg = bestPlate.second.getAverage()
        var isProblematic = if( avg > 0.6) {
            false
        } else if(avg > 0.4){
            true
        }
        else{
            return
        }

        var nav : String? = null

        CoroutineScope(Dispatchers.IO).launch {
            withContext(Main){
                nav = Navigation.navigation.getLocation()
            }
                Log.println(Log.INFO, "CAR_PLATE", "OCRed Text sending to API")
                val image: ByteArray = CommonUtils.convertBitmapToByteArray(OriginalImage)
                val srequest = SKPRequest(isProblematic, image, nav!!,
                    CommonUtils.parseProbabilityToRequestFormat(avg),
                    bestPlate.first, "")
                srequest.start()

        }
    }
    public fun update(image: Bitmap){
        Box.generateBoundingBox()
        if(OCR_util.checkBoxProportions(Box.getWidth(), Box.getHeight()))
        {
            OCR.ToBeOCRed.add(Pair(image, generateYoloBox(image.width, image.height)))
            CoroutineScope(Dispatchers.Default).launch {
                OCR.ProceedOCR()
            }
        }
    }

    public fun replaceBox(bitmap: Bitmap, box: YoloBox){
        var cropped = cropBoundingBox(bitmap, box)
        val trackBox = TrackBox(cropped, (box.x*bitmap.width).toInt(), (box.y*bitmap.height).toInt())
        Box = trackBox
        Probability = box.probability
    }

    public fun generateYoloBox(imageWidth: Int, imageHeight: Int) : YoloBox{
        return YoloBox(
            Box.left.toFloat()/imageWidth.toFloat(),
            Box.top.toFloat()/imageHeight.toFloat(),
            (Box.right - Box.left).toFloat()/imageWidth.toFloat(),
            (Box.bot - Box.top).toFloat()/imageHeight.toFloat(),
            Probability)
    }
}