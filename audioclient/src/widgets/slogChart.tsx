import { LineChart } from "@mui/x-charts";
import { Dialog, DialogContent } from "@mui/material";

//fucntion return's syllables chart
export const SlogChart = ({ handleCloseChart, open, sessionsData }: any) => {
  console.log(sessionsData);
  const validSessions = sessionsData.filter(
    (session: any) =>
      session.session_compares_history.length > 0 &&
      session.session_compares_history[
        session.session_compares_history.length - 1
      ].compared_sessions_id.length > 1
  );

  // Extract data for the chart
  const evals = validSessions.map(
    (element: any) =>
      element.session_compares_history[
        element.session_compares_history.length - 1
      ].session_score
  );

  //Labels for chart
  const labels = validSessions.map((element: any) =>
    element.session_compares_history[
      element.session_compares_history.length - 1
    ].compared_sessions_id.join("/")
  );

  return (
    <Dialog open={open} onClose={handleCloseChart} fullWidth>
      <DialogContent>
        {!evals.length ? (
          <span>Сеансы не оценёны, невозможно построить график!</span>
        ) : (
          <LineChart
            xAxis={[{ scaleType: "point", data: labels }]}
            series={[
              {
                data: evals,
              },
            ]}
            width={500}
            height={300}
          />
        )}
      </DialogContent>
    </Dialog>
  );
};
