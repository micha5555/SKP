package pw.ee.proj_zesp.skp.detection

import android.graphics.Bitmap
import org.opencv.android.Utils
import org.opencv.core.Mat
import org.opencv.core.MatOfByte
import org.opencv.core.MatOfFloat
import org.opencv.core.MatOfPoint2f
import org.opencv.core.Point
import org.opencv.video.Video

public fun opticalFlow(bitmap: Bitmap, previousMatImage: Mat?, currentMatImage: Mat?, lastResult: Result_Yolo_v8?, currentFPS: Double, originImage: Bitmap) : Result_Yolo_v8? {
    if (previousMatImage == null || currentMatImage == null)
        return null
    if(lastResult == null)
        return null
    if(lastResult.boxes.isEmpty())
    {
        return Result_Yolo_v8(0, emptyList(),currentFPS,originImage)
    }


    val resultPoints = MatOfPoint2f()
    val status = MatOfByte()
    val err = MatOfFloat()
    Video.calcOpticalFlowPyrLK(
        previousMatImage, currentMatImage,
        calcMatPointsFromResults(lastResult),
        resultPoints, status, err)

    return calcResultsFromMatPoints(resultPoints, status, lastResult, currentFPS, originImage)

}

fun calcMatFromBitmap(bitmap: Bitmap) : Mat
{
    val mat = Mat()
    val bmp32: Bitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true)
    Utils.bitmapToMat(bmp32, mat)
    return mat
}

private fun calcResultsFromMatPoints(
    points: MatOfPoint2f,
    status: MatOfByte,
    prevResult: Result_Yolo_v8,
    currentFPS: Double,
    originImage: Bitmap
): Result_Yolo_v8 {
    val newBoxes: MutableList<YoloBox> = mutableListOf()
    val statusArray = status.toArray()
    val pointsArray = points.toArray()
    for (i in 0 until prevResult.boxes.size) {
        var p1Index = i * 4
        var p2Index = i * 4 + 1
        var p3Index = i * 4 + 2
        var p4Index = i * 4 + 3

        //Status Mat - 1: Found, 0: Lost
        var isP1Found = statusArray[p1Index].toInt() == 1
        var isP2Found = statusArray[p2Index].toInt() == 1
        var isP3Found = statusArray[p3Index].toInt() == 1
        var isP4Found = statusArray[p4Index].toInt() == 1

        if (!isP1Found && !isP2Found && !isP3Found && !isP4Found)
            continue;

        val oldBoxProbability = prevResult.boxes[i].probability

        val left = getLeftPosition(
            statusArray,
            pointsArray,
            p1Index,
            p2Index,
            p3Index,
            p4Index,
            prevResult,
            i
        )
        val right = getRightPosition(
            statusArray,
            pointsArray,
            p1Index,
            p2Index,
            p3Index,
            p4Index,
            prevResult,
            i
        )
        val up = getTopPosition(
            statusArray,
            pointsArray,
            p1Index,
            p2Index,
            p3Index,
            p4Index,
            prevResult,
            i
        )
        val down = getBottomPosition(
            statusArray,
            pointsArray,
            p1Index,
            p2Index,
            p3Index,
            p4Index,
            prevResult,
            i
        )

        val newWidth = right - left
        val newHeight = down - up

        val newBox = YoloBox(
            left.toFloat(), up.toFloat(),
            newWidth.toFloat(), newHeight.toFloat(),
            oldBoxProbability
        )

        newBoxes.add(newBox)
    }

    return Result_Yolo_v8(newBoxes.size, newBoxes, currentFPS, originImage)
}

private fun getLeftPosition(statusArray: ByteArray, pointsArray: Array<Point>, p1Index: Int, p2Index: Int, p3Index: Int, p4Index: Int, prevResult: Result_Yolo_v8, currentBox: Int) : Double
{
    var isP1Found = statusArray[p1Index].toInt() == 1
    var isP2Found = statusArray[p2Index].toInt() == 1
    var isP3Found = statusArray[p3Index].toInt() == 1
    var isP4Found = statusArray[p4Index].toInt() == 1

    val p1 = Point( //LU
        (pointsArray[p1Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p1Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p2 = Point( //RD
        (pointsArray[p2Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p2Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p3 = Point( //LD
        (pointsArray[p3Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p3Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p4 = Point( //RU
        (pointsArray[p4Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p4Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())

    if(isP1Found && isP3Found)
        return (p1.x + p3.x)/2
    if(isP1Found)
        return p1.x
    if(isP3Found)
        return p3.x

    if(isP2Found && isP4Found)
    {
        val tmpLeft = (p2.x + p4.x)/2 - prevResult.boxes[currentBox].width
        if(tmpLeft > 0)
            return tmpLeft
        else
            return 0.0
    }
    if(isP2Found)
    {
        val tmpLeft = p2.x - prevResult.boxes[currentBox].width;
        if(tmpLeft > 0)
            return tmpLeft
        else
            return 0.0
    }
//        if(isP4Found)
    val tmpLeft =  p4.x - prevResult.boxes[currentBox].width;
    if(tmpLeft > 0)
        return tmpLeft
    else
        return 0.0
}

private fun getRightPosition(statusArray: ByteArray, pointsArray: Array<Point>, p1Index: Int, p2Index: Int, p3Index: Int, p4Index: Int, prevResult: Result_Yolo_v8, currentBox: Int) : Double
{
    var isP1Found = statusArray[p1Index].toInt() == 1
    var isP2Found = statusArray[p2Index].toInt() == 1
    var isP3Found = statusArray[p3Index].toInt() == 1
    var isP4Found = statusArray[p4Index].toInt() == 1

    val p1 = Point( //LU
        (pointsArray[p1Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p1Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p2 = Point( //RD
        (pointsArray[p2Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p2Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p3 = Point( //LD
        (pointsArray[p3Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p3Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p4 = Point( //RU
        (pointsArray[p4Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p4Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())

    if(isP2Found && isP4Found)
        return (p2.x + p4.x)/2
    if(isP2Found)
        return p2.x
    if(isP4Found)
        return p4.x

    if(isP1Found && isP3Found)
    {
        var tmpRight = (p1.x + p3.x)/2 + prevResult.boxes[currentBox].width
        if(tmpRight < prevResult.bitmap_origin.width)
            return tmpRight
        else
            return prevResult.bitmap_origin.width.toDouble()
    }
    if(isP1Found)
    {
        var tmpRight = p1.x + prevResult.boxes[currentBox].width
        if(tmpRight < prevResult.bitmap_origin.width)
            return tmpRight
        else
            return prevResult.bitmap_origin.width.toDouble()
    }
//        if(isP4Found)
    var tmpRight = p3.x + prevResult.boxes[currentBox].width
    if(tmpRight < prevResult.bitmap_origin.width)
        return tmpRight
    else
        return prevResult.bitmap_origin.width.toDouble()
}

private fun getTopPosition(statusArray: ByteArray, pointsArray: Array<Point>, p1Index: Int, p2Index: Int, p3Index: Int, p4Index: Int, prevResult: Result_Yolo_v8, currentBox: Int) : Double
{
    var isP1Found = statusArray[p1Index].toInt() == 1
    var isP2Found = statusArray[p2Index].toInt() == 1
    var isP3Found = statusArray[p3Index].toInt() == 1
    var isP4Found = statusArray[p4Index].toInt() == 1

    val p1 = Point( //LU
        (pointsArray[p1Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p1Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p2 = Point( //RD
        (pointsArray[p2Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p2Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p3 = Point( //LD
        (pointsArray[p3Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p3Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p4 = Point( //RU
        (pointsArray[p4Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p4Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())

    if(isP1Found && isP4Found)
        return (p1.y + p4.y)/2
    if(isP1Found)
        return p1.y
    if(isP4Found)
        return p4.y

    if(isP2Found && isP3Found)
    {
        var tmpTop = (p2.y + p3.y)/2 - prevResult.boxes[currentBox].height
        if (tmpTop >  0)
            return tmpTop
        else
            return 0.0
    }
    if(isP2Found)
    {
        val tmpTop = p2.y - prevResult.boxes[currentBox].height
        if (tmpTop >  0)
            return tmpTop
        else
            return 0.0
    }
//        if(isP4Found)
    val tmpTop = p3.y - prevResult.boxes[currentBox].height
    if (tmpTop >  0)
        return tmpTop
    else
        return 0.0
}

private fun getBottomPosition(statusArray: ByteArray, pointsArray: Array<Point>, p1Index: Int, p2Index: Int, p3Index: Int, p4Index: Int, prevResult: Result_Yolo_v8, currentBox: Int) : Double
{
    val isP1Found = statusArray[p1Index].toInt() == 1
    val isP2Found = statusArray[p2Index].toInt() == 1
    val isP3Found = statusArray[p3Index].toInt() == 1
    val isP4Found = statusArray[p4Index].toInt() == 1

    val p1 = Point( //LU
        (pointsArray[p1Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p1Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p2 = Point( //RD
        (pointsArray[p2Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p2Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p3 = Point( //LD
        (pointsArray[p3Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p3Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())
    val p4 = Point( //RU
        (pointsArray[p4Index].x.toFloat()/prevResult.bitmap_origin.width).toDouble(),
        (pointsArray[p4Index].y.toFloat()/prevResult.bitmap_origin.height).toDouble())

    if(isP2Found && isP3Found)
        return (p2.y + p3.y)/2
    if(isP2Found)
        return p2.y
    if(isP3Found)
        return p3.y

    if(isP1Found && isP4Found)
    {
        val tmpBot = (p1.y + p4.y)/2 + prevResult.boxes[currentBox].height;
        if(tmpBot < prevResult.bitmap_origin.width)
            return tmpBot
        else
            return prevResult.bitmap_origin.width.toDouble()
    }
    if(isP1Found)
    {
        val tmpBot = p1.y + prevResult.boxes[currentBox].height;
        if(tmpBot < prevResult.bitmap_origin.width)
            return tmpBot
        else
            return prevResult.bitmap_origin.width.toDouble()
    }

    val tmpBot = p4.y + prevResult.boxes[currentBox].height;
    if(tmpBot < prevResult.bitmap_origin.width)
        return tmpBot
    else
        return prevResult.bitmap_origin.width.toDouble()

}

private fun calcMatPointsFromResults(result: Result_Yolo_v8) : MatOfPoint2f
{
    //Currently we are taking only 2 points - maybe 4 are better?
    //Left upper corner and right lower corner of box
    val points: MutableList<Point> = mutableListOf()
    for(oldBox in result.boxes)
    {
        val left = oldBox.x.toDouble()*result.bitmap_origin.width
        val right = (oldBox.x + oldBox.width).toDouble()*result.bitmap_origin.width
        val up = oldBox.y.toDouble()*result.bitmap_origin.height
        val down = (oldBox.y + oldBox.height).toDouble()*result.bitmap_origin.height

        //LU, RD, LD, RU
        val p1 = Point(left, up)
        val p2 = Point(right, down)
        val p3 = Point(left, down)
        val p4 = Point(right, up)

        points.add(p1)
        points.add(p2)
        points.add(p3)
        points.add(p4)
    }

    val matPoints = MatOfPoint2f()
    matPoints.fromList(points)
    return  matPoints
}