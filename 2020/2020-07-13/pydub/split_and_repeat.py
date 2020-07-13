from pydub import AudioSegment
from pydub.silence import split_on_silence

sound_file = AudioSegment.from_wav("counting.wav")
audio_chunks = split_on_silence(sound_file, min_silence_len=250, silence_thresh=-32)

combined = None
for i, chunk in enumerate(audio_chunks):
    if combined is None:
        combined = chunk*2
    else:
        combined += chunk*2

combined.export("./out/repeated.wav", format="wav")
