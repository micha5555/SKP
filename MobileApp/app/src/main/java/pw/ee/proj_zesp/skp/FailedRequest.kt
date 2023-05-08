package pw.ee.proj_zesp.skp

class FailedRequest(currentLocation: String?, probability: String?, registerPlate: String?, currentDate: String?) {

    val currentLocation: String? = currentLocation
        get() {
            return field
        }

    val probability: String? = probability
        get() {
            return field
        }

    val registerPlate: String? = registerPlate
        get() {
            return field
        }

    val currentDate: String? = registerPlate
        get() {
            return field
        }

    init {
        FailedRequest.failedRequests.add(this)
    }

    companion object {
        private var failedRequests: ArrayList<FailedRequest> = ArrayList()

        fun resendFailedRequests() {
            for (request in failedRequests) {
                val skpRequest: SKPRequest  = SKPRequest(request.currentLocation, request.probability, request.registerPlate, request.currentDate)
                try {
                    skpRequest.send()
                    failedRequests.remove(request)
                } catch (e: Exception){
//
                }
            }
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