// frontend/src/pages/ChatPage.tsx
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export function ChatPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="bg-slate-900 text-slate-200 h-screen">
      <header className="flex items-center justify-between p-4 border-b border-slate-700">
        <h1 className="text-xl font-bold text-cyan-400">Atlas</h1>
        <div className="flex items-center gap-4">
          <p>Bienvenido, {user?.email}</p>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded-md text-sm font-semibold"
          >
            Cerrar Sesión
          </button>
        </div>
      </header>
      <main>
        {/* Aquí integraremos nuestra UI de chat y monitoreo en el siguiente paso */}
        <p className="p-4">¡Dashboard del Chat! Próximamente...</p>
      </main>
    </div>
  );
}
