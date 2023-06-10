package pw.ee.proj_zesp.skp.track

import android.graphics.Bitmap
import org.opencv.core.Mat
import org.opencv.core.Rect
import pw.ee.proj_zesp.skp.detection.Result_Yolo_v8
import pw.ee.proj_zesp.skp.detection.YoloBox
import pw.ee.proj_zesp.skp.detection.calcMatFromBitmap
import pw.ee.proj_zesp.skp.utils.cropBoundingBox
import pw.ee.proj_zesp.skp.utils.isOverlaping
import java.lang.Exception

class CustomMultiTracker {
    var Tracks = mutableListOf<Track>()
    var ProbabilityMultiplier: Float = 0.9F
    var ProbabilityThreshold: Float = 0.4F

    var LastWorkingBitmap : Bitmap? = null
    var LastBitmap : Bitmap? = null


    public fun add(result: Result_Yolo_v8, workingBitmap: Bitmap){
        update(result.bitmap_origin, workingBitmap)

        for (box in result.boxes)
        {

            var isTracked = false

            for (track in Tracks) {
                val trackYoloBox = YoloBox(track.Box.left.toFloat()/workingBitmap.width.toFloat(), track.Box.top.toFloat()/workingBitmap.width.toFloat(), (track.Box.right - track.Box.left).toFloat()/workingBitmap.width.toFloat(), (track.Box.bot - track.Box.top).toFloat()/workingBitmap.width.toFloat(), track.Probability)

                if (isOverlaping(box, trackYoloBox)) {
                    isTracked = true
                    if(box.probability > trackYoloBox.probability)
                    {
                        var cropped = cropBoundingBox(result.bitmap_origin, box)
                        val trackBox = TrackBox(cropped, (box.x*result.bitmap_origin.width).toInt(), (box.y*result.bitmap_origin.height).toInt())
                        Tracks.add(Track(box.probability, trackBox))
                        Tracks.remove(track)
                    }
                    break
                }
            }

            if (!isTracked) {
                var cropped = cropBoundingBox(result.bitmap_origin, box)
                val trackBox = TrackBox(cropped, (box.x*result.bitmap_origin.width).toInt(), (box.y*result.bitmap_origin.height).toInt())
                Tracks.add(Track(box.probability, trackBox))
            }

        }
    }

    private fun update(imageMat: Mat)
    {
        if(LastWorkingBitmap == null)
            return
        var prevMat = calcMatFromBitmap(LastWorkingBitmap!!)
        var i = 0
        while (i < Tracks.size)
        {
            var track = Tracks[i]
            var success = track.Box.update(prevMat, imageMat) > 0.8
            if(success)
            {
                track.Probability *= ProbabilityMultiplier;
                if(track.Probability < ProbabilityThreshold)
                {
                    Tracks.remove(track)
                    i--
                }
                else
                {
                    track.Box.generateBoundingBox()
                }
            }
            else
            {
                Tracks.remove(track)
                i--
            }
            i++
        }
    }

    public fun update(bitmap: Bitmap, workingBitmap: Bitmap)
    {
        update(calcMatFromBitmap(workingBitmap))
        LastWorkingBitmap = workingBitmap
        LastBitmap = bitmap
    }

    public fun generateResult() : Result_Yolo_v8{
        var bitmap: Bitmap = LastBitmap ?: throw Exception()
        var result = Result_Yolo_v8(Tracks.size, generateYoloBoxList(), 0.0, bitmap)
        return result
    }

    public fun generateYoloBoxList() : List<YoloBox>{
        var result = mutableListOf<YoloBox>()
        var bitmap: Bitmap = LastBitmap ?: throw Exception()
        var workingBitmap: Bitmap = LastWorkingBitmap ?: throw Exception()

        for(track in Tracks)
        {
            var box = YoloBox(track.Box.left.toFloat()/workingBitmap.width.toFloat(), track.Box.top.toFloat()/workingBitmap.width.toFloat(), (track.Box.right - track.Box.left).toFloat()/workingBitmap.width.toFloat(), (track.Box.bot - track.Box.top).toFloat()/workingBitmap.width.toFloat(), track.Probability)
            result.add(box)
        }

        return result
    }
}