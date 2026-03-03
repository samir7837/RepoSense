import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const authApi = {
  loginUrl: "http://localhost:8000/api/auth/github/login",
};

export const dashboardApi = {
  getRepos: (githubId: string) => api.get(`/dashboard/repos/${githubId}`),
  getReviews: (githubId: string) => api.get(`/dashboard/reviews/${githubId}`),
};

export default api;
