import { useState } from "react";
import classes from "./BasicInfo.module.css";

function BasicInfo({ onChange }) {
  const [type, setType] = useState(null);
  const [theme, setTheme] = useState("");
  const [link, setLink] = useState("");
  const [place, setPlace] = useState("");

  const handleTypeChange = (typeIn) => {
    setType(typeIn);
    onChange({ type: typeIn, theme, meet: typeIn === "online" ? link : place });
  };

  const handleThemeChange = (e) => {
    setTheme(e.target.value);
    onChange({ type, theme: e.target.value, meet: type === "online" ? link : place });
  };

  const handleLinkChange = (e) => {
    setLink(e.target.value);
    onChange({ type, theme, meet: type === "online" ? e.target.value : place });
  };

  const handlePlaceChange = (e) => {
    setPlace(e.target.value);
    onChange({ type, theme, meet: type === "online" ? link : e.target.value });
  };

  return (
    <>
      <span className={classes.span}>Введите основные сведения</span>
      <p>Тип встречи</p>
      <label className={classes.label}>
        <input
          type="radio"
          checked={type === "online"}
          onChange={() => handleTypeChange("online")}
        />
        <span>Онлайн</span>
      </label>
      <label className={classes.label}>
        <input
          type="radio"
          checked={type === "offline"}
          onChange={() => handleTypeChange("offline")}
        />
        <span>Очная</span>
      </label>
      <p>Тема встречи</p>
      <input
        placeholder="Тема"
        type="text"
        id="theme"
        value={theme}
        onChange={handleThemeChange}
      />
      {type && (
        <>
          {type === "online" ? (
            <>
              <p>Ссылка на чат/звонок</p>
              <input
                placeholder="Ссылка"
                className={classes.input}
                type="text"
                value={link}
                onChange={handleLinkChange}
              />
            </>
          ) : (
            <>
              <p>Место встречи</p>
              <input
                placeholder="Корпус-аудитория"
                className={classes.input}
                type="text"
                value={place}
                onChange={handlePlaceChange}
              />
            </>
          )}
        </>
      )}
    </>
  );
}

export default BasicInfo;
