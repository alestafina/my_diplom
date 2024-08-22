import { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import api from "../../api/axiosInstance";
import classes from "./MainPage.module.css";
import Button from "../../components/Button/Button";
import Modal from "../../components/Modal/Modal";
import checkAuth from "../../api/checkAuth";
import Loader from "../../components/Loader/Loader";

function MainPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [type, setType] = useState("");
  const [load,setLoad] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getData();
  }, []);

  useEffect(() => {
    if (type === "existing" || type === "new") {
      handleCreateMeeting(type);
    }
  }, [type]);

  const handleCreate = () => {
    setIsModalOpen(true);
  };

  const getData = async () => {
    try {setLoad(true);
    const data = await api.get("/api/main");
    setName(data.data.name);
    setEmail(data.data.corp_mail);} catch(error) {
      console.log(error);
    } finally {
      setLoad(false);
    }
  };

  const additionalButtons = [
    {
      text: "С существующей командой",
      onClick: () => setType("existing"),
    },
    {
      text: "С новой командой",
      onClick: () => setType("new"),
    },
    {
      text: "Отмена",
      onClick: () => handleModalClose(),
    },
  ];

  const handleCreateMeeting = (type) =>
    navigate("/new_meeting", { state: { data: type } });

  const handleMyTeams = () => navigate("/my_teams");
  const handleActiveMeet = () => navigate("/active_meetings");

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  if (!checkAuth()) {
    return <Navigate to="/login" />;
  } else {
    return (
      <div className={classes.page}>
        {load && <Loader />}
        <div className={classes.lk}>Личный кабинет</div>
        <div className={classes.fio}>
          ФИО: <span>{name}</span>{" "}
        </div>
        <div className={classes.mail}>
          Почта: <span>{email}</span>{" "}
        </div>
        <Button
          className={classes.Button}
          onClick={handleActiveMeet}
          text="Активные встречи"
        />
        <Button
          className={classes.Button}
          onClick={handleMyTeams}
          text="Мои команды"
        />
        <div className={classes.create}>
          <Button onClick={handleCreate} text="Создать встречу" />
        </div>
        {isModalOpen && <Modal additionalButtons={additionalButtons} />}
      </div>
    );
  }
}

export default MainPage;
