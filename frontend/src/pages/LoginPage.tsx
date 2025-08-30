// frontend/src/pages/LoginPage.tsx
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import apiClient from "../services/apiClient";

export function LoginPage() {
  const { login } = useAuth();

  const handleGoogleSuccess = async (credentialResponse: any) => {
    try {
      // Enviamos el token de Google a nuestro backend
      const res = await apiClient.post("/auth/google", {
        token: credentialResponse.credential,
      });

      // Si el backend lo valida, nos devuelve nuestro propio token JWT
      const { access_token } = res.data;
      login(access_token); // Guardamos el token en nuestro estado global
      // Seremos redirigidos automáticamente por el router
    } catch (error) {
      console.error("Error en el inicio de sesión con Google:", error);
      alert("No se pudo iniciar sesión. Revisa la consola.");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-slate-900">
      <div className="text-center p-10 bg-slate-800 rounded-lg shadow-xl">
        <h1 className="text-3xl font-bold text-cyan-400 mb-2">
          Bienvenido a Atlas
        </h1>
        <p className="text-slate-400 mb-6">Inicia sesión para continuar</p>
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => {
            console.log("Login Failed");
          }}
        />
      </div>
    </div>
  );
}
