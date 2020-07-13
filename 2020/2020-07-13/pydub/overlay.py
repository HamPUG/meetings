from pydub import AudioSegment
from pydub.silence import split_on_silence

sound_file = AudioSegment.from_wav("counting.wav")
audio_chunks = split_on_silence(sound_file, min_silence_len=250, silence_thresh=-32)

overlayed = None
for i, chunk in enumerate(audio_chunks):
    if overlayed is None:
        overlayed = chunk
    else:
        overlayed = overlayed.overlay(chunk)

overlayed.export("./out/overlayed.wav", format="wav")
