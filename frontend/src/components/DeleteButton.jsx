import React from "react";

function DeleteButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        // marginTop: "10px",
        // marginBottom: "0",
        // backgroundSize: "10px 10px",
        // paddingLeft: "8px",
        // paddingRight: "10px",
        // paddingBottom: "5px",
        borderRadius: "15px",
        backgroundColor: "rgb(200, 40, 40)",
        fontSize: "14px",
        fontWeight: "450"
      }}
    >
      Удалить
      {/* <img src="../../delete.png" width="25px" height="25px" /> */}
    </button>
  );
}

export default DeleteButton;
