import { useState, useEffect } from "react";
import DeleteButton from "../DeleteButton";
import Button from "../Button/Button";
import classes from "./Participants.module.css";

const ParticipantInputs = ({ onChange }) => {
  const [participants, setParticipants] = useState([{ id: 0, name: "" }]);
  const [groupValues, setGroupValues] = useState([""]);
  const [depValues, setDepValues] = useState([""]);
  
  const addFields = (e) => {
    e.preventDefault();
    const newParticipant = { id: participants.length, name: "" };
    const newGroupValues = [...groupValues, ""];
    const newDepValues = [...depValues, ""];
    const newParticipants = [...participants, newParticipant];

    setParticipants(newParticipants);
    setGroupValues(newGroupValues);
    setDepValues(newDepValues);
    onChange(newParticipants, newGroupValues, newDepValues);
  };

  const handleInputChange = (index, name, value) => {
    const newParticipants = [...participants];
    newParticipants[index][name] = value;
    setParticipants(newParticipants);
    onChange(newParticipants, groupValues, depValues);
  };

  const handleGroupChange = (index, value) => {
    const newGroupValues = [...groupValues];
    newGroupValues[index] = value;
    const newDepValues = depValues.map((dep, i) => (i === index ? "" : dep));
    const newParticipants = participants.map((participant, i) => {
      if (i === index) {
        return { ...participant, group: value };
      }
      return participant;
    });

    setParticipants(newParticipants);
    setGroupValues(newGroupValues);
    setDepValues(newDepValues);
    onChange(newParticipants, newGroupValues, newDepValues);
  };

  const handleDepChange = (index, value) => {
    const newDepValues = [...depValues];
    newDepValues[index] = value;
    const newGroupValues = groupValues.map((group, i) => (i === index ? "" : group));
    const newParticipants = participants.map((participant, i) => {
      if (i === index) {
        return { ...participant, department: value };
      }
      return participant;
    });

    setParticipants(newParticipants);
    setGroupValues(newGroupValues);
    setDepValues(newDepValues);
    onChange(newParticipants, newGroupValues, newDepValues);
  };

  const handleDelete = (e, id) => {
    e.preventDefault();
    const newParticipants = participants.filter((participant) => participant.id !== id);
    const newGroupValues = groupValues.filter((_, i) => i !== id);
    const newDepValues = depValues.filter((_, i) => i !== id);

    setParticipants(newParticipants);
    setGroupValues(newGroupValues);
    setDepValues(newDepValues);
    onChange(newParticipants, newGroupValues, newDepValues);
  };

  return (
    <div>
      <span className={classes.span}>Введите список участников</span> <br />
      {participants.map((participant, index) => (
        <div key={index}>
          <input
            placeholder="Фамилия Имя Отчество"
            className={classes.input}
            type="text"
            id={`fio_${index}`}
            value={participant.name || ""}
            onChange={(e) => handleInputChange(index, "name", e.target.value)}
          />
          <input
            placeholder="Группа"
            className={`${classes.input} ${
              depValues[index] !== "" ? classes.disabled : ""
            }`}
            type="text"
            id={`group_${index}`}
            value={groupValues[index]}
            onChange={(e) => handleGroupChange(index, e.target.value)}
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
          <DeleteButton onClick={(e) => handleDelete(e, participant.id)} />
        </div>
      ))}
      <Button text="Добавить участника" onClick={addFields} />
    </div>
  );
};

export default ParticipantInputs;
