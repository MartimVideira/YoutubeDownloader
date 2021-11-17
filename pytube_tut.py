from pytube import YouTube


yt = YouTube(
    'https://www.youtube.com/watch?v=fPO76Jlnz6c')

print(yt.title)
print(yt.views)
print(yt.rating)




audio_stream =yt.streams.get_audio_only