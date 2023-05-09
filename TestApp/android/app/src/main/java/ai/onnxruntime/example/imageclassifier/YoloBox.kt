package ai.onnxruntime.example.imageclassifier

import android.graphics.Point

class YoloBox {
    var x: Float = 0.0F
    var y: Float = 0.0F
    var width: Float = 0.0F
    var height: Float = 0.0F
    var probability: Float = 0.0F

    constructor(x: Float, y: Float, width: Float, height: Float, probability: Float){
        this.x = x
        this.y = y
        this.width = width
        this.height = height
        this.probability = probability
    }

    // Getters
    fun getX1(): Float{  return x  }
    fun getX2(): Float{  return x + width  }
    fun getY1(): Float{  return y  }
    fun getY2(): Float{  return y + height  }
    fun getXCenter(): Float {return x + width/2}
    fun getYCenter(): Float{return y + height/2}
    fun getCenterPoint(targetResoultion: Int) : Point {
        return Point(
            ((x + width/2)*targetResoultion).toInt(),
            ((y + height/2)*targetResoultion).toInt())
    }
//    fun getWidth(): Double{  return width   }
//    fun getHeight(): Double{  return height  }
//    fun getProbability(): Double{  return probability  }

    // Setters - TODO


}