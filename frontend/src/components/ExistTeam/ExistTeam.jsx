import { useEffect, useState } from "react";
import api from "../../api/axiosInstance";
import classes from "./ExistTeam.module.css";
import Button from "../Button/Button";

const ExistTeam = ({ onSelectTeam }) => {
  const [teams, setTeams] = useState([]);
  const [expandedTeam, setExpandedTeam] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await api.get("/teams");
        setTeams(response.data);
      } catch (error) {
        setError("Ошибка при получении команд.");
      }
    };

    fetchTeams();
  }, []);

  const handleExpandClick = (e, teamTitle) => {
    e.preventDefault();
    setExpandedTeam(expandedTeam === teamTitle ? null : teamTitle);
  };

  const handleSelectTeam = (e, team) => {
    e.preventDefault();
    setSelectedTeam(team);
    onSelectTeam(e, team.members);
  };

  return (
    <>
      {teams.map((team) => (
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
            <ul className={classes.membersList}><br /><br />
              {team.members.map((member, index) => (
                <li key={index}>
                  {member.name}{" | "}
                  {member.group !== "" ? member.group : member.dep}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
      {error && <div className={classes.error}>{error}</div>}
    </>
  );
};

export default ExistTeam;
