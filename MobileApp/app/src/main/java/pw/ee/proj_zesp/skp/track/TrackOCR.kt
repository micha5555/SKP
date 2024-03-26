package pw.ee.proj_zesp.skp.track

import android.graphics.Bitmap
import android.util.Log
import com.google.mlkit.vision.common.InputImage
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import pw.ee.proj_zesp.skp.SKPRequest
import pw.ee.proj_zesp.skp.detection.YoloBox
import pw.ee.proj_zesp.skp.ocr.OCR_util
import pw.ee.proj_zesp.skp.ocr.OCR_util.Companion.recognizer
import pw.ee.proj_zesp.skp.ocr.StatisticsOCR
import pw.ee.proj_zesp.skp.utils.CommonUtils
import pw.ee.proj_zesp.skp.utils.NavigationUtils
import java.util.LinkedList
import java.util.Queue

class TrackOCR {
    var ToBeOCRed : Queue<Pair<Bitmap, YoloBox>> = LinkedList()
//    var ReadyPlates : Queue<Pair<String, Double>> = LinkedList()
    val MapPlates : MutableMap<String, StatisticsOCR> = mutableMapOf()

    public fun ProceedOCR()
    {
        if(ToBeOCRed.isEmpty())
            return
        val pairToOCR = ToBeOCRed.poll()
        val preparedImage = OCR_util.prepareImageToOCR(pairToOCR.first, pairToOCR.second)

        val imageToMlKit = InputImage.fromBitmap(preparedImage,0)
        val resultMlKit = recognizer.process(imageToMlKit).addOnSuccessListener { visionText ->
            if(visionText.textBlocks.size > 0 && visionText.textBlocks[0].lines.size > 0)
            {
                var parsed = OCR_util.parseOCRResults(visionText)
                if(parsed != null)
                {
                    var plateInMap = MapPlates.get(parsed.first)
                    if(plateInMap != null)
                    {
                        plateInMap.sum += parsed.second
                        plateInMap.Occured += 1
                        MapPlates.replace(parsed.first, plateInMap)
                    }
                    else{
                        var statistic = StatisticsOCR()
                        statistic.sum = parsed.second
                        statistic.Occured = 1
                        MapPlates.put(parsed.first, statistic)
                    }
                }
            }

        }

    }

    public fun getVotedPlate() : Pair<String, StatisticsOCR>{
        val votes = MapPlates.toList()
        var biggestPlate = ""
        var value = StatisticsOCR()

        for (vote in votes)
        {
            if (vote.second.sum > value.sum)
            {
                value = vote.second
                biggestPlate = vote.first
            }
        }

        return Pair(biggestPlate, value)
    }

}