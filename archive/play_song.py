
""" A script to play a song while the script main.py is running"""
import os
import threading
from playsound import playsound

def play_song():
    '''Play a song while the script is running'''
    global song_thread
    song = 'archive/song.mp3'
    if os.path.exists(song):
        song_thread = threading.Thread(target=playsound, args=(song,))
        song_thread.start()
    else:
        print("File not found")

def stop_song():
    '''Stop the song'''
    global song_thread
    if song_thread and song_thread.is_alive():
        song_thread._delete()

if __name__ == '__main__':
    play_song()