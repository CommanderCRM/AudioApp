import { LineChart } from "@mui/x-charts";
import { Dialog, DialogContent } from "@mui/material";

//function returns phrase chart
export const PhraseChart = ({ handleCloseChart, open, sessionsData }: any) => {
  // Filter sessions with valid data
  const validSessions = sessionsData.filter(
    (element: any) =>
      element.session_compares_history.length &&
      element.session_compares_history[0].compared_sessions_id &&
      element.session_compares_history[0].compared_sessions_id.length === 1
  );

  // Extract data for the chart
  const x_nums = validSessions.map((element: any) => element.session_id);
  const evals = validSessions.map(
    (element: any) =>
      element.session_compares_history[
        element.session_compares_history.length - 1
      ].session_score
  );

  return (
    <Dialog open={open} onClose={handleCloseChart} fullWidth>
      <DialogContent>
        {!evals.length ? (
          <span>Сеансы не оценёны, невозможно построить график!</span>
        ) : (
          <LineChart
            xAxis={[{ data: x_nums }]}
            series={[{ data: evals }]}
            width={500}
            height={300}
          />
        )}
      </DialogContent>
    </Dialog>
  );
};
