import axios from "axios";

//doctor's api
export const $api_doctor = axios.create({
  baseURL: process.env.REACT_APP_BASE_URL_DOCTOR,
  withCredentials: true,
});

//docror's interceptors

$api_doctor.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem("tok")}`;
  return config;
});

$api_doctor.interceptors.response.use(
  (config) => {
    return config;
  },
  async (error) => {
    const originalRequest = error.config;
    console.log("1234");
    console.log(error);
    console.log(!originalRequest._isRetry);
    if (error.message === "Network Error") {
      originalRequest._isRetry = true;
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_BASE_URL_DOCTOR}update_tokens`,
          { refresh: getCookie("tok") }
        );
        localStorage.setItem("tok", response.data.access_token);
        document.cookie = `tok=${response.data.refresh_token}; path=/;`;
        return $api_doctor.request(originalRequest);
      } catch (error: any) {
        // if (error.response.status === 500) {
        //   window.location.href = '/';
        // }
        window.location.href = '/';
      }
    } else {
      // localStorage.clear()
      // window.location.href = '/';
    }

    throw error;
  }
);

//get cookie function

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
  await $api_doctor
    .get(`${process.env.REACT_APP_BASE_URL_DOCTOR}/patients?limit=${limit}`)
    .then((r) => {
      if (r.status === 200) {
        return r.data;
      } else {
        console.log("Невозможно получить пациентов");
      }
    });
}
