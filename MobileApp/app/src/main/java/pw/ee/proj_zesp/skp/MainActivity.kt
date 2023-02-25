package pw.ee.proj_zesp.skp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import pw.ee.proj_zesp.skp.kontrolastart.KontrolaStart
import pw.ee.proj_zesp.skp.kontrolastop.KontrolaStop
import pw.ee.proj_zesp.skp.menu.Menu
import pw.ee.proj_zesp.skp.osystemie.OSystemie
import pw.ee.proj_zesp.skp.ui.theme.SKPTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SKPTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colors.background
                ) {
//                    Menu()
                    KontrolaStart()
//                    KontrolaStop()
//                    OSystemie();
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String) {
    Text(text = "Hello $name!")
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    SKPTheme {
        Greeting("Android")
    }
}