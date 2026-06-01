package es.uniovi.amigos

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {
    private val _amigosList = MutableLiveData<List<Amigo>>()
    val amigosList: LiveData<List<Amigo>> = _amigosList

    init {
        Log.d("MainViewModel", "MainViewModel created")
        startPolling()
    }

    fun getAmigosList() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigos()
                if (!response.isSuccessful) {
                    Log.e("MainViewModel", "Error al obtener los amigos: ${response.code()}")
                    return@launch
                }
                val body = response.body()
                if (body == null) {
                    Log.e("MainViewModel", "Lista de amigos es nula")
                    return@launch
                }
                _amigosList.setValue(body)
                Log.d("MainViewModel", "Amigos recibidos: ${amigosList.value}")
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepcion al obtener los amigos", e)
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
}
