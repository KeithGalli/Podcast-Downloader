# Programmatic Podcast Downloader & Transcriber
Ever feel like you spend as much time searching for podcasts as you do listening to them? Well put that in the past because this repo allows you to programmatically search through & download podcast episodes you'll find interesting with the simple click of button.

![Python program downloading & transcribing Lex Fridman podcasts. You see the name of each file as it is being downloaded/transcribed in a linux terminal](./resources/podcast_downloader.gif)

## Setup

To access all of the files I recommend you fork this repo and then clone it locally. Instructions on how to do this can be found here: https://help.github.com/en/github/getting-started-with-github/fork-a-repo

You will also need to make sure that you have all of the required Python libraries. You can do that by running a 
```pip install -r path/to/requirements.txt```

Now that you have the files & libraries locally, you will want to specify which Podcasts to run. Go into the [download_podcasts.py](https://github.com/KeithGalli/Podcast-Downloader/blob/master/download_podcasts.py) & [transcriptions.py](https://github.com/KeithGalli/Podcast-Downloader/blob/master/transcriptions.py) and edit the ```podcast_list``` located at the bottom of each file. 

You need to insert Podcast objects for each podcast that you want to programmatically scrape with Python. The first argument is the name of the podcast, the second argument is the URL for the podcast's RSS feed. If you don't know how to find this URL, I recommend checking out [this youtube video](https://youtu.be/UmGOeHEsSx8). You can add as many podcasts as you want.

Next you should set how many podcast episodes you want to download from each podcast by modifying the ```limit``` variable. You can also modify the search term to filter which types of episodes you download. In this example it is 'robot'. If you don't want a search term, uncomment the line that says get_items and comment the line that says search_items. See the image below for reference
![alt text](./resources/code_sample.png)

After you are done with these components, you can run the bash script 'run_all.sh' to download & transcribe your podcasts. Have fun!
