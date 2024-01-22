import { toast } from "react-toastify";

//success toast
export const ShowSuccessToastMessage = (str: string) => {
  toast.success(str, {
    position: toast.POSITION.TOP_RIGHT,
  });
};

//error toast
export const ShowErrorToastMessage = (name = "Произошла ошибка!") => {
  toast.error(name, {
    position: toast.POSITION.TOP_RIGHT,
  });
};

//warning toast
export const ShowWarningToastMessage = (name = "Внимание! Возможна ошибка") => {
  toast.warning(name, {
    position: toast.POSITION.TOP_RIGHT,
  });
};

//info toast
export const ShowInfoToastMessage = (str: string) => {
  toast.info(str, {
    position: toast.POSITION.TOP_RIGHT,
  });
};

//defult toats
export const ShowDefaultToastMessage = () => {
  toast("Default Notification!", {
    position: toast.POSITION.TOP_RIGHT,
  });
};

//custom toast
export const howCustomToastMessage = () => {
  toast("Custom Style Notification!", {
    position: toast.POSITION.TOP_RIGHT,
    className: "foo-bar",
  });
};
