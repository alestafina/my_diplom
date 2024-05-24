import React from "react";
import classes from "./DeleteModal.module.css";
import Button from "../Button/Button";

const ConfirmationModal = ({ message, onConfirm, onCancel }) => {
  return (
    <div className={classes.modal}>
      <div className={classes.modalContent}>
        <p>{message}</p>
        <div className={classes.buttons}>
          <span className={classes.confirmButton}><Button onClick={onConfirm} text="Да" /></span>
          <span className={classes.cancelButton}><Button onClick={onCancel} text="Отмена" /></span>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;
