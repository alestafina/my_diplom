import { useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import classes from "./MainPage.module.css";
import Button from "../../components/Button/Button";
import Modal from "../../components/Modal/Modal";
import checkAuth from "../../api/checkAuth";

function MainPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [type, setType] = useState("");
  const navigate = useNavigate();
  useEffect(() => {
    if (type === "existing" || type === "new") {
      handleCreateMeeting(type);
    }
  }, [type]); 

  const handleClick = () => {
    alert("Кнопка нажата!");
  };

  const handleCreate = () => {
    setIsModalOpen(true);
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

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  if (!checkAuth()) {
    return <Navigate to="/login" />;
  } else {
    return (
      <>
        <div className={classes.page}>
          <div className={classes.lk}>Личный кабинет</div>
          <div className={classes.fio}>ФИО: {} </div>
          <Button
            className={classes.Button}
            onClick={handleClick}
            text="Активные встречи"
          />
          <Button
            className={classes.Button}
            onClick={handleClick}
            text="Мои команды"
          />
          <div className={classes.create}>
            <Button onClick={handleCreate} text="Создать встречу" />
          </div>
          {isModalOpen && (
            <Modal
              additionalButtons={additionalButtons}
            />
          )}
        </div>
      </>
    );
  }
}

export default MainPage;
