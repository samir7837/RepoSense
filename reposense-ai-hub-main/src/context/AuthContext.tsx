import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface AuthContextType {
  githubId: string | null;
  login: string | null;
  setAuth: (githubId: string, login: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [githubId, setGithubId] = useState<string | null>(null);
  const [login, setLogin] = useState<string | null>(null);

  useEffect(() => {
    const storedId = localStorage.getItem("github_id");
    const storedLogin = localStorage.getItem("github_login");
    if (storedId) {
      setGithubId(storedId);
      setLogin(storedLogin);
    }
  }, []);

  const setAuth = (id: string, loginName: string) => {
    localStorage.setItem("github_id", id);
    localStorage.setItem("github_login", loginName);
    setGithubId(id);
    setLogin(loginName);
  };

  const logout = () => {
    localStorage.removeItem("github_id");
    localStorage.removeItem("github_login");
    setGithubId(null);
    setLogin(null);
  };

  return (
    <AuthContext.Provider value={{ githubId, login, setAuth, logout, isAuthenticated: !!githubId }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
