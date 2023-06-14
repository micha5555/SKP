package pw.ee.proj_zesp.skp.ocr

import android.graphics.Bitmap
import com.google.mlkit.vision.text.Text
import com.google.mlkit.vision.text.TextRecognition
import com.google.mlkit.vision.text.latin.TextRecognizerOptions
import org.opencv.android.Utils
import org.opencv.core.Core
import org.opencv.core.CvType
import org.opencv.core.Mat
import org.opencv.core.Scalar
import org.opencv.imgproc.Imgproc
import pw.ee.proj_zesp.skp.detection.YoloBox
import pw.ee.proj_zesp.skp.utils.cropBoundingBox

class OCR_util {
    companion object{
        public val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)

        fun prepareImageToOCR(image: Bitmap, box: YoloBox): Bitmap
        {
            val cropped = cropBoundingBox(image, box);
            var matSource = Mat()
            Utils.bitmapToMat(cropped, matSource)

            Imgproc.cvtColor(matSource,matSource, Imgproc.COLOR_RGB2GRAY)
            var matDest = Mat()

            matSource.convertTo(matDest, CvType.CV_32F, 1.0 / 255.0)

            // Zastosowanie zmiany gamma
            val gamma = 3.0 // Wartość gamma
            Core.pow(matDest, gamma, matDest)

            // Konwersja z powrotem na zakres 0-255
            Core.multiply(matDest, Scalar(255.0), matDest)
            matDest.convertTo(matDest, CvType.CV_8U)

            val bmp: Bitmap = Bitmap.createBitmap(cropped.width,cropped.height,Bitmap.Config.ARGB_8888)
            Utils.matToBitmap(matDest, bmp);

            matSource.release()
            matDest.release()

            return bmp
        }
        fun parseOCRResults(resultText : Text) : Pair<String, Double>?
        {
            var registerPlate: String = ""
            var cumulatedConfidence: Double = 0.0
            var characterCount: Int = 0
            val regex = Regex("[^A-Za-z0-9]")
            val regexForSymbols = Regex("[A-Za-z0-9]+")
            for(block in resultText.textBlocks)
            {
                for(line in block.lines)
                {
                    val parsedLine = line.text.replace(regex, "")
                    if(parsedLine.length < 4 || parsedLine.length > 7)
                    {
                        continue
                    }
                    else
                    {
                        val elements = line.elements
                        for(element in elements)
                        {
                            for(symbol in element.symbols)
                            {
                                val symbolText = symbol.text
                                val matches = symbolText.matches(regexForSymbols)
                                if(matches)
                                {
                                    cumulatedConfidence += symbol.confidence
                                    characterCount++
                                    registerPlate += symbol.text
                                }
                            }
                        }
                        cumulatedConfidence /= characterCount
                        return Pair(registerPlate, cumulatedConfidence)
                    }
                }
            }
            return null
        }

        // register plate in Poland has proportion 4.561 : 1
        fun checkBoxProportions(left: Double, right: Double, top: Double, bottom: Double) : Boolean
        {
            val width = Math.abs(right - left)
            val height = Math.abs(bottom - top)
            val proportions = width / height
//    Log.println(Log.INFO, "CAR PLATE", "OCRed Text: proprtion plate " + proportions)
            return proportions in 2.1..5.0
        }

        fun checkBoxProportions(width: Double, height: Double) : Boolean
        {
            if(height == 0.0)
            {
                return false
            }
            val proportions: Double = Math.abs(width / height)
            return proportions in 2.1..5.0
        }
    }
}