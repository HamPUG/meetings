from pydub import AudioSegment

sound_file = AudioSegment.from_wav("counting.wav")
sound_file = sound_file.reverse()
sound_file.export("./out/counting-reverse.wav")
