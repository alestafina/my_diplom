import Button from "../Button/Button";
import classes from "./Modal.module.css";

function Modal({ additionalButtons }) {
  return (
    <div className={classes.modal}>
      <div className={classes.modalContent}>
        {additionalButtons.map((button, index) => (
          <Button key={index} onClick={button.onClick} text={button.text} />
        ))}
      </div>
    </div>
  );
}

export default Modal;
