package es.uniovi.amigos

import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.Path

data class Amigo(
    val id: Int,
    val name: String,
    val lati: String,
    val longi: String
)

data class DeviceTokenPayload(
    val device: String
)

data class LocationPayload(
    val lati: String,
    val longi: String
)

interface AmigosApiService {
    @GET("api/amigos")
    suspend fun getAmigos(): Response<List<Amigo>>

    @GET("api/amigo/byName/{name}")
    suspend fun getAmigoByName(@Path("name") name: String): Response<Amigo>

    @PUT("api/amigo/{id}")
    suspend fun updateAmigoPosition(
        @Path("id") amigoId: Int,
        @Body payload: LocationPayload
    ): Response<Amigo>

    @retrofit2.http.PUT("api/amigo/{id}")
    suspend fun updateAmigoDeviceToken(
        @Path("id") amigoId: Int,
        @retrofit2.http.Body payload: DeviceTokenPayload
    ): Response<Amigo>
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
