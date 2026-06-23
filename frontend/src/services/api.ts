import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_URL = `${BASE_URL.replace(/\/$/, '')}/api`;

export const getDashboardSummary = async () => {
  try {
    const response = await axios.get(`${API_URL}/dashboard/summary`);
    return response.data;
  } catch (error) {
    console.error('Error fetching dashboard summary:', error);
    throw error;
  }
};

export const getCustomers = async (skip = 0, limit = 50) => {
  try {
    const response = await axios.get(`${API_URL}/customers?skip=${skip}&limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching customers:', error);
    throw error;
  }
};
