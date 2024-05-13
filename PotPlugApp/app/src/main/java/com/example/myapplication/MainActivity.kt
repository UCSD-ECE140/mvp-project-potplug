package com.example.myapplication

import android.Manifest
import android.app.Activity
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapplication.ui.theme.MyApplicationTheme
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothSocket
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresApi
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.io.IOException
import java.util.UUID

class MainActivity : ComponentActivity() {
    lateinit var bluetoothAdapter:BluetoothAdapter
    private var deviceList = mutableListOf<String>()
    private val BT_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
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
        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                            name = "Android",
                            modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
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



        // Start device discovery

        bluetoothAdapter.startDiscovery()

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
            val bluetoothSocket: BluetoothSocket = device.createRfcommSocketToServiceRecord(BT_UUID)
            bluetoothSocket.connect()
        } catch(e: IOException) {
            e.printStackTrace()
            // Handle connection errors
        }
    }
}



//Starter Code for UI
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
            text = "Hello $name!",
            modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyApplicationTheme {
        Greeting("Android")
    }
}