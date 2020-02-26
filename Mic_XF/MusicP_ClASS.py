from PyQt5.Qt import *
from PyQt5.QtCore import QUrl
import sys
import os

'''
    本文件目前一个类 
    Mic_Media 类实现播放媒体生成，协助Main_CALSS类实现播放功能

'''

class Mic_Media(QWidget):
    def __init__(self,timer=None):
        super().__init__()
        # self.current_Music = ''  # 当前播放音乐
        # self.url = ''
        self.timer = timer  #定时器
        self.url_list = None
        # **********播放器设置***********
        self.player = QMediaPlayer()  # 生成播放媒体
        self.player.setVolume(30)  # 设置音量
        self.player_list = QMediaPlaylist(self) #生成播放列表
        # **********end***********
        #self.setMusicList()
        #self.player.setPlaylist(self.player_list)


    def setMusicList(self,urls):
        for url in urls:
            context = QMediaContent(QUrl.fromLocalFile(url))
            self.player_list.addMedia(context)
        self.player.setPlaylist(self.player_list)#播放器play设置播放列表


    def getMusicPath(self):
        pwd = os.getcwd()  # 获取当前文件路径
        music_pwd = pwd + '\music\\'  # 获取当前音乐文件夹路径
        return music_pwd

    def getMusicFiles(self):
        music_pwd = self.getMusicPath()
        files = os.listdir(music_pwd)  # 获取音乐文件夹下的音乐文件
        return files

    def changeMusic(self, music_name,index):
        #print(music_name,index)
        #获取歌曲名称，音乐列表双击歌曲的索引
        #把媒体列表 设置为当前索引指示的歌曲 并且播放
        print('change')
        self.player_list.setCurrentIndex(index)
        self.playMusic()

    def playMusic(self):
        self.timer.stop()
        self.timer.start(1000)
        self.player.play()

    def pauseMusic(self):
        self.player.pause()
        self.timer.stop()
    def stopMusic(self):

        self.timer.stop()
        self.player.stop()
        self.player.setPosition(0)
        #print('下一首歌曲'+str(self.player.position()) + 'ms')



def main():
    app = QApplication(sys.argv)
    gui = Mic_Media()
    gui.resize(500, 500)
    gui.move(500, 300)
    gui.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
