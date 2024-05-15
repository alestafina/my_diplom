import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import checkAuth from "../../api/checkAuth";
import classes from "./NewMeetPage.module.css";
import api from "../../api/axiosInstance";
import Button from "../../components/Button/Button";
import DeleteButton from "../../components/DeleteButton";
import BasicInfo from "../../components/BasicInfo/BasicInfo";
import TimeTable from "../../components/TimeTable/TimeTable";

function NewMeetPage() {
  const [participants, setParticipants] = useState([{ id: 0, name: "" }]);
  const [groupValues, setGroupValues] = useState([""]);
  const [depValues, setDepValues] = useState([""]);
  const [save, setSave] = useState(false);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [timeIdate, setTimeIdate] = useState({
    time: "",
    date: "",
  });
  const [timeTable, setTimeTable] = useState({
    free: {},
    d_m_date: {},
    time_for_lsns: [],
    d_of_week: [],
  });
  const [basicInfo, setBasicInfo] = useState({
    type: null,
    theme: "",
    meet: "",
  });
  const navigate = useNavigate();

  const handleBasicInfo = (basicInfoData) => setBasicInfo(basicInfoData);

  const handleTimeIdate = (timeIdate) => setTimeIdate(timeIdate); 

  // создаем объекты участников
  const addFields = (e) => {
    e.preventDefault();
    setParticipants([...participants, { id: participants.length }]);
    setGroupValues([...groupValues, ""]);
    setDepValues([...depValues, ""]);
  };

  const handleInputChange = (index, name, value) => {
    const newParticipants = [...participants];
    newParticipants[index][name] = value;
    setParticipants(newParticipants);
  };

  const handleDelete = (id) => {
    setParticipants((prevParticipants) =>
      prevParticipants.filter((participant) => participant.id !== id)
    );
    setGroupValues((prevValues) => prevValues.filter((_, i) => i !== id));
    setDepValues((prevValues) => prevValues.filter((_, i) => i !== id));
  };

  const handleGroupChange = (index, value) => {
    const newValues = [...groupValues];
    newValues[index] = value;
    setGroupValues(newValues);
    setDepValues((prevValues) =>
      prevValues.map((_, i) => (i === index ? "" : prevValues[i]))
    );
    const newParticipants = participants.map((participant, i) => {
      if (i === index) {
        return { ...participant, group: value };
      }
      return participant;
    });
    setParticipants(newParticipants);
  };

  const handleDepChange = (index, value) => {
    const newValues = [...depValues];
    newValues[index] = value;
    setDepValues(newValues);
    setGroupValues((prevValues) =>
      prevValues.map((_, i) => (i === index ? "" : prevValues[i]))
    );
    const newParticipants = participants.map((participant, i) => {
      if (i === index) {
        return { ...participant, department: value };
      }
      return participant;
    });
    setParticipants(newParticipants);
  };
  
  const handleSave = (e) => {
    setSave(e.target.checked);
  };

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };


  // отправляем серверу наших участников
  const handleSubmit = async (e) => {
    e.preventDefault();
    let data = {
      name: participants.map((participant) => participant.name),
      group: participants.map((participant) => participant.group),
      department: participants.map((participant) => participant.department),
      save,
    };
    if (save) {
      data = { ...data, title };
    }
    if (data.save && !data.title) {
      setError("Введите название команды.");
      setTimeout(() => setError(""), 5000);
    } else {
      try {
        const result = await api.post("/new_meeting", data);
        console.log("Данные успешно отправлены:", result);
        setTimeTable(result.data);
      } catch (error) {
        console.log("Ошибка при отправке данных:", error);
        setError(error.response.data.error);
        setTimeout(() => setError(""), 5000);
      }
    }
  };

  // отправляем дату, время и остальное
  const handleSubmitAll = async (e) => {
    e.preventDefault();
    const data = {
      names: participants.map((participant) => participant.name),
      type: basicInfo.type,
      theme: basicInfo.theme,
      meet: basicInfo.meet,
      time: timeIdate.time,
      date: timeIdate.date,
    };
    if (!timeIdate.time || !timeIdate.date) {
      setError("Для выбора нажмите на ячейку.");
      setTimeout(() => setError(""), 5000);
    } else if (!data.type) {
      setError("Укажите тип встречи.");
      setTimeout(() => setError(""), 5000);
    } else if (!data.meet) {
      setError(
        `Укажите ${
          type === "online"
            ? "ссылку для проведения совещания"
            : "место проведения совещания"
        }.`
      );
      setTimeout(() => setError(""), 5000);
    } else {
      try {
        const result = await api.post("/choice", data);
        console.log("Данные успешно отправлены:", result);
        navigate("/main");
      } catch (error) {
        console.log("Ошибка при отправке данных:", error);
        setError(error.response.data.error);
        setTimeout(() => setError(""), 5000);
      }
    }
  };

  if (!checkAuth()) {
    return <Navigate to="/login" />;
  } else {
    return (
      <>
        <section className={classes.page}>
          <form className={classes.form}>
            {!timeTable.schedule ? (
              <>
                <div>
                  <span className={classes.span}>
                    Введите список участников
                  </span>{" "}
                  <br />
                  {participants.map((participant, index) => (
                    <div key={index}>
                      <input
                        placeholder="Фамилия Имя Отчество"
                        className={classes.input}
                        type="text"
                        id={`fio_${index}`}
                        value={participant.name || ""}
                        onChange={(e) =>
                          handleInputChange(index, "name", e.target.value)
                        }
                      />
                      <input
                        placeholder="Группа"
                        className={`${classes.input} ${
                          depValues[index] !== "" ? classes.disabled : ""
                        }`}
                        type="text"
                        id={`group_${index}`}
                        value={groupValues[index]}
                        onChange={(e) =>
                          handleGroupChange(index, e.target.value)
                        }
                      />
                      <span className={classes.or}>или </span>
                      <input
                        placeholder="Кафедра"
                        className={`${classes.input} ${
                          groupValues[index] !== "" ? classes.disabled : ""
                        }`}
                        type="text"
                        id={`dep_${index}`}
                        value={depValues[index]}
                        onChange={(e) => handleDepChange(index, e.target.value)}
                      />

                      <DeleteButton
                        onClick={() => handleDelete(participant.id)}
                      />
                    </div>
                  ))}
                  <Button text="Добавить участника" onClick={addFields} />
                </div>
                <label>
                  <input type="checkbox" value={save} onChange={handleSave} />
                  Сохранить команду
                </label>
                {save && (
                  <>
                    <br />
                    <p>Введите название команды:</p>
                    <input
                      type="text"
                      value={title}
                      placeholder="Назвние команды"
                      onChange={handleTitleChange}
                    />
                  </>
                )}
                <br />
                <Button
                  text="Перейти к выбору даты"
                  type="submit"
                  onClick={handleSubmit}
                />
                <br />{" "}
              </>
            ) : (
              <>
                <span className={classes.span}>Выберете дату и время:</span>
                <TimeTable
                  dOfWeek={timeTable.d_of_week}
                  dMDate={timeTable.d_m_date}
                  schedule={timeTable.schedule}
                  onChange={handleTimeIdate}
                />
                <br />
                <BasicInfo onChange={handleBasicInfo} />
                <br />
                <Button
                  text="Создать встречу"
                  type="submit"
                  onClick={handleSubmitAll}
                />
              </>
            )}
          </form>
        </section>
        {error && <div className={classes.error}>{error}</div>}
      </>
    );
  }
}
export default NewMeetPage;
