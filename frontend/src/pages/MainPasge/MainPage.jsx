import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import classes from "./MainPage.module.css"
import Button from "../../components/Button/Button";
import Nav from "../../components/Nav/Nav";
import api from "../../api/axiosInstance";

function MainPage() {
  const [auth, setAuth] = useState(true);

  useEffect(() => {
    isAuth();
  }, []);

  const isAuth = async () => {
    try {
      const response = await api.get("/checkAuth");
      setAuth(response.data.isAuth);
    } catch (error) {
      console.error(error);
    }
  };

  const handleClick = () => {
    alert("Кнопка нажата!");
  };

  if (!auth) {
    return <Navigate to="/login" />;
  } else {
    return (
      <>
        <Nav />
        <div>Личный кабинет</div>
        <div>ФИО: {} </div>
        <Button className={classes.Button} onClick={handleClick} text="Активные встречи" />
        <Button className={classes.Button} onClick={handleClick} text="Мои команды" />
        <Button className={classes['Button_create']} onClick={handleClick} text="Создать встречу" />
      </>
    );
  }
}

export default MainPage;
