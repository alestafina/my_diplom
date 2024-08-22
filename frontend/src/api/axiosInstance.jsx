import axios from 'axios';

axios.defaults.withCredentials = true; // разрешение получать куки

const instance = axios.create({
  baseURL: 'http://217.71.129.139:4087', // привязываем сервер к фронту
});

export default instance;
