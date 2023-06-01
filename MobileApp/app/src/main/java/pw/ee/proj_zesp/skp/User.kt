package pw.ee.proj_zesp.skp

class User(login: String, accessToken: String, refreshToken: String) {

    companion object {
        var loggedUser: User? = null
    }

    var login: String = login
        get() {
            return field
        }

    var accessToken: String = accessToken
        get() {
            return field
        }

    var refreshToken: String = refreshToken
        get() {
            return field
        }
}