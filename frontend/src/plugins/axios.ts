import axios from 'axios';
import NProgress from 'nprogress';
import router from './../router';
import 'nprogress/nprogress.css';

// set base URL
axios.defaults.baseURL = process.env.VUE_APP_API_URL

NProgress.configure({ showSpinner: false, trickleSpeed: 200 });

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
    // Only check for suspension on auth-related endpoints
    if (response.config.url?.includes('/token/') ||
      response.config.url?.includes('/user/me/')) {
      if (response.data?.user?.status === 'Suspended') {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        router.push('/auth/login?error=suspended')
        return Promise.reject(new Error('Account suspended'))
      }
    }
    stopProgress()
    return response
  },
  (error) => {
    stopProgress()

    // Check for suspended status in error response
    if (error.response?.status === 403 &&
      error.response?.data?.error?.includes('suspended') &&
      (error.config.url?.includes('/token/') ||
        error.config.url?.includes('/user/me/'))) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/auth/login?error=suspended')
    }

    // Handle other 401 errors
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/auth/login')
    }

    return Promise.reject(error)
  }
);

export default axios; 