import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axiosInstance";
import classes from "./ExistTeam.module.css";
import Button from "../Button/Button";
import Loader from "../Loader/Loader";

const ExistTeam = ({ onSelectTeam, onExist }) => {
  const [teams, setTeams] = useState([]);
  const [exist, setExist] = useState(false);
  const [loading, setLoading] = useState(false);
  const [expandedTeam, setExpandedTeam] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTeams = async () => {
      setLoading(true);
      try {
        const response = await api.get("/api/teams");
        if (!response.data.massage) {
          setExist(true);
          setTeams(response.data);
          onExist(true);
        }
      } catch (error) {
        setError("Ошибка при получении команд.");
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  const navigate = useNavigate();

  const handleExpandClick = (e, teamTitle) => {
    e.preventDefault();
    setExpandedTeam(expandedTeam === teamTitle ? null : teamTitle);
  };

  const handleSelectTeam = (e, team) => {
    e.preventDefault();
    setSelectedTeam(team);
    onSelectTeam(e, team);
  };

  const handleBack = () => navigate("/main");

  return (
    <>
      {loading && <Loader />}
      {!exist ? (
        <>
          <div className={classes.massage}>
            У вас нет ни одной команды.
            <br />
            Чтобы создать команду, создайте встречу <i>с новой командой.</i>
          </div>
          <Button text="Вернуться" onClick={handleBack} />
        </>
      ) : (
        teams.map((team) => (
          <div key={team.title} className={classes.team}>
            <span className={classes.teamTitleButton}>
              <Button
                onClick={(e) => handleSelectTeam(e, team)}
                text={team.title}
              />
            </span>
            <span className={classes.teamRollButton}>
              <Button
                onClick={(e) => handleExpandClick(e, team.title)}
                text={expandedTeam === team.title ? "▲" : "▼"}
              />
            </span>
            {expandedTeam === team.title && (
              <ul className={classes.membersList}>
                <br />
                <br />
                {team.members.map((member, index) => (
                  <li key={index}>
                    {member.name}
                    {" | "}
                    {member.group !== "" ? member.group : member.dep}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))
      )}
    </>
  );
};

export default ExistTeam;
