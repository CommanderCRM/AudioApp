import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";

export const DialogProcess = ({ open, handleClose, isSave }: any) => {
  return (
    <>
      <Dialog open={open} fullWidth>
        <DialogTitle>Обработка может занять некоторе время</DialogTitle>
        <DialogContent>Ожидайте активации кнопки активации</DialogContent>
        <DialogActions>
          <Button onClick={handleClose} variant="contained" disabled={isSave}>
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};
