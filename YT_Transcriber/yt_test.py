from youtube_transcript_api._api import YouTubeTranscriptApi

print("Methods available:")
print(dir(YouTubeTranscriptApi))  # Look for 'get_transcript'

video_id = "Ks-_Mh1QhMc"
transcript = YouTubeTranscriptApi.get_transcript(video_id)
print("Transcript:")
print(transcript[:2])
