package es.uniovi.amigos

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.google.firebase.messaging.FirebaseMessaging
import kotlinx.coroutines.delay
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val _amigosList = MutableLiveData<List<Amigo>>()
    val amigosList: LiveData<List<Amigo>> = _amigosList

    private val locationFlow = application.createLocationFlow()

    private var userName: String? = null
    var userId: Int? = null

    init {
        Log.d("MainViewModel", "MainViewModel created")
        startPolling()
    }

    fun getAmigosList() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigos()
                if (!response.isSuccessful) {
                    Log.e("MainViewModel", "Error: \${response.code()}")
                    return@launch
                }
                val body = response.body()
                if (body == null) {
                    Log.e("MainViewModel", "Lista nula")
                    return@launch
                }
                _amigosList.setValue(body)
                Log.d("MainViewModel", "Amigos recibidos: \${amigosList.value}")
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepcion", e)
            }
        }
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (true) {
                Log.d("Polling", "Pidiendo amigos...")
                getAmigosList()
                delay(5000)
            }
        }
    }

    fun startLocationUpdates() {
        viewModelScope.launch {
            locationFlow.collect { result ->
                if (result is LocationResult.NewLocation) {
                    val location = result.location
                    Log.d("GPS", "Nueva ubicacion: \${location.latitude}, \${location.longitude}")
                    userId?.let { idNoNulo ->
                        try {
                            val payload = LocationPayload(
                                lati = location.latitude.toString(),
                                longi = location.longitude.toString()
                            )
                            RetrofitClient.api.updateAmigoPosition(idNoNulo, payload)
                            Log.d("GPS", "Posicion actualizada en backend")
                        } catch (e: Exception) {
                            Log.e("GPS", "Error actualizando posicion", e)
                        }
                    }
                } else if (result is LocationResult.ProviderDisabled) {
                    Log.w("GPS", "GPS desactivado")
                }
            }
        }
    }

    fun setUserName(name: String) {
        userName = name
        Log.d("MainViewModel", "Nombre establecido: \$userName")
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigoByName(name)
                if (!response.isSuccessful) {
                    Log.e("MainViewModel", "Error buscando amigo: \${response.code()}")
                    return@launch
                }
                val amigo = response.body()
                if (amigo == null) {
                    Log.e("MainViewModel", "Amigo no encontrado")
                    return@launch
                }
                userId = amigo.id
                Log.d("MainViewModel", "Id del usuario: \$userId")
                try {
                    val token = FirebaseMessaging.getInstance().token.await()
                    Log.d("MainViewModel", "Token FCM: \$token")
                    RetrofitClient.api.updateAmigoDeviceToken(amigo.id, DeviceTokenPayload(token))
                    Log.d("MainViewModel", "Token enviado al backend")
                } catch (ex: Exception) {
                    Log.e("MainViewModel", "Error obteniendo/enviando token FCM", ex)
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepcion buscando amigo", e)
            }
        }
    }
}
