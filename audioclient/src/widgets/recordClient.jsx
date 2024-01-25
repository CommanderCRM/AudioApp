import { useState, useEffect } from "react";
import { AudioRecorder } from "react-audio-voice-recorder";
import { IconButton, Button } from "@mui/material";
import MicIcon from "@mui/icons-material/Mic";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { useParams } from "react-router-dom";
import { client, doctor } from "..";

//dialog fucntion to record or load audio phrase for patient
export const RecorderVoiceItem = ({
  speechId,
  handleButtonNext,
  patientID,
}) => {
  const [phrases, setPhrases] = useState([]);
  const [index, setIndex] = useState(1);
  const [isMic, setisMic] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      const res = await client.getPhrases(speechId.session_id);
      const speechType =
        speechId.session_type === "фраз"
          ? speechId.session_type + "а"
          : speechId.session_type;

      setPhrases(speechType === "слоги" ? res.syllables : res.phrases);
    };

    fetchData();
    console.log(phrases);
  }, [patientID, speechId]);

  const handleIndex = () => {
    if (index + 1 > phrases.length) {
      handleButtonNext();
    }
    setIndex(index + 1);
    if (isMic) setisMic(!isMic);
  };

  const handleFile = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = function () {
        const base64 = reader.result.split(",")[1];
        const data = {
          speech_type:
            speechId.session_type === "фраз"
              ? speechId.session_type + "а"
              : speechId.session_type,
          base64_value: base64,
          base64_value_segment: "",
          real_value: phrases[index - 1],
        };
        client
          .saveAudio(
            speechId.sessionId,
            data.speech_type,
            data.base64_value,
            data.real_value
          )
          .then(() => {
            handleIndex();
          })
          .catch((error) =>
            console.error("Error updating session speech:", error)
          );
      };
    }
  };

  return (
    <>
      <div>
        {speechId.session_type[0].toUpperCase() +
          speechId.session_type.slice(1, speechId.session_type.length)}{" "}
        {index}/{phrases.length}: {phrases[index - 1]}
      </div>
      {isMic ? (
        <RecordVoice
          speechId={speechId}
          handleIndex={handleIndex}
          real_val={phrases[index - 1]}
        />
      ) : (
        <div className="flex flex-col items-center justify-center ">
          <div className="mt-4">
            <IconButton onClick={() => setisMic(!isMic)}>
              <MicIcon />
            </IconButton>
          </div>
          <div className="my-3">или</div>
          <Button
            component="label"
            variant="contained"
            startIcon={<CloudUploadIcon />}
          >
            Upload file
            <input
              type="file"
              onChange={(event) => handleFile(event)}
              accept=".webm"
              style={{ display: "none" }}
            />
          </Button>
        </div>
      )}
    </>
  );
};

//fucntion that records audio
const RecordVoice = ({ speechId, handleIndex, real_val }) => {
  const [audio, setAudio] = useState(null);
  const [showAudio, setShow] = useState(false);
  const handleNext = async () => {
    var reader = new window.FileReader();
    reader.readAsDataURL(audio);
    reader.onloadend = function () {
      const base64 = reader.result.split(",")[1];
      const data = {
        speech_type:
          speechId.session_type === "фразы"
            ? (speechId.session_type = "фраза")
            : speechId.session_type === "слоги"
            ? (speechId.session_type = "слог")
            : speechId.session_type,
        base64_value: base64,
        base64_value_segment: "",
        real_value: real_val,
      };

      client
        .saveAudio(
          speechId.sessionId,
          data.speech_type,
          data.base64_value,
          data.real_value
        )
        .then(() => {
          setShow(false);
          handleIndex();
        })
        .catch((error) =>
          console.error("Error updating session speech:", error)
        );
    };
  };
  const onStop = (audioData) => {
    setAudio(audioData);
    setShow(true);
  };
  return (
    <div>
      <div className="flex justify-center">
        {!showAudio ? (
          <AudioRecorder
            onRecordingComplete={onStop}
            audioTrackConstraints={{
              noiseSuppression: true,
              echoCancellation: true,
            }}
            downloadOnSavePress={true}
            downloadFileExtension="webm"
            showVisualizer
          />
        ) : (
          <ListenAudio
            audio={audio}
            handleNext={handleNext}
            setShow={setShow}
          />
        )}
      </div>
    </div>
  );
};

const ListenAudio = ({ audio, handleNext, setShow }) => {
  const url = URL.createObjectURL(audio);
  return (
    <div>
      <div className="flex-col align-center">
        <audio src={url} controls={true} />
        <div className="flex justify-between">
          <Button onClick={handleNext} variant="outlined" sx={{ mt: 2 }}>
            Продолжить
          </Button>
          <Button
            onClick={() => setShow(false)}
            variant="outlined"
            sx={{ mt: 2 }}
          >
            Перезаписать
          </Button>
        </div>
      </div>
    </div>
  );
};
