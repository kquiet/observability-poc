// src/services/apiService.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/backend', // Replace with your API's base URL
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
  },
});

export default {
    callApi(id) {
        return apiClient.get(`/beats/${id}/`);
    },
};
