from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pages.MainPage import MainScreen
from pages.HistoryPage import HistoryScreen
from pages.MediaPlayer.MediaRoutes import MediaRoutes
from Database.Script.Scrpit import executeDatabase 

class DownloaderApp(App):
    def build(self):
        executeDatabase()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='MainPage'))
        sm.add_widget(HistoryScreen(name='HistoryPage'))  
        MediaRoutes(sm)
        return sm

if __name__ == "__main__":
    DownloaderApp().run()
