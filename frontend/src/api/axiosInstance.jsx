import axios from 'axios';

axios.defaults.withCredentials = true; // разрешение получать куки

const instance = axios.create({
  baseURL: 'http://localhost:5000', // привязываем сервер к фронту
});

export default instance;
