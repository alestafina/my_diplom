import Button from "../Button/Button";
import classes from "./Modal.module.css";

function Modal({ winName, additionalButtons }) {
  return (
    <div className={classes.modal}>
      <div className={classes.modalContent}>
        <p className={classes.title}>{winName}</p>
        {additionalButtons.map((button, index) => (
          <Button key={index} onClick={button.onClick} text={button.text} />
        ))}
      </div>
    </div>
  );
}

export default Modal;
