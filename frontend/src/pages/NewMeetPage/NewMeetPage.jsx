import { useState, useEffect } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import checkAuth from "../../api/checkAuth";
import classes from "./NewMeetPage.module.css";
import api from "../../api/axiosInstance";
import Button from "../../components/Button/Button";
import Participants from "../../components/Participants/Participants";
import ExistTeam from "../../components/ExistTeam/ExistTeam";
import BasicInfo from "../../components/BasicInfo/BasicInfo";
import TimeTable from "../../components/TimeTable/TimeTable";
import Loader from "../../components/Loader/Loader";

function NewMeetPage() {
  const [back, setBack] = useState(false);
  const [exist, setExist] = useState(false);
  const [loading, setLoading] = useState(false);
  const [save, setSave] = useState(false);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [participants, setParticipants] = useState({
    participants: [{ id: 0, name: "" }],
    groups: [""],
    deps: [""],
  });
  const [timeIdate, setTimeIdate] = useState({
    time: "",
    date: "",
  });
  const [timeTable, setTimeTable] = useState({
    schedule: {},
    d_m_date: [],
    d_of_week: [],
  });
  const [basicInfo, setBasicInfo] = useState({
    type: null,
    theme: "",
    meet: "",
  });
  const navigate = useNavigate();
  const location = useLocation();
  const type = location.state.data;

  const cellStyles = {
    lessonActive: "rgb(152, 251, 152)",
    lessonInactive: "rgb(255, 182, 193)",
    activeButtonColor: "rgb(144, 238, 144)"
  };

  const handleParticipantChange = (participants, groups, deps) => {
    setParticipants({
      participants: participants.map((participant) => participant.name),
      groups: groups,
      deps: deps,
    });
  };
  const handleBasicInfo = (basicInfoData) => setBasicInfo(basicInfoData);
  
  const handleTimeIdate = (timeIdate) => setTimeIdate(timeIdate);
  
  const handleSave = (e) => {
    setSave(e.target.checked);
  };
  
  const handleTitleChange = (e) => {
    setTitle(e.target.value);
  };
  
  const handleCancel = (e) => {
    e.preventDefault();
    setBack(false);
  };
  
  const updateExist = (value) => {
    setExist(value);
  };

  const handleSelectTeam = (e, team) => {
    e.preventDefault();
    const names = team.members.map((member) => member.name);
    const groups = team.members.map((member) => member.group);
    const deps = team.members.map((member) => member.dep);
    setParticipants({ participants: names, groups, deps });
  };
  
  // отправляем серверу участников
  const handleSubmit = async (e) => {
    e.preventDefault();
    let data = {
      name: participants.participants,
      group: participants.groups,
      department: participants.deps,
      save,
    };
    console.log(data);
    if (save) {
      data = { ...data, title };
    }
    if (data.save && !data.title) {
      setError("Введите название команды.");
      setTimeout(() => setError(""), 5000);
    } else {
      try {
        setLoading(true);
        const result = await api.post("/new_meeting", data);
        console.log("Данные успешно отправлены:", result);
        setTimeTable(result.data);
        setBack(true);
      } catch (error) {
        console.log("Ошибка при отправке данных:", error);
        setError(error.response.data.error);
        setTimeout(() => setError(""), 5000);
      } finally {
        setLoading(false);
      }
    }
  };
  
  // отправляем дату, время и остальное
  const handleSubmitAll = async (e) => {
    e.preventDefault();
    const data = {
      names: participants.participants,
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
          data.type === "online"
            ? "ссылку для проведения совещания."
            : "место проведения совещания."
        }.`
      );
      setTimeout(() => setError(""), 5000);
    } else {
      try {
        const result = await api.post("/choice", data);
        console.log("Данные успешно отправлены:", result.data);
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
      {loading && <Loader />}
        <section className={classes.page}>
          <form className={classes.form}>
            {!back ? (
              type === "new" ? (
                <>
                  <Participants
                    onChange={handleParticipantChange}
                  />
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
                        placeholder="Название команды"
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
                </>
              ) : (
                <>
                {exist && <><span className={classes.span}>Выберите команду</span><br /></>}
                  <ExistTeam onSelectTeam={handleSelectTeam} onExist={updateExist} />
                  {exist && <Button
                    text="Перейти к выбору даты"
                    type="submit"
                    onClick={handleSubmit}
                  />}
                </>
              )
            ) : (
              <>
                <span className={classes.span}>Выберите дату и время:</span>
                <TimeTable
                  dOfWeek={timeTable.d_of_week}
                  dMDate={timeTable.d_m_date}
                  schedule={timeTable.schedule}
                  onChange={handleTimeIdate}
                  styles={cellStyles}
                />
                <br />
                <BasicInfo onChange={handleBasicInfo} />
                <br />
                <Button
                  text="Создать встречу"
                  type="submit"
                  onClick={handleSubmitAll}
                />
                <Button
                  text="Вернуться к списку участников"
                  onClick={handleCancel}
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
