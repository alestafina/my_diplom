import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Button/Button";
import classes from "./Nav.module.css";
import api from "../../api/axiosInstance";

function Nav() {
  const navigate = useNavigate();
  const [week, setWeek] = useState(0);

  useEffect(() => {
    weekNumber()
  }, []);

  const weekNumber = async () => {
    try {
      const response = await api.get("/main");
      setWeek(response.data.week)
    } catch(error) {
      console.log(error)
    }
  };

  const handleLogout = async () => {
    try {
      const response = await api.post("/logout");
      console.log(response.data);
      navigate("/login");
    } catch (error) {
      console.error("Ошибка при выходе из системы:", error);
    }
  };

  return ( <>
    <ul className={classes.Nav}>
      <li className={classes.li}>
        <div className={classes.name} href="#">
          MEETING
        </div>
      </li>
          <li className={classes.li}>
            <a href="#">Активные встречи</a>
          </li>
          <li className={classes.li}>
            <a href="#">Мои команды</a>
          </li>
          <li className={classes.li}>
            <a href="#">Личный кабинет</a>
          </li>
          <li className={classes.li}>
            <Button onClick={handleLogout} text="Выход" />
          </li>
          <p className={classes.p}> {week} учебная неделя </p>
    </ul>
    </>
  );
}

export default Nav;
