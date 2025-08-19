import axios from 'axios';
import NProgress from 'nprogress';
import router from './../router';
import 'nprogress/nprogress.css';

// set base URL
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

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
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
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
    if (response.config.url?.includes('/api/token/') ||
      response.config.url?.includes('/api/user/me/')) {
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
  async (error) => {
    stopProgress()

    // Check for suspended status in error response
    if (error.response?.status === 403 &&
      error.response?.data?.error?.includes('suspended') &&
      (error.config.url?.includes('/api/token/') ||
        error.config.url?.includes('/api/user/me/'))) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      router.push('/auth/login?error=suspended')
    }

    // Handle 401 errors with token refresh logic
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      // Prevent infinite loop
      if (refreshToken && !error.config._retry) {
        error.config._retry = true;
        try {
          const refreshResponse = await axios.post('/api/token/refresh/', { refresh: refreshToken });
          const newAccessToken = refreshResponse.data.access;
          localStorage.setItem('access_token', newAccessToken);
          axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
          error.config.headers['Authorization'] = `Bearer ${newAccessToken}`;
          // Retry the original request
          return axios(error.config);
        } catch (refreshError) {
          // Fix: assert refreshError as AxiosError
          const axiosError = refreshError as import('axios').AxiosError;
          const refreshErrorData = axiosError.response?.data;
          const hasCode = typeof refreshErrorData === 'object' && refreshErrorData !== null && 'code' in refreshErrorData;
          const hasDetail = typeof refreshErrorData === 'object' && refreshErrorData !== null && 'detail' in refreshErrorData;
          if (
            axiosError.response?.status === 401 ||
            (hasCode && (refreshErrorData as any).code === 'token_not_valid') ||
            (hasDetail && (refreshErrorData as any).detail === 'Token is expired')
          ) {
            // Refresh token is invalid/expired, log out
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            router.push('/auth/login');
            return Promise.reject(axiosError);
          }
          // Other refresh error, log out as fallback
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          router.push('/auth/login');
          return Promise.reject(axiosError);
        }
      } else {
        // No refresh token or already retried, log out
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        router.push('/auth/login');
      }
    }

    return Promise.reject(error)
  }
);

export default axios; 