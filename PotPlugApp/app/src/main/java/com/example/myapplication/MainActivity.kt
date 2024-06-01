package com.example.myapplication

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothSocket
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.renderscript.ScriptGroup.Input
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresApi
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.app.ActivityCompat
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import java.io.ByteArrayInputStream
import java.io.IOException
import java.io.InputStream
import java.util.UUID


class MainActivity : ComponentActivity() {
    lateinit var bluetoothAdapter:BluetoothAdapter
    lateinit var bluetoothSocket: BluetoothSocket
    lateinit var anInputStream: InputStream
    private var deviceList = mutableStateListOf<String>()
    private val BT_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")


    //IMPORTANT: Find and enter the address of the Bluetooth device you want to connect here.
    private val DEVICE_ADDRESS = "D4:8A:FC:9E:50:7E"
    private val enableBluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            // Bluetooth is enabled, proceed with further actions
            Toast.makeText(this, "Bluetooth is enabled", Toast.LENGTH_SHORT).show()
            println("yay?")
        } else {
            // User chose not to enable Bluetooth
            Toast.makeText(this, "Bluetooth not enabled", Toast.LENGTH_SHORT).show()
            println("grrrr")
        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        checkPermissions()

        val bluetoothManager: BluetoothManager = getSystemService(BluetoothManager::class.java)
        bluetoothAdapter = bluetoothManager.getAdapter()


        if (bluetoothAdapter == null) {
            println("Bluetooth is not supported on this device")
            return
        }
        if (!bluetoothAdapter.isEnabled) {
            var intent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            enableBluetoothLauncher.launch(intent)
        }

        val device: BluetoothDevice = bluetoothAdapter.getRemoteDevice(DEVICE_ADDRESS)

        connectBT(device)

        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    DeviceList(

                        modifier = Modifier.padding(innerPadding),
                        theList = deviceList
                    )
                }
            }
        }


        StartBT(anInputStream)

        

        // Start device discovery
//        bluetoothAdapter.startDiscovery()

    }
    override fun onResume() {
        super.onResume()
        registerReceiver(receiver, IntentFilter(BluetoothDevice.ACTION_FOUND))
    }

    override fun onPause() {
        super.onPause()
        unregisterReceiver(receiver)
    }

    private val receiver = object : BroadcastReceiver() {

        @RequiresApi(Build.VERSION_CODES.TIRAMISU)
        override fun onReceive(context: Context, intent: Intent) {
            val action: String? = intent.getAction()
            when(action) {
                BluetoothDevice.ACTION_FOUND -> {
                    // Discovery has found a device. Get the BluetoothDevice
                    // object and its info from the Intent.
                    val device: BluetoothDevice? =
                        intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE, BluetoothDevice::class.java)
                    if (ActivityCompat.checkSelfPermission(
                            context,
                            Manifest.permission.BLUETOOTH_CONNECT
                        ) != PackageManager.PERMISSION_GRANTED
                    ) {
                        val REQ_PERMISSION_CODE = 113
                        ActivityCompat.requestPermissions(this@MainActivity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT),REQ_PERMISSION_CODE)
                        return
                    }
                    val deviceName = device!!.name
                    val deviceHardwareAddress = device.getAddress() // MAC address
                    deviceList.add(deviceName)
                    println(deviceList)
                    //Verify device information, then use connectBT if the device is the one you wish to connect
                }
            }
        }
    }

    fun connectBT(device: BluetoothDevice){
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.BLUETOOTH_CONNECT
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            val REQ_PERMISSION_CODE = 113
            ActivityCompat.requestPermissions(this@MainActivity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT),REQ_PERMISSION_CODE)
            return
        }
        try {
            bluetoothSocket = device.createRfcommSocketToServiceRecord(BT_UUID)
            bluetoothSocket.connect()
            anInputStream = bluetoothSocket.inputStream
        } catch(e: IOException) {
            e.printStackTrace()
            // Handle connection errors
        }
    }

    fun checkPermissions(){
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH) != PackageManager.PERMISSION_GRANTED ||
            ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_ADMIN) != PackageManager.PERMISSION_GRANTED) {

            val REQ_PERMISSION_CODE = 110
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.BLUETOOTH,
                    Manifest.permission.BLUETOOTH_ADMIN
                ),
                REQ_PERMISSION_CODE
            )
        }
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.BLUETOOTH_SCAN
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            val REQ_PERMISSION_CODE = 111
            ActivityCompat.requestPermissions(this@MainActivity, arrayOf(Manifest.permission.BLUETOOTH_SCAN),REQ_PERMISSION_CODE)
            return
        }
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.BLUETOOTH_CONNECT
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            val REQ_PERMISSION_CODE = 113
            ActivityCompat.requestPermissions(this@MainActivity, arrayOf(Manifest.permission.BLUETOOTH_CONNECT),REQ_PERMISSION_CODE)
            return
        }
    }



}



fun StartBT(anInputStream: InputStream) {
    var aThread = Thread(InteractAPI(anInputStream))
    aThread.start()
}


//Starter Code for UI
@Composable
fun theHeader(){
    Column(
        modifier = Modifier
            .height(40.dp)
            .fillMaxWidth()
            .background(Color.hsv( 210F, .29F, .29F))
    ) {
        Text(
            text = "PotPlug",
            fontFamily = FontFamily.Serif,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            modifier = Modifier.fillMaxWidth(),
            style = MaterialTheme.typography.headlineLarge,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
fun DeviceList(modifier: Modifier = Modifier,theList: SnapshotStateList<String> = mutableStateListOf<String>()) {
    Column(
        modifier.background(Color.hsl(209F, .34F, .12F))
    ) {
        LazyColumn {
            item {
                theHeader()
            }

            items(theList) {

            }


            item {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .fillMaxHeight(),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Button(onClick = {}) {
                        Text("Begin Receiving Data")
                    }
                }

            }
        }
    }

}

@SuppressLint("UnrememberedMutableState")
@Preview(showBackground = true)
@Composable
fun TitlePreview() {
    val anInputStream: InputStream = ByteArrayInputStream("test".toByteArray())
    var deviceList = mutableStateListOf<String>()
    MyApplicationTheme {
        DeviceList(Modifier.fillMaxSize(), deviceList)
    }
}

