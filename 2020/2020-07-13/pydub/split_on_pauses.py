from pydub import AudioSegment
from pydub.silence import split_on_silence

sound_file = AudioSegment.from_wav("counting.wav")
audio_chunks = split_on_silence(sound_file, min_silence_len=250, silence_thresh=-32)

print(len(audio_chunks), "chunk(s)")
for i, chunk in enumerate(audio_chunks):
    out_file = "./out/counting-{0}.wav".format(i)
    chunk.export(out_file, format="wav")
