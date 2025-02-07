import axios from 'axios';
import NProgress from 'nprogress';
import router from './../router';
import 'nprogress/nprogress.css';

// set base URL
axios.defaults.baseURL = process.env.VUE_APP_API_URL

NProgress.configure({ showSpinner: true, trickleSpeed: 200 });

let activeRequests = 0;

const startProgress = () => {
  activeRequests++;
  if (activeRequests === 1) {
    NProgress.start();
  }
};

const stopProgress = () => {
  activeRequests--;
  if (activeRequests <= 0) {
    activeRequests = 0;
    NProgress.done();
  }
};

axios.interceptors.request.use(
  (config) => {
    startProgress();
    return config;
  },
  (error) => {
    stopProgress();
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    stopProgress();
    return response;
  },
  (error) => {
    stopProgress();

    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/auth/login')
    }

    return Promise.reject(error);
  }
);

export default axios; 