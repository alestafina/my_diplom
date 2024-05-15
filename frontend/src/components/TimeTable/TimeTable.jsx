import { useState } from "react";
import classes from "./TimeTable.module.css";

function TimeTable({ dOfWeek, dMDate, schedule, onChange }) {
  const [activeButton, setActiveButton] = useState({ date: "", time: "" });
  const timeForLessons = ["08:30 - 10:00", "10:15 - 11:45", "12:00 - 13:30", "14:00 - 15:30", "15:45 - 17:15", "17:30 - 19:00", "19:15 - 20:45"]
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
            {Array.from({ length: 12 }, (_, j) => j + 1).map((dayIndex) => (
              <td
                key={dayIndex}
                style={{
                  backgroundColor:
                    schedule.days[dayIndex - 1]["day " + dayIndex][
                      "lesson " + (i + 1)
                    ] === 1
                      ? "rgb(152, 251, 152)"
                      : "rgb(255, 182, 193)",
                }}
                className={classes.t}
              >
                {schedule.days[dayIndex - 1]["day " + dayIndex][
                  "lesson " + (i + 1)
                ] === 1 ? (
                  <button
                    className={`${classes.button} ${
                      activeButton.date === dMDate[dayIndex - 1] &&
                      activeButton.time === time
                        ? classes.active
                        : ""
                    }`}
                    onClick={(e) =>
                      handleDateTime(e, time, dMDate[dayIndex - 1])
                    }
                  ></button>
                ) : (
                  ""
                )}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default TimeTable;
