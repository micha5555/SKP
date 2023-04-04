package ai.onnxruntime.example.imageclassifier

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.util.AttributeSet
import android.view.View

class CustomView constructor(context: Context?, attributeSet: AttributeSet?) : View(context, attributeSet) {

    private val boxes: MutableList<RectF> = mutableListOf()
//    private val bitmap: Bitmap = Bitmap.createBitmap()

    val paint = Paint().apply {
        color = Color.RED  // Set the box color to red
        style = Paint.Style.STROKE  // Set the paint style to stroke
        strokeWidth = 5f  // Set the stroke width to 4 pixels
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        boxes.forEach{canvas.drawRect(it, paint)}

    }

    fun drawBoxes(boxes: List<RectF>, canvas: Canvas) {
        this.boxes.clear()
        this.boxes.addAll(boxes)
        this.draw(canvas)
    }

    fun drawImage(bitmap: Bitmap) {

    }


}