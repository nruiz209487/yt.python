from kivy.uix.screenmanager import ScreenManager
from pages.MediaPlayer.Video.VideoPlayerPage import VideoPlayerScreen
from pages.MediaPlayer.Music.MusicReproductorPage import MusicReproductorScreen
from pages.MediaPlayer.Gallery.GalleryPage import GalleryScreen
from pages.MediaPlayer.Gallery.ImagePage import ImageScreen
from pages.MediaPlayer.Video.VideoPage import VideoPageScreen
from pages.MediaPlayer.Music.MusicPage import MusicPageScreen

def MediaRoutes(sm: ScreenManager):
    sm.add_widget(VideoPlayerScreen(name='VideoPlayerPage'))
    sm.add_widget(MusicReproductorScreen(name='MusicReproductorPage'))
    sm.add_widget(GalleryScreen(name='GalleryPage'))
    sm.add_widget(ImageScreen(name='ImagePage'))
    sm.add_widget(VideoPageScreen(name='VideoPage'))
    sm.add_widget(MusicPageScreen(name='MusicPage'))