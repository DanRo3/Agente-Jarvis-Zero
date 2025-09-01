// frontend/src/App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { LoginPage } from "./pages/LoginPage";
import { ChatLayout } from "./pages/ChatLayout";
import { ChatPage } from "./pages/ChatPage";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <ChatLayout />
              </ProtectedRoute>
            }
          >
            {/* Rutas anidadas que se renderizarán dentro de ChatLayout */}
            <Route path="chat/:sessionId" element={<ChatPage />} />
            <Route
              index
              element={
                <div className="h-full grid place-content-center text-slate-500">
                  Selecciona o crea una nueva conversación
                </div>
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
