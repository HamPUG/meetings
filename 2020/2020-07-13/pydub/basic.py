from pydub import AudioSegment

sound_file = AudioSegment.from_wav("counting.wav")

print("--> info")
print("length in msec:", len(sound_file))
print("length in s:", sound_file.duration_seconds)
print("channels:", sound_file.channels)
print("frame_rate (Hz):", sound_file.frame_rate)
print("frame_width:", sound_file.frame_width)
print("max:", sound_file.max)
print("max DBFS:", sound_file.max_dBFS)

print("--> other")
print("converter:", sound_file.converter)
