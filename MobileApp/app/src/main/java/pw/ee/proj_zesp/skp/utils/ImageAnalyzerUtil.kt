package pw.ee.proj_zesp.skp.utils

import android.graphics.Bitmap
import android.graphics.Matrix
import android.util.Log
import pw.ee.proj_zesp.skp.detection.YoloBox

fun Bitmap.rotate(degrees: Float): Bitmap {
    val matrix = Matrix().apply { postRotate(degrees) }
    return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
}

fun cropBoundingBox(originalImage: Bitmap, boundingBox: YoloBox) : Bitmap {
    var x = (boundingBox.x * originalImage.width).toInt();
    var y = (boundingBox.y * originalImage.height).toInt();
    var width = (boundingBox.width * originalImage.width).toInt();
    var height = (boundingBox.height * originalImage.height).toInt();

    if(x >= originalImage.width || x < 0)
        x = 0
    if(y >= originalImage.height || y < 0)
        y = 0

    Log.println(Log.INFO, "CropBoundingBox", "x=$x ,y=$y ,width=$width ,height=$height")

    if (x + width > originalImage.width)
        width = originalImage.width - x;
    if (y + height > originalImage.height)
        height = originalImage.height - y;

    if(width <= 0)
        width = 1;
    if(height <= 0)
        height = 1;

    Log.println(Log.INFO, "CropBoundingBox", "x=$x ,y=$y ,width=$width ,height=$height")

    val newBitmap = Bitmap.createBitmap(originalImage, x, y, width,height);
    return newBitmap;
}