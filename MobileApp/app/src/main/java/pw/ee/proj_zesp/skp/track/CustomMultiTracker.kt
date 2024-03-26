package pw.ee.proj_zesp.skp.track

import android.graphics.Bitmap
import pw.ee.proj_zesp.skp.detection.Result_Yolo_v8
import pw.ee.proj_zesp.skp.detection.YoloBox
import pw.ee.proj_zesp.skp.detection.calcMatFromBitmap
import pw.ee.proj_zesp.skp.ocr.OCR_util.Companion.checkBoxProportions
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
                val trackYoloBox = track.generateYoloBox(result.bitmap_origin.width, result.bitmap_origin.height)

                if (isOverlaping(box, trackYoloBox)) {
                    isTracked = true
                    if(box.probability > trackYoloBox.probability ) {
                        track.replaceBox(result.bitmap_origin, box)
                    }
                    break
                }
            }

            if (!isTracked && checkBoxProportions(box.width.toDouble(), box.height.toDouble())) {
                Tracks.add(Track.createTrack(result.bitmap_origin, box))
            }

        }
    }

    private fun update(workingBitmap: Bitmap)
    {
        val imageMat = calcMatFromBitmap(workingBitmap)
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
                    track.lost()
                    Tracks.remove(track)
                    i--
                }
                else
                {
                    track.update(workingBitmap)
                }
            }
            else
            {
                track.lost()
                Tracks.remove(track)
                i--
            }
            i++
        }
    }

    public fun update(bitmap: Bitmap, workingBitmap: Bitmap)
    {
        update(workingBitmap)
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
            result.add(track.generateYoloBox(workingBitmap.width, workingBitmap.height))
        }

        return result
    }
}