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