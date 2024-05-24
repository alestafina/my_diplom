import React from "react";

function DeleteButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        borderRadius: "15px",
        backgroundColor: "rgb(200, 40, 40)",
        fontSize: "14px",
        fontWeight: "450",
      }}
    >
      Удалить
    </button>
  );
}

export default DeleteButton;
