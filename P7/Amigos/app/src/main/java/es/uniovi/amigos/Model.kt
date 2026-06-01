package es.uniovi.amigos

import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

data class Amigo(
    val id: Int,
    val name: String,
    val lati: String,
    val longi: String
)

interface AmigosApiService {
    @GET("api/amigos")
    suspend fun getAmigos(): Response<List<Amigo>>
}

object RetrofitClient {
    var BASE_URL = "http://192.168.1.148/"

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: AmigosApiService by lazy {
        retrofit.create(AmigosApiService::class.java)
    }
}
