'''
HOW TO: Download YouTube Videos Programmatically with Python & pytube

$ pip install pytube

$ python3 download.py
'''
import videotrim_util
import ytupload_util
from pytube import YouTube
import os.path
import sys

default_description = "comedy_clip_dialogues"
default_categoryId = "23"


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

yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="clips/", filename=filename)

# video = yt.streams.filter(res="1080p").first().download(output_path="clips/", filename='new_filename.mp4')

# Check if the download is successful
if os.path.isfile(filename):
    print("[*] Downloaded clip succesfully! - %s" % filename)
else:
    print("[!] Download failed!")
    sys.exit(0)

print("[*] Opening clip in video player..")
os.startfile(filename)

op = input("[+] Do you want to trim the video? (Y/n): ")
if (op in ["Y", "y", ""]):
    # Open video trimming util
    if (videotrim_util.trimVideo(filename)):
        print("[*] Video trimmed successfully!")
        filename = filename.split(".ts")[0] + "_trimmed.ts"
    else:
        print("[!] Video trim failed!")
        op = input("Do you want to (E)xit or (C)ontinue?")
        if op in ["E", "e", ""]:
            sys.exit()

elif op in ["N", "n"]:
    # Do not open video trimming util
    pass

op = input("[+] Upload to YouTube? (Y/n): ")

if op in ["Y", "y", ""]:
    # Upload created clip to YT

    yt_title = input("[+] Video Title: ")
    yt_description = input("[+] Video Description (leave empty for default description): ")
    yt_tags = input("[+] Video Tags (seperated by comas): ")
    yt_categoryId = input("[+] Category ID (Leave empty for Comedy): ")
    yt_privacyStatus = input("[+] Privacy Status (public/private/unlisted): ")
    yt_credits = input("[+] Credits for Original Creator: ")

    if yt_title == "":
        print("[!] Title can't be empty")

    if yt_privacyStatus.lower() not in ["public", "private", "unlisted"]:
        print("[!] Invalid privacy status")

    if yt_description == "":
        yt_description = default_description

    if yt_categoryId == "":
        yt_categoryId = default_categoryId

    yt_description += "\n" + "Credits: \n" + yt_credits

    print("[*] Uploading video to YouTube. This might take a while..be patient, do not close the script.")
    videoId = ytupload_util.upload(filename, yt_title, yt_description, yt_tags, yt_categoryId, yt_privacyStatus)

    if videoId is not None:
        print("[*] Succesfully uploaded video. ")
        print("[*] https://www.youtube.com/watch?v=%s" % videoId)

    else:
        print("[!] Video upload failed.")
