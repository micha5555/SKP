package pw.ee.proj_zesp.skp.track

import android.graphics.Bitmap
import org.opencv.core.CvType.CV_32F
import org.opencv.core.CvType.CV_32FC1
import org.opencv.core.Mat
import org.opencv.core.MatOfByte
import org.opencv.core.MatOfFloat
import org.opencv.core.MatOfPoint
import org.opencv.core.MatOfPoint2f
import org.opencv.core.Point
import org.opencv.imgproc.Imgproc
import org.opencv.video.Video
import pw.ee.proj_zesp.skp.detection.calcMatFromBitmap

class TrackBox(cropped: Bitmap, xCropped: Int, yCropped: Int) {
    var Points = mutableListOf<TrackPoint>()
    var OriginalNumberOfPoints: Int
    var left: Double
    var right: Double
    var top: Double
    var bot: Double

    init {
        left = xCropped.toDouble()
        right = xCropped.toDouble() + cropped.width
        top = yCropped.toDouble()
        bot = yCropped.toDouble() + cropped.height
        generatePoints(cropped, xCropped, yCropped)
        OriginalNumberOfPoints = Points.size
    }

    public fun generatePoints(cropped: Bitmap, xCropped: Int, yCropped: Int)
    {
        val matCropped = calcMatFromBitmap(cropped)
        val points = MatOfPoint()

        var matEditted = Mat()
        Imgproc.cvtColor(matCropped, matEditted, Imgproc.COLOR_RGB2GRAY)
        matEditted.convertTo(matEditted, CV_32FC1)
        Imgproc.goodFeaturesToTrack(matEditted, points, 20, 0.1, 10.0)

        val pointsArray = points.toList()
        for (point in pointsArray)
        {
            var trackPoint = TrackPoint(point.x+xCropped, point.y+yCropped, point.x, cropped.width - point.x, point.y, cropped.height - point.y)
            Points.add(trackPoint)
        }
    }

    public fun update(prevMat: Mat, currMat: Mat) : Double
    {
        val prevPointsList = mutableListOf<Point>()

        for(point in Points)
        {
            prevPointsList.add(Point(point.x, point.y))
        }

        val prevPoints = MatOfPoint2f()
        prevPoints.fromList(prevPointsList)

        val currPoints = MatOfPoint2f()

        val status = MatOfByte()
        val error = MatOfFloat()

        Video.calcOpticalFlowPyrLK(prevMat, currMat, prevPoints, currPoints, status, error)

        var statusArray = status.toArray()
        var currPointsArray = currPoints.toArray()

        var lost = 0
        var i = 0
        while(i < Points.size)
        {
            var point = Points[i]
            var isFound = statusArray[i].toInt() == 1
            if(isFound)
            {
                point.x = currPointsArray[i].x
                point.y = currPointsArray[i].y
            }
            else
            {
                Points.remove(point)
                i--
            }
            i++
        }

        return Points.size.toDouble()/OriginalNumberOfPoints.toDouble()
    }

    public fun generateBoundingBox(){
        var leftSum = 0.0
        var rightSum = 0.0
        var topSum = 0.0
        var botSum = 0.0
        for (point in Points)
        {
            leftSum += point.x - point.toLeft
            rightSum += point.x + point.toRight
            topSum += point.y - point.toTop
            botSum += point.y + point.toBot
        }

        left = leftSum/Points.size
        right = rightSum/Points.size
        top = topSum/Points.size
        bot = botSum/Points.size
    }
}