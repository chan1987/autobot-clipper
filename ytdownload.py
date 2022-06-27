import os.path
import sys

from pytube import YouTube


def on_progress(stream, chunk, bytes_remaining):
    print("Downloading...")


def on_complete(stream, file_path):
    print("Download Complete")


youtubeurl = input("[+] Please enter youtube video url: ")
print(youtubeurl)

fileinputname = input("[+] Please enter video filename: ")
pwd = os.path.dirname(os.path.abspath(__file__))
filename = pwd + "/clips/" + fileinputname + ".mp4"
print(filename)

yt = YouTube(
    youtubeurl,
    on_progress_callback=on_progress,
    on_complete_callback=on_complete,
    use_oauth=False,
    allow_oauth_cache=True
)

if not os.path.isdir("clips"):
    os.mkdir("clips")

yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
    output_path="clips/", filename=filename)

# video = yt.streams.filter(res="1080p").first().download(output_path="clips/", filename='new_filename.mp4')

# Check if the download is successful
if os.path.isfile(filename):
    print("[*] Downloaded clip succesfully! - %s" % filename)
else:
    print("[!] Download failed!")
    sys.exit(0)


