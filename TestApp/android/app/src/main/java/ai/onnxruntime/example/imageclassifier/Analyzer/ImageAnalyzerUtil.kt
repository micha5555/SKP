package ai.onnxruntime.example.imageclassifier.Analyzer

import ai.onnxruntime.example.imageclassifier.YoloBox
import android.graphics.Bitmap
import android.graphics.Matrix

fun Bitmap.rotate(degrees: Float): Bitmap {
    val matrix = Matrix().apply { postRotate(degrees) }
    return Bitmap.createBitmap(this, 0, 0, width, height, matrix, true)
}

fun cropBoundingBox(orignalImage: Bitmap, boundingBox: YoloBox) : Bitmap {
    val x = (boundingBox.x * orignalImage.width).toInt();
    val y = (boundingBox.y * orignalImage.height).toInt();
    var width = (boundingBox.width * orignalImage.width).toInt();
    var height = (boundingBox.height * orignalImage.height).toInt();

    if (x + width > orignalImage.width)
        width = orignalImage.width - x;
    if (y + height > orignalImage.height)
        height = orignalImage.height - y;

    val newBitmap = Bitmap.createBitmap(orignalImage, x, y, width,height);
    return newBitmap;
}