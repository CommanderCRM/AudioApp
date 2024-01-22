import axios from "axios";

//clien's api
export const $api_client = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL_CLIENT,
  withCredentials: true,
});

//client's interceptors

$api_client.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem("ctok")}`;
  return config;
});

$api_client.interceptors.response.use(
  (config) => {
    return config;
  },
  async (error) => {
    const originalRequest = error.config;

    if (
      originalRequest &&
      !originalRequest._isRetry &&
      error.response.status === 500
    ) {
      originalRequest._isRetry = true;
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_BASE_URL_CLIENT}/update_tokens`,
          { refresh: getCookie("ctok") }
        );
        localStorage.setItem("ctok", response.data.access);
        return $api_client.request(originalRequest);
      } catch (error: any) {
        if (error.response.status === 500) {
        }
        // window.location.href = '/login'
      }
    } else {
      // localStorage.clear()
      // window.location.href = '/';
    }

    throw error;
  }
);

//get Cookie

export default function getCookie(name: string) {
  let matches = document.cookie.match(
    new RegExp(
      // eslint-disable-next-line no-useless-escape
      "(?:^|; )" +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

//get patients
export async function get_patients(limit: number) {
  await $api_client
    .get(`${process.env.REACT_APP_BASE_URL_DOCTOR}/patients?limit=${limit}`)
    .then((r) => {
      if (r.status === 200) {
        return r.data;
      } else {
        console.log("Невозможно получить пациентов");
      }
    });
}
