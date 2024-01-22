//convert time function
export const ConvertTime = (originalDate) => {
  const dateObject = new Date(originalDate);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
  };

  return new Intl.DateTimeFormat("ru-RU", options).format(dateObject);
};
