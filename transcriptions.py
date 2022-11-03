import os
import json
import time
import requests
from podcast import Podcast

def create_transcripts(podcast_list, **kwargs):
	all_transcription_metadata = {}
	for podcast in podcast_list:
		podcast_metadata = {}
		downloads = os.listdir(podcast.download_directory)
		for download in downloads:
			print("Uploading", download)
			file_path = f'{podcast.download_directory}/{download}'
			content_url = upload_to_assembly_ai(file_path)
			transcription_id = transcribe_podcast(content_url, **kwargs)
			podcast_metadata[download] = transcription_id

		all_transcription_metadata[podcast.name] = podcast_metadata.copy()

	return all_transcription_metadata

def upload_to_assembly_ai(file_path):
	headers = {'authorization': os.environ['ASSEMBLY_AI_KEY']}
	endpoint = 'https://api.assemblyai.com/v2/upload'
	response = requests.post(endpoint, headers=headers, data=read_file(file_path))
	upload_url = response.json()['upload_url']
	return upload_url

def transcribe_podcast(url, **kwargs):
	headers = {
	    "authorization": os.environ['ASSEMBLY_AI_KEY'],
	    "content-type": "application/json"
	}
	
	json = {'audio_url': url}
	for key, value in kwargs.items():
		json[key] = value
	
	endpoint = 'https://api.assemblyai.com/v2/transcript'
	response = requests.post(endpoint, headers=headers, json=json)
	transcription_id = response.json()['id']
	return transcription_id

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def save_transcription_metadata(metadata, file_path='./transcripts/metadata.json'):
	with open(file_path,'w') as f:
		json.dump(metadata, f)

def load_transcription_metadata(file_path='./transcripts/metadata.json'):
	with open(file_path) as json_file:
		metadata = json.load(json_file)

	return metadata

def save_transcriptions_locally(podcast_list):
	metadata = load_transcription_metadata()
	for podcast in podcast_list:
		podcast_transcriptions = metadata[podcast.name]
		for episode, transcription_id in podcast_transcriptions.items():
			episode_name = os.path.splitext(episode)[0]
			output_path = f'{podcast.transcription_directory}/{episode_name}.txt'
			print('Trying to save', output_path)
			transcription = wait_and_get_assembly_ai_transcript(transcription_id)
			with open(output_path, 'w') as f:
				f.write(transcription['text'])

def get_assembly_ai_transcript(transcription_id):
	headers = {'authorization': os.environ['ASSEMBLY_AI_KEY']}
	endpoint = f'https://api.assemblyai.com/v2/transcript/{transcription_id}'
	response = requests.get(endpoint, headers=headers)
	return response.json()

def wait_and_get_assembly_ai_transcript(transcription_id):
	while True:
		response = get_assembly_ai_transcript(transcription_id)
		if response['status'] == 'completed':
			print("Got transcript")
			break
		elif response['status'] == 'error':
			print("Error getting transcript")
			break
		else:
			print("Transcript not available, trying again in 5 minutes...")
			time.sleep(300) # Try again in 5 minutes

	return response

if __name__ == '__main__':
	print("\n--- Transcribing podcasts... ---\n")
	#podcast_list = [Podcast('tim-ferriss', 'https://rss.art19.com/tim-ferriss-show')]
	podcast_list = [Podcast('lex-fridman', 'https://lexfridman.com/feed/podcast/')]
	metadata = create_transcripts(podcast_list, audio_start_from=600000, audio_end_at=900000)
	print('Uploaded transcripts')
	save_transcription_metadata(metadata)
	save_transcriptions_locally(podcast_list)