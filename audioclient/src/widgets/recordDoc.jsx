import { useState, useEffect } from "react";
import { AudioRecorder, useAudioRecorder } from "react-audio-voice-recorder";
// import "react-audio-voice-recorder/dist/index.css";
import { IconButton, Button } from "@mui/material";
import MicIcon from "@mui/icons-material/Mic";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { useParams } from "react-router-dom";
import { doctor } from "..";

//dialog fucntion to record or load audio phrase for doctor
export const RecorderVoiceItem = ({
  speechId,
  handleButtonNext,
  phrasesold,
}) => {
  const { patientID } = useParams();
  const [phrases, setPhrases] = useState([]);
  const [index, setIndex] = useState(1);
  const [isMic, setisMic] = useState(false);
  const [audioData, setAudioData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await doctor.getExampleSpeech(patientID, speechId);
      const speechType =
        speechId.session_type === "фраз"
          ? speechId.session_type + "а"
          : speechId.session_type;
      if (phrasesold && phrasesold.length !== 0) {
        setPhrases(phrasesold);
      } else {
        setPhrases(speechType === "слог" ? res.syllables : res.phrases);
      }
    };

    fetchData();
  }, [speechId, handleButtonNext]);

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
        console.log(base64);
        const data = {
          speech_type:
            speechId.session_type === "фраз"
              ? speechId.session_type + "а"
              : speechId.session_type,
          base64_value: base64,
          base64_value_segment: "",
          real_value: phrases[index - 1],
        };
        doctor
          .updateSessionSpeech(speechId, data)
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
        Фраза {index}/{phrases?.length}: {phrases[index - 1]}
      </div>
      {isMic ? (
        <RecordVoice
          speechId={speechId}
          handleIndex={handleIndex}
          real_val={phrases[index - 1]}
          setAudioData={setAudioData}
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
const RecordVoice = ({ speechId, handleIndex, real_val, setAudioData }) => {
  const onStop = async (audioData) => {
    var reader = new window.FileReader();
    reader.readAsDataURL(audioData);
    reader.onloadend = function () {
      const base64 = reader.result.split(",")[1];
      const data = {
        speech_type:
          speechId.session_type === "фраз"
            ? speechId.session_type + "а"
            : speechId.session_type,
        base64_value: base64,
        base64_value_segment: "",
        real_value: real_val,
      };
      doctor
        .updateSessionSpeech(speechId, data)
        .then(() => {
          handleIndex();
        })
        .catch((error) =>
          console.error("Error updating session speech:", error)
        );
    };
  };

  return (
    <div>
      <div className="flex justify-center">
        <AudioRecorder
          onRecordingComplete={(blob) => onStop(blob)}
          audioTrackConstraints={{
            noiseSuppression: true,
            echoCancellation: true,
          }}
          downloadOnSavePress={true}
          downloadFileExtension="webm"
          showVisualizer
        />
      </div>
    </div>
  );
};

// const base64ToArrayBuffer = (base64) => {
//   const binaryString = window.atob(base64);
//   const len = binaryString.length;
//   const bytes = new Uint8Array(len);
//   for (let i = 0; i < len; i++) {
//     bytes[i] = binaryString.charCodeAt(i);
//   }
//   return bytes.buffer;
// };

// const arrayBufferToBase64 = (arrayBuffer) => {
//   const uint8Array = new Uint8Array(arrayBuffer);
//   const binaryString = uint8Array.reduce(
//     (acc, byte) => acc + String.fromCharCode(byte),
//     ""
//   );
//   return window.btoa(binaryString);
// };
