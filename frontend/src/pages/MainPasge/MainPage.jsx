import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import classes from "./MainPage.module.css";
import Button from "../../components/Button/Button";
import Nav from "../../components/Nav/Nav";
import Modal from "../../components/Modal/Modal";
import checkAuth from "../../api/checkAuth";

function MainPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const handleClick = () => {
    alert("Кнопка нажата!");
  };

  const handleCreate = () => {
    setIsModalOpen(true);
  };

  const additionalButtons = [
    {
      text: "С существующей командой",
      onClick: () => handleCreateMeeting("existing"),
    },
    {
      text: "С новой командой",
      onClick: () => handleCreateMeeting("new"),
    },
    {
      text: "Отмена",
      onClick: () => handleModalClose(),
    },
  ];

  const handleCreateMeeting = (type) => {
    if (type === "new") {
      navigate("/new_meeting");
    } else {
    }
  };

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
              winName="Создать встречу"
              additionalButtons={additionalButtons}
            />
          )}
        </div>
      </>
    );
  }
}

export default MainPage;
