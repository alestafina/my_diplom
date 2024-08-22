import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import api from "../../api/axiosInstance";
import checkAuth from "../../api/checkAuth";
import ExistTeam from "../../components/ExistTeam/ExistTeam";
import Button from "../../components/Button/Button";
import DeleteModal from "../../components/Modal/DeleteModal";
import classes from "./MyTeamsPage.module.css";

function MyTeamsPage() {
  const [teams, setTeams] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [error, setError] = useState("");
  const [selectedTeam, setSelectedTeam] = useState({
    members: [""],
    title: "",
  });

  useEffect(() => {
    console.log(selectedTeam);
  }, [selectedTeam]);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const response = await api.get("/api/teams");
        setTeams(response.data);
      } catch (error) {
        setError("Ошибка при получении команд.");
      }
    };

    fetchTeams();
  }, []);

  const handleSelectTeam = (e, team) => {
    e.preventDefault();
    setSelectedTeam(team);
  };

  const handleDelete = async () => {
    try {
      await api.post("/api/teams/delete", { title: selectedTeam.title });
      setTeams((prevTeams) => prevTeams.filter((team) => team.title !== selectedTeam.title));
        setSelectedTeam({ members: [""], title: "" });
        setIsModalOpen(false);
    } catch (error) {
      setError("Ошибка при удалении команды.");
    }
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
      <section className={classes.page}>
        <div className={classes.title}>Мои команды</div>
        <ExistTeam onSelectTeam={handleSelectTeam} />
        <span
          className={`${classes.span} ${selectedTeam.title !== '' ? "" : classes.disabled}`}
        >
          <Button text="Удалить" onClick={openModal} />
        </span>
        {isModalOpen && (
          <DeleteModal
            message={`Вы уверены, что хотите удалить команду "${selectedTeam.title}"?`}
            onConfirm={handleDelete}
            onCancel={closeModal}
          />
        )}
      </section>
    );
  }
}
export default MyTeamsPage;
