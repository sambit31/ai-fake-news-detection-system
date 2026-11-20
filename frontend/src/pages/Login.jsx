
import { useNavigate } from "react-router-dom";
import AuthPage from "../components/auth/AuthPage";

export default function Login() {
  const navigate = useNavigate();

  return (
    <AuthPage
      initialMode="login"
      onBack={() => navigate("/")}
      onAuthenticated={() => navigate("/")}
    />
  );
}
