from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl


def play_music():
    music_file = QUrl.fromLocalFile("C:/Users/sanad/planner/background music.wav")
    player = QMediaPlayer()
    playlist = QMediaPlaylist(player)
    playlist.addMedia(QMediaContent(music_file))
    playlist.setPlaybackMode(QMediaPlaylist.Loop)
    player.setPlaylist(playlist)

    return player
