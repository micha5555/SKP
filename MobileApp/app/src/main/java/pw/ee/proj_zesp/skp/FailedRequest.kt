package pw.ee.proj_zesp.skp

import android.graphics.drawable.Drawable
import java.util.*
import kotlin.collections.ArrayList

class FailedRequest(isProblematic: Boolean, photo: ByteArray, currentLocation: String, probability: String, registerPlate: String, currentDate: String) {

    val isProblematic: Boolean = isProblematic
        get() {
            return field
        }

    val photo: ByteArray = photo
        get() {
            return field
        }

    val currentLocation: String = currentLocation
        get() {
            return field
        }

    val probability: String = probability
        get() {
            return field
        }

    val registerPlate: String = registerPlate
        get() {
            return field
        }

    val currentDate: String = registerPlate
        get() {
            return field
        }

    init {
        FailedRequest.failedRequests.add(this)
    }

    companion object {
        private var failedRequests: ArrayList<FailedRequest> = ArrayList()
        var timer : Timer = Timer()

        // for development purpose only
        fun printFailedRequests() {
            println(failedRequests)
        }

        object timerTask : TimerTask() {
            override fun run() {
                if(failedRequests.size > 0) {
                    resendFailedRequests()
                } else {
                    println("There aren`t failed requests")
                }
            }
        }

        fun resendFailedRequests() {
            for (request in failedRequests) {
                val skpRequest: SKPRequest  = SKPRequest(request.isProblematic, request.photo, request.currentLocation, request.probability, request.registerPlate, request.currentDate)
                try {
                    skpRequest.start()
                    failedRequests.remove(request)
                } catch (e: Exception){
                    e.printStackTrace()
                }
            }
        }

//        Use this method when detection is started
        fun startSendingFailedRequestsAtIntervals(intervalInMiliseconds: Long) {
            if(timer == null) {
                timer = Timer()
            }
            timer.scheduleAtFixedRate(timerTask, 0, intervalInMiliseconds)
        }

        fun stopSendingFailedRequests() {
            timerTask.cancel()
            timer.cancel()
        }

        fun addFailedRequest(failedRequest: FailedRequest) {
            failedRequests.add(failedRequest)
        }

        fun getFailedRequests() : ArrayList<FailedRequest> {
            return failedRequests
        }

        fun countFailedRequests() : Int {
            return failedRequests.size
        }

        fun clearFailedRequests() {
            failedRequests = ArrayList()
        }
    }


}