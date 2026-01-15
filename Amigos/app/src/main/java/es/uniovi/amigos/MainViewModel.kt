package es.uniovi.amigos

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {
    private var amigosList: List<MainActivity.Amigo>? = null // Por defecto es nula

    init {
        Log.d("MainViewModel", "MainViewModel created")
    }

    fun getAmigosList() {
        viewModelScope.launch {
            try {
                val response = MainActivity.RetrofitClient.api.getAmigos()
                if (!response.isSuccessful) {
                    Log.e("MainActivity", "Error al obtener los amigos: ${response.code()}")
                    return@launch
                }
                val amigosList = response.body()
                if (amigosList == null) {
                    Log.e("MainActivity", "Lista de amigos es nula")
                    return@launch
                }
                Log.d("MainViewModel", "Amigos: $amigosList")
            } catch (e: Exception) {
                Log.e("MainActivity", "Excepción al obtener los amigos", e)
            }
        }
    }
}