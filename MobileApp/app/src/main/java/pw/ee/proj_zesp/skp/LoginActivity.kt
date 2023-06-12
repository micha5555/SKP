package pw.ee.proj_zesp.skp

import android.content.Intent
import android.graphics.drawable.Drawable
import android.os.Bundle
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.content.ContextCompat
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import pw.ee.proj_zesp.skp.utils.CommonUtils

class LoginActivity : AppCompatActivity() {
    lateinit var loginTextField: EditText
    lateinit var passwordTextField: EditText
    override fun onCreate(savedInstanceState: Bundle?) {
        getSupportActionBar()?.hide()
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
        super.onCreate(savedInstanceState)
        setContentView(R.layout.login_layout)

        val loginButton: ImageButton = findViewById<ImageButton>(R.id.login_button)
        val button: Drawable = ContextCompat.getDrawable(this, R.drawable.button_shape)!!
        loginButton.setBackgroundDrawable(button)
        loginButton.setOnClickListener {
            loginTextField = findViewById(R.id.login_text_field)
            passwordTextField = findViewById(R.id.password_text_field)
            val login: String = loginTextField.text.toString()
            val password: String = passwordTextField.text.toString()
            SKPLoginRequest.loginRequest(login, password)

            Thread.sleep(2000)
//            When you need token for api requests
            println("user token")
            println(User.loggedUser?.accessToken)
            if(User.loggedUser != null && User.loggedUser?.accessToken != null) {
                val intent = Intent(this, MainActivity::class.java)
                this.startActivity(intent)
            }
        }
    }
}