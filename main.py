from youtube_transcript_api import YouTubeTranscriptApi

video_id = "a87Tb27UE4Y"

a = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])

print(a)
