import { useState, useEffect } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import checkAuth from "../../api/checkAuth";
import classes from "./ActiveMeetPage.module.css";
import api from "../../api/axiosInstance";
import Button from "../../components/Button/Button";
import TimeTable from "../../components/TimeTable/TimeTable";
import DeleteModal from "../../components/Modal/DeleteModal";
import Loader from "../../components/Loader/Loader";

function ActiveMeetPage() {
  const [loading, setLoading] = useState(false);
  const [timeTable, setTimeTable] = useState({
    schedule: {},
    d_m_date: [],
    d_of_week: [],
  });
  const [timeIdate, setTimeIdate] = useState({
    time: "",
    date: "",
  });
  const [selectedMeeting, setSelectedMeeting] = useState(null);
  const [showParticipants, setShowParticipants] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const timeForLessons = [
    "08:30 - 10:00",
    "10:15 - 11:45",
    "12:00 - 13:30",
    "14:00 - 15:30",
    "15:45 - 17:15",
    "17:30 - 19:00",
    "19:15 - 20:45",
  ];

  useEffect(() => {
    const getData = async () => {
      try {
        setLoading(true);
        const data = await api.get("/active_meet");
        console.log(data);
        setTimeTable(data.data);
      } catch (error) {
        console.log(error);
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, []);

  const cellStyles = {
    lessonActive: "rgb(240, 230, 140)",
    lessonInactive: "rgb(255, 250, 250)",
    activeButtonColor: "rgb(189, 183, 107)", // Active button color
  };

  const handleTimeIdate = ({ date, time }) => {
    const [day, month, year] = date.split(".");
    const formattedDate = `20${year}-${month}-${day}`;
    setTimeIdate({ date: formattedDate, time });
    const selectedDay = timeTable.schedule.days.find(
      (day) => day.date === formattedDate
    );
    if (selectedDay) {
      const dayKey = `day ${timeTable.d_m_date.indexOf(date) + 1}`;
      const lessonKey = `lesson ${timeForLessons.indexOf(time) + 1}`;
      const meeting = selectedDay[dayKey][lessonKey];
      setSelectedMeeting(meeting);
      setShowParticipants(false);
    }
  };

  const handleCancel = () => {
    setSelectedMeeting(null);
    setTimeIdate({ time: "", date: "" });
  };

  const newDate = (dateString) => {
    const [year, month, day] = dateString.split('-');
    const shortYear = year.slice(2); // удаляем первые две цифры года
    return `${day}.${month}.${shortYear}`;
  };

  const handleDelete = async () => {
    const { date, time } = timeIdate;
    const { type, theme } = selectedMeeting;
    try {
      const response = await api.post("/delete_meet", {
        date,
        time,
        type,
        theme,
      });
      const updatedSchedule = { ...timeTable.schedule };
      const dayIndex = timeTable.d_m_date.indexOf(newDate(date));
      const lessonIndex = timeForLessons.indexOf(time);
      const dayKey = `day ${dayIndex + 1}`;
      const lessonKey = `lesson ${lessonIndex + 1}`;
      updatedSchedule.days[dayIndex][dayKey][lessonKey] = 0;
      setTimeTable({ ...timeTable, schedule: updatedSchedule });
      setIsModalOpen(false);
      handleCancel();
    } catch (error) {
      console.log("Ошибка при удалении встречи:", error);
    }
  };

  const handleOpenList = () => {
    setShowParticipants(true);
  };
  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  if (!checkAuth()) {
    return <Navigate to="/login" />;
  } else {
    return (
      <div className={classes.page}>
        {loading && <Loader />}
        <div className={classes.title}>Активные встречи</div>
        <br />
        <TimeTable
          dOfWeek={timeTable.d_of_week}
          dMDate={timeTable.d_m_date}
          schedule={timeTable.schedule}
          onChange={handleTimeIdate}
          styles={cellStyles}
        />
        {selectedMeeting && (
          <div className={classes.details}>
            <div className={classes.infotitle}>Детали встречи</div>
            <div className={classes.info}>
              <strong>Тема:</strong> {selectedMeeting.theme}
            </div>
            <div className={classes.info}>
              <strong>Тип:</strong> {selectedMeeting.type}
            </div>
            <div className={classes.info}>
              <strong>
                {selectedMeeting.type === "Очная" ? "Место" : "Ссылка"}:
              </strong>{" "}
              {selectedMeeting.meet}
            </div>
            <Button text="Закрыть" onClick={handleCancel} />
            <Button text="Список участников" onClick={handleOpenList} />
            <Button text="Удалить" onClick={openModal} />
            {showParticipants && (
              <div className={classes.participantList}>
                <ul className={classes.infotitle}>
                  Участники встречи
                  {selectedMeeting.members.map((member, index) => (
                    <li className={classes.info} key={index}>
                      {member}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {isModalOpen && (
              <DeleteModal
                message={`Вы уверены, что хотите удалить встречу?`}
                onConfirm={handleDelete}
                onCancel={closeModal}
              />
            )}
          </div>
        )}
      </div>
    );
  }
}

export default ActiveMeetPage;
