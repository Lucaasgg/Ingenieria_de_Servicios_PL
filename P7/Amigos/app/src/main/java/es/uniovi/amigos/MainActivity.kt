package es.uniovi.amigos

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import androidx.preference.PreferenceManager
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker

class MainActivity : AppCompatActivity() {
    private var map: MapView? = null
    private val viewModel: MainViewModel by viewModels()

    private val updateReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "updateFromServer") {
                Log.d("MainActivity", "Aviso de FCM recibido! Actualizando amigos...")
                viewModel.getAmigosList()
            }
        }
    }

    private val requestPermissionLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                Log.d("Permissions", "Permiso de GPS CONCEDIDO")
                viewModel.startLocationUpdates()
            } else {
                Log.d("Permissions", "Permiso de GPS DENEGADO")
            }
        }

    private fun checkAndRequestLocationPermissions() {
        val permissionsToRequest = arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
        if (permissionsToRequest.all {
                ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
            }) {
            Log.d("Permissions", "Permisos ya concedidos. Iniciando GPS.")
            viewModel.startLocationUpdates()
        } else {
            Log.d("Permissions", "Solicitando permisos...")
            requestPermissionLauncher.launch(permissionsToRequest)
        }
    }

    private fun askUserName() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Identificacion")
        builder.setMessage("Introduce tu nombre de usuario:")
        val input = EditText(this)
        builder.setView(input)
        builder.setPositiveButton("Aceptar") { _, _ ->
            val name = input.text.toString()
            if (name.isNotBlank()) {
                viewModel.setUserName(name)
            }
        }
        builder.show()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        lifecycleScope.launch {
            withContext(Dispatchers.IO) {
                val ctx: Context = applicationContext
                Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx))
            }
            map = findViewById(R.id.map)
            map?.setTileSource(TileSourceFactory.MAPNIK)
            centrarMapaEnEuropa()
        }

        viewModel.amigosList.observe(this) { listaDeAmigos ->
            Log.d("MainActivity", "Observer notificado! Amigos: $listaDeAmigos")
            paintAmigosList(listaDeAmigos)
        }

        checkAndRequestLocationPermissions()
        askUserName()
    }

    override fun onResume() {
        super.onResume()
        map?.onResume()
        Log.d("MainActivity", "Registrando receptor de avisos FCM...")
        val filter = IntentFilter("updateFromServer")
        registerReceiver(updateReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
    }

    override fun onPause() {
        super.onPause()
        map?.onPause()
        Log.d("MainActivity", "Desregistrando receptor de avisos FCM...")
        unregisterReceiver(updateReceiver)
    }

    private fun centrarMapaEnEuropa() {
        val mapController = map?.controller
        mapController?.setZoom(5.5)
        val startPoint = GeoPoint(48.8583, 2.2944)
        mapController?.setCenter(startPoint)
    }

    private fun paintAmigosList(amigos: List<Amigo>) {
        map?.overlays?.clear()
        for (amigo in amigos) {
            val lat = amigo.lati.toDoubleOrNull() ?: continue
            val lon = amigo.longi.toDoubleOrNull() ?: continue
            addMarker(lat, lon, amigo.name)
        }
        map?.invalidate()
    }

    private fun addMarker(latitud: Double, longitud: Double, name: String?) {
        map?.let { mapaNoNulo ->
            val coords = GeoPoint(latitud, longitud)
            val startMarker = Marker(mapaNoNulo)
            startMarker.position = coords
            startMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_CENTER)
            startMarker.title = name
            mapaNoNulo.overlays.add(startMarker)
        }
    }
}
