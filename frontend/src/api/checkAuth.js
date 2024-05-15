import { useState } from "react";
import { useEffect } from "react";
import api from "./axiosInstance";

function checkAuth() {
  const [auth, setAuth] = useState(true);

  useEffect(() => {
    isAuth();
  }, []);

  const isAuth = async () => {
    try {
      const response = await api.get("/checkAuth");
      setAuth(response.data.isAuth);
    } catch (error) {
      console.error(error);
    }
  };
  return auth;
}

export default checkAuth;
