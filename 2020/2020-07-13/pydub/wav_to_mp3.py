from pydub import AudioSegment

sound_file = AudioSegment.from_wav("counting.wav")
sound_file.export("./out/counting.mp3",
                  format="mp3",
                  bitrate="192k",
                  tags={"album": "The Greatest Hits", "artist": "The Talker"})
