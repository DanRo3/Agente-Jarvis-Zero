// frontend/src/components/auth/ProtectedRoute.tsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import type { JSX } from "react";

export function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { token, isLoading } = useAuth();

  if (isLoading) {
    return <div>Cargando...</div>; // O un spinner bonito
  }

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
