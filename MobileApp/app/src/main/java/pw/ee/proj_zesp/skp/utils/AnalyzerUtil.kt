package pw.ee.proj_zesp.skp.utils

import android.util.Log
import com.google.mlkit.vision.text.Text
import pw.ee.proj_zesp.skp.detection.YoloBox

fun addBoxToListIfNewOrBetter(listOfBoxes: MutableList<YoloBox>, newBox: YoloBox)
{
    if(listOfBoxes.isEmpty())
        listOfBoxes.add(newBox)

    for (box in listOfBoxes){
        if(isOverlaping(newBox, box))
        {
            saveHigherProbabilityBox(newBox, box, listOfBoxes)
            break
        }
    }
}

fun isOverlaping(box1: YoloBox, box2: YoloBox) : Boolean
{
    val (boxA, boxB) = getBoxesInOrder(box1, box2)

    if(boxB.getX1() < boxA.getX2())
        return true
    if(boxB.getY1() < boxA.getY2())
        return true
    return false
}

fun saveHigherProbabilityBox(newBox: YoloBox, oldBox: YoloBox, listOfBoxes: MutableList<YoloBox>){
    if(newBox.probability > oldBox.probability)
    {
        listOfBoxes.remove(oldBox)
        listOfBoxes.add(newBox)
    }
}

fun getBoxesInOrder(box1: YoloBox, box2: YoloBox) : Pair<YoloBox, YoloBox>
{
    val boxA : YoloBox
    val boxB : YoloBox

    if(box1.x < box2.x)
    {
        boxA = box1
        boxB = box2
    }
    else if(box1.x > box2.x)
    {
        boxA = box2
        boxB = box1
    }
    else if(box1.y > box2.y)
    {
        boxA = box2
        boxB = box1
    }
    else
    {
        boxA = box1
        boxB = box2
    }
    return Pair(boxA, boxB)
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