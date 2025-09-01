// frontend/src/pages/LoginPage.tsx
import { useState } from "react";
import { GoogleLogin, type CredentialResponse } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import apiClient from "../services/apiClient";
import { useNavigate } from "react-router-dom";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGoogleSuccess = async (
    credentialResponse: CredentialResponse
  ) => {
    setError(null);
    setIsLoading(true);

    if (!credentialResponse.credential) {
      setError("No se recibió el token de credencial de Google.");
      setIsLoading(false);
      return;
    }

    try {
      console.log("Enviando token de Google al backend...");

      const res = await apiClient.post("/auth/google", {
        token: credentialResponse.credential,
      });

      console.log("Respuesta del backend recibida:", res.data);

      const { access_token } = res.data;
      if (!access_token) {
        throw new Error(
          "La respuesta del backend no contenía un access_token."
        );
      }

      console.log("¡Login exitoso! Guardando token JWT.");
      login(access_token);

      // Forzamos la navegación a la página principal después del login.
      navigate("/");
    } catch (err: any) {
      console.error("Error detallado en el inicio de sesión con Google:", err);
      const errorMessage =
        err.response?.data?.detail ||
        err.message ||
        "Ocurrió un error desconocido.";
      setError(`Error de inicio de sesión: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-slate-900">
      <div className="text-center p-10 bg-slate-800 rounded-lg shadow-xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-cyan-400 mb-2">
          Bienvenido a Atlas
        </h1>
        <p className="text-slate-400 mb-6">
          Inicia sesión para continuar con tu compañero de IA
        </p>

        <div className="flex justify-center">
          {isLoading ? (
            <div className="text-slate-300">Verificando...</div>
          ) : (
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                setError("Error al intentar iniciar sesión con Google.");
              }}
            />
          )}
        </div>

        {error && (
          <div className="mt-6 p-3 bg-red-900/50 border border-red-500/50 text-red-300 rounded-md text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
