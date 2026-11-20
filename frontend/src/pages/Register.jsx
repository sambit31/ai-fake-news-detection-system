
import { useNavigate } from "react-router-dom";
import AuthPage from "../components/auth/AuthPage";

export default function Register() {
  const navigate = useNavigate();

  return (
    <AuthPage
      initialMode="register"
      onBack={() => navigate("/")}
      onAuthenticated={() => navigate("/")}
    />
  );
}
