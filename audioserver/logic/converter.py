import base64
from pydub import AudioSegment
from io import BytesIO

def base64_to_wav(base64_string):
    # ?????????? base64 ?????? ? ???????? ??????
    audio_data = base64.b64decode(base64_string)

    # ??????? ?????? BytesIO ?? ???????? ??????
    audio_io = BytesIO(audio_data)

    # ????????? ??? ??????????
    magic_number = audio_io.read(4)
    audio_io.seek(0)  # ???????????? ? ?????? ?????

    if magic_number == b'RIFF':
        # ???? ???? ??? ? ??????? WAV, ?????? ?????????? ???
        return base64_string
    elif magic_number == b'\x1aE\xdf\xa3':
        # ???? ???? ? ??????? webm, ?????????? ?????????
        pass
    else:
        # ???????????????? ??????
        raise ValueError("Unsupported audio format")

    # ????????? ????? ? ??????? webm ? ?????????????? pydub
    audio = AudioSegment.from_file(audio_io, format="webm", codec="opus", parameters=["-ar", "16000"])

    # ??????????? ????? ? ?????? WAV
    wav_data = audio.raw_data
    wav_file = AudioSegment(
        wav_data,
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # ???????? ???????? ?????? WAV
    wav_binary_data = wav_file.export(format="wav").read()

    # ???????? ???????? ?????? WAV ? base64
    return base64.b64encode(wav_binary_data).decode('utf-8')