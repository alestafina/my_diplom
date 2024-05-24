import { useState } from "react";
import classes from "./TimeTable.module.css";

function TimeTable({ dOfWeek, dMDate, schedule, onChange, styles }) {
  const [activeButton, setActiveButton] = useState({ date: "", time: "" });
  const timeForLessons = [
    "08:30 - 10:00",
    "10:15 - 11:45",
    "12:00 - 13:30",
    "14:00 - 15:30",
    "15:45 - 17:15",
    "17:30 - 19:00",
    "19:15 - 20:45",
  ];

  const handleDateTime = (e, _time, _date) => {
    e.preventDefault();
    setActiveButton({ date: _date, time: _time });
    onChange({ date: _date, time: _time });
  };

  return (
    <table className={classes.table}>
      <thead>
        <tr>
          <th className={classes.t}></th>
          {dOfWeek.map((day, index) => (
            <th key={index} className={classes.t}>
              {day}
              <br />
              {dMDate[index]}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {timeForLessons.map((time, i) => (
          <tr key={i}>
            <td className={classes.t}>{time}</td>
            {dMDate.map((date, dayIndex) => {
              const dayKey = "day " + (dayIndex + 1);
              const lessonKey = "lesson " + (i + 1);
              const lesson =
                schedule.days[dayIndex] &&
                schedule.days[dayIndex][dayKey] &&
                schedule.days[dayIndex][dayKey][lessonKey];

              const isLessonActive =
                lesson && (lesson === 1 || lesson.status === 1);

              const isButtonActive =
                activeButton.date === date && activeButton.time === time;

              return (
                <td
                  key={dayIndex}
                  style={{
                    backgroundColor: isLessonActive
                      ? styles.lessonActive
                      : styles.lessonInactive,
                  }}
                  className={classes.t}
                >
                  {isLessonActive ? (
                    <button
                      className={`${classes.button} ${
                        isButtonActive ? classes.active : ""
                      }`}
                      onClick={(e) => handleDateTime(e, time, date)}
                      style={{
                        backgroundColor: isButtonActive
                          ? styles.activeButtonColor
                          : '',
                      }}
                    ></button>
                  ) : (
                    ""
                  )}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TimeTable;
