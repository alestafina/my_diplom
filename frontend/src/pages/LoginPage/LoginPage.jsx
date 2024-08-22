import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axiosInstance";
import Button from "../../components/Button/Button";
import classes from "./LoginPage.module.css";
import Loader from "../../components/Loader/Loader";

function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  
  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!email || !password) {
      setError("Необходимо указать логин и пароль");
      setTimeout(() => setError(""), 8000);
      return; 
    }
    try {
      setLoading(true);
      const response = await api.post("/api/login", { email, password });
      console.log("Успешная аутентификация:", response.data);
      navigate("/main");
    } catch (error) {
      console.error("Ошибка аутентификации:", error);
      setError("Пожалуйста, проверьте логин и пароль.");
      setTimeout(() => setError(""), 8000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className={classes.container}>
      {loading && <Loader />}
      <h2 className={classes.container}>Авторизация</h2>
      <form className={classes.form} onSubmit={handleSubmit}>
        <div>
          <input
            placeholder="Корпоративная почта НГТУ"
            className={classes.input}
            type="text"
            id="email"
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <div>
          <input
            placeholder="Пароль"
            className={classes.input}
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </div>
        <Button className={classes.button} type="submit" text="Войти" />
      </form>
      {error && <div className={classes.error}>{error}</div>}
    </section>
  );
}

export default LoginPage;
