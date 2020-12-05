import pyautogui
from pynput import keyboard
import time
import sys
import threading
from TikTokApi import TikTokApi
import win32clipboard
import requests
import chat_reader

VIDEO_TIME = 0


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.f1:
        print("exiting")
        exit()


def main(api: TikTokApi):
    video_time = 0
    # Getting the video link twice, because for some reason the clipboard doesn't update properly if you only add
    # one thing to it. Once we copy the link twice, GetClipboardData() works as intended.
    get_link()
    time.sleep(0.3)
    get_link()
    time.sleep(0.3)
    toggle_pause()
    video_scene()
    _URL = copy_clipboard()
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }
    try:
        _new_URL = requests.get(_URL, headers=header)
        video_data = api.getTikTokByUrl(_new_URL.url)
        video_time = video_data['itemInfo']['itemStruct']['video']['duration']
        print(str(video_time)
              + "seconds  -  "
              + video_data['itemInfo']['itemStruct']['author']['uniqueId']
              + "   -   "
              + _URL
              + "   -   "
              + _new_URL.url)
        _new_URL = None
    except Exception:
        print("Could not connect to TikTok...: " + _URL)

    _URL = None
    # In case it couldn't connect, just use 20 seconds as default time.
    if video_time == 0:
        video_time = 20

    # Now watching the video, sleep so it just idles meanwhile.
    watch_video(video_time)
    next_video()


def watch_video(_time: int) -> None:
    """
    Handle all the events while watching a TikTok.
    Events include:
    - skipping
    - liking
    - none
    :param _time: The length of the TikTok video.
    :return: None
    """
    chat_reader.reset_chat()
    liked = False
    for i in range(0, _time - 1):
        time.sleep(1)
        # TODO: Make audience events percentage based or something
        if chat_reader.laughs > 2 and not liked:
            like_video()
            liked = True
        elif chat_reader.boring > 2:
            print("Skipping")
            break


def transition_scene() -> None:
    pyautogui.click(1350, 824)


def video_scene() -> None:
    # Sleeping here so we wait for share window to go away
    time.sleep(0.1)
    pyautogui.click(1350, 805)


def like_video() -> None:
    pyautogui.click(960, 600)
    pyautogui.click(960, 600)


def next_video() -> None:
    """User input to advance to the next TikTok video."""
    transition_scene()
    pyautogui.moveTo(960, 600)
    pyautogui.mouseDown()
    pyautogui.moveTo(960, 100, 0.2)
    pyautogui.mouseUp()
    toggle_pause()


def toggle_pause() -> None:
    pyautogui.click(960, 600)


def previous_video() -> None:
    """User input to go to the previous TikTok video."""
    pyautogui.moveTo(960, 100)
    pyautogui.mouseDown()
    pyautogui.moveTo(960, 600, 0.2)
    pyautogui.mouseUp()
    pyautogui.moveTo(960, 100)


def get_link() -> None:
    """Copies the link of the current TikTok video."""
    pyautogui.click(1184, 870)
    time.sleep(0.7)
    pyautogui.click(690, 845)


def copy_clipboard() -> str:
    """Returns the current text in the clipboard."""
    win32clipboard.OpenClipboard()
    _URL = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return _URL


def keyboard_listener():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    site_api = TikTokApi()
    pyautogui.FAILSAFE = True
    chat_thread = threading.Thread(target=chat_reader.main, args=())
    chat_thread.start()
    while True:
        main(site_api)
