import { Github } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { authApi } from "@/services/api";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/60 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-6">
        <Link to="/" className="text-xl font-bold tracking-tight">
          <span className="gradient-text">Repo</span>
          <span className="text-foreground">Sense</span>
        </Link>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard">
                <Button variant="ghost" size="sm">Dashboard</Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout}>Logout</Button>
            </>
          ) : (
            <a href={authApi.loginUrl}>
              <Button size="sm" className="gap-2 bg-primary hover:bg-primary/90">
                <Github className="h-4 w-4" />
                Login with GitHub
              </Button>
            </a>
          )}
        </div>
      </div>
    </nav>
  );
}
