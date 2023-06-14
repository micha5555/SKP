package pw.ee.proj_zesp.skp.ocr

class StatisticsOCR {
    public var sum : Double = 0.0
//    public var Average : Double = 0.0
    public var Occured : Int = 0

    public fun getAverage() : Double{
        return sum/Occured
    }
}