from PyQt5.Qt import *
from MusicP_ClASS import *
from BenDi_CLASS import *
import sys
from PyQt5.QtCore import Qt

'''
    本文件目前两个类 
    MainUi 类实现UI界面和播放功能
    headerWidget 类实现鼠标事件重写
    
'''
class MainUi(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1024, 670)
        self.move(450, 185)
        #self.setFixedSize(self.width(), self.height(#222225));  # 固定窗口大小
        # self.setStyleSheet('background-color:#232326;')
        self.setWindowFlags(Qt.FramelessWindowHint)    #隐藏标题栏
        self.setWindowIcon(QIcon(r'resource\format.ico'))
        self.setObjectName('FatherWindow')
        #**********定时器设置***********
        # 初始化一个定时器， 用于定时更新当前媒体歌曲播放进度
        self.timer = QTimer()
        self.timer.stop() #定时器先关闭
        # 定时器开启后 会按设定时间，触发下面信号
        self.timer.timeout.connect(self.time_slot) #设置信号与槽

        #初始化一个播放媒体 并传递定时器 来管理
        self._first_meida = Mic_Media(self.timer)
        self.changeFlag = False #如果双击切歌为False 切歌键切歌为True
        self.Pre_Mic_Index = 0 #记录上一首播放歌曲的索引值 用来控制显示列表高亮



        with open('styleByQss\style.qss','r') as f:
            qApp.setStyleSheet(f.read())

        self.set_button() #初始化按钮
        self.set_label()    #初始化标签
        self.set_Frame()    #初始化分割线
        self.set_Slider()   #初始化滑条
        self.set_LineEdit()   #初始化搜索栏
        self.set_head_Layout()      #初始化顶部布局
        self.set_bottom_layout()    #初始化底部布局

        self.set_left_list()        ##初始化左边列表
        self.set_left_layout()      #初始化左边布局 左边列表在布局之中

        self.set_right_layout()     #初始化右边布局
        self._first_meida.setMusicList(self.right_Widget.getMusicUrls())
        self.set_slot()             #设置信号和槽的链接
        self.set_right_Change()


    def set_button(self):

        #btn_close btn_min 在被创建时候没有声明父类，因为要加入布局
        #加入布局后，布局就是其父类
        self.btn_close = QPushButton('×')
        self.btn_close.setObjectName('btn_close')
        self.btn_close.resize(50,30)

        self.btn_min = QPushButton('-')
        self.btn_min.setObjectName("btn_min")
        self.btn_min.resize(30,30)

        self.btn_last = QPushButton()
        self.btn_last.setObjectName('btn_last')
        self.btn_last.resize(30,30)
        self.btn_last.setMinimumSize(36, 36)

        self.btn_play = QPushButton()
        self.btn_play.setObjectName('btn_play')
        self.btn_play.setMinimumSize(36, 36)

        self.btn_next = QPushButton()
        self.btn_next.setObjectName('btn_next')
        self.btn_next.setMinimumSize(36, 36)


        #静音按钮 现在还没写
        self.btn_volume = QPushButton()
        self.btn_volume.setObjectName('btn_volume')
        self.btn_volume.setMinimumSize(25, 25)
    def set_label(self):
        #logoLabel music_text_label 在被创建时候没有声明父类，因为要加入布局
        #加入布局后，布局就是其父类
        self.logoLabel = QLabel()
        # self.logoLabel.move(2,5)
        self.logoLabel.resize(33,33)
        self.logoLabel.setText("<img src='resource\\format_meitu_1.png'>")#设置背景图片
        #self.logoLabel.setText("<img src='resource\\format_meitu_1.png' wigth = 60>")
        #self.logoLabel.setScaledContents(True) 设置图片自适应label大小 但好像不太管用

        self.music_text_label = QLabel()
        self.music_text_label.setObjectName("music_text_label")
        self.music_text_label.setText(" XLF-Music")
        self.music_text_label.resize(80,30)

        self.now_time_label = QLabel()
        self.now_time_label.setObjectName("time_label")
        self.now_time_label.setText("00:00")
        self.now_time_label.adjustSize()

        self.all_time_label = QLabel()
        self.all_time_label.setObjectName("time_label")
        self.all_time_label.setText("00:00")
        self.all_time_label.adjustSize()

        self.all_time_label = QLabel()
        self.all_time_label.setObjectName("time_label")
        self.all_time_label.setText("00:00")
        self.all_time_label.adjustSize()

        self.recommendLabel = QLabel(" 推荐")
        self.recommendLabel.setObjectName("recommendLabel")
        self.recommendLabel.setMaximumHeight(27)

        self.myMusicLabel = QLabel(" 我的音乐")
        self.myMusicLabel.setObjectName("myMusicLabel")
        self.myMusicLabel.setMaximumHeight(27)
        # self.myMusic.setMaximumHeight(54)

        self.singsListLabel = QLabel(" 收藏与创建的歌单")
        self.singsListLabel.setObjectName("singsListLabel")
        self.singsListLabel.setMaximumHeight(27)

        self.loc_File_label = QLabel("本地音乐")
        self.loc_File_label.setObjectName("loc_File_label")

        self.loc_File_label.setContentsMargins(20,18,0,0)
    def set_LineEdit(self):
        self.action = QAction()#声明一个动作行为，再把这个行为附着到控件 #这样可以让每个控件都有类似按钮的功能
        self.action.setIcon(QIcon(r'resource\search_hover.png'))
        # 当点击时候进行信号触发
        #self.action.triggered.connect(self.Check)

        self.lineEdit = QLineEdit()
        self.lineEdit.resize(220,30)
        self.lineEdit.setPlaceholderText("搜索音乐，歌手")
        self.lineEdit.setTextMargins(8,0,10,0) #设置光标焦点位置
        self.lineEdit.setObjectName('LineEdit')

        #为编辑框添加动作行为，第二个参数：把这个行为放在 Trail末尾 的位置
        self.lineEdit.addAction(self.action, QLineEdit.TrailingPosition)

        #当按下回车键时候 触发
        #self.lineEdit.returnPressed.connect(self.cao)
        #当有文字输入的时候触发，但setText()不会触发 #若想让setText()也触发，可使用textChange信号
        #self.lineEdit.textEdited.connect(self.cao2)
    def set_Slider(self):
        self.time_slider = QSlider()
        self.time_slider.setOrientation(Qt.Horizontal)
        self.time_slider.setMinimumHeight(5)
        self.time_slider.setMinimumWidth(440)
        # 将范围设置成1000滚动时更舒服。
        self.time_slider.setRange(0, 1000)
        self.time_slider.setObjectName("time_slider")


        self.volumeSlider = QSlider()
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setValue(self._first_meida.player.volume())
        self.volumeSlider.setMinimumHeight(5)
        self.volumeSlider.setObjectName("volumeSlider")
    def set_Frame(self):
        self.header_line = QFrame(self)
        self.header_line.setObjectName("header_line")
        self.header_line.setFrameShape(QFrame.HLine)#设置样式 有盒子 有水平线 有垂线
        self.header_line.setFrameShadow(QFrame.Plain)#设置线的样式，是实线 还是填充线
        #self.header_line.setMaximumSize(1, 25)
        self.header_line.resize(1024,10)
        self.header_line.move(0,47)
        self.header_line.setLineWidth(3)#设置线的宽度

        self.left_line = QFrame(self)
        self.left_line.setObjectName("left_line")
        self.left_line.setFrameShape(QFrame.VLine)#设置样式 有盒子 有水平线 有垂线
        self.left_line.setFrameShadow(QFrame.Plain)#设置线的样式，是实线 还是填充线
        #self.header_line.setMaximumSize(1, 25)
        self.left_line.resize(3, 580)
        self.left_line.move(201,55)
        self.left_line.setLineWidth(2)#设置线的宽度
        self.left_line.setStyleSheet('color:#2D2F32;')

        self.right_line = QFrame()
        self.right_line.setObjectName("right_line")
        self.right_line.setFrameShape(QFrame.HLine)#设置样式 有盒子 有水平线 有垂线
        self.right_line.setFrameShadow(QFrame.Plain)#设置线的样式，是实线 还是填充线
        self.right_line.setLineWidth(1)#设置线的宽度
        self.right_line.setStyleSheet('color:#2D2F32;')
    def set_left_list(self):
        self.left_header_List = QListWidget()
        self.left_header_List.setMaximumHeight(110)
        self.left_header_List.setObjectName("left_header_List")
        self.left_header_List.addItem(QListWidgetItem(QIcon('resource/music.png'), " 发现音乐"))
        self.left_header_List.addItem(QListWidgetItem(QIcon('resource/signal.png'), " 私人FM"))
        self.left_header_List.addItem(QListWidgetItem(QIcon('resource/movie.png'), " MV"))

        self.left_header_List.setCurrentRow(0)

        self.left_mid_List = QListWidget()
        self.left_mid_List.setObjectName("left_mid_List")
        self.left_mid_List.setMaximumHeight(100)
        self.left_mid_List.addItem(QListWidgetItem(QIcon('resource/notes.png')," 本地音乐"))
        self.left_mid_List.addItem(QListWidgetItem(QIcon('resource/download_icon.png'), " 我的下载"))
        self.left_mid_List.addItem(QListWidgetItem(QIcon('resource/recommend_icon.png'), " 专属推荐"))
        self.left_mid_List.setCurrentRow(0)
    def set_right_Change(self):
        self.w1 = QWidget(self)
        self.w1.resize(820, 555)
        self.w1.move(204,55)
        label = QLabel(self.w1)
        label.setText('别点了，我还没写完这项功能呢！！')
        label.setStyleSheet('color:white;font-size:25px;')
        self.w1.hide()
    def set_head_Layout(self):
        #在此创建header_widget2 因为布局之际就撑满主窗口 无法修改大小
        #所以创建子窗口且作为布局的父类。 这样可以修改子窗口的大小位置 来控制布局的大小位置
        self.header_widget = headerWidget(self)
        self.header_widget.resize(1024, 50)
        self.header_widget.setObjectName('header_widget2')

        #在此无法这是背景颜色 待解决问题一
        #self.header_widget.setStyleSheet('background-color:#232326')
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.addWidget(self.logoLabel,1)#参数：添加的空间，所占的比例
        header_layout.addWidget(self.music_text_label,3)#这个比例就是上面的三倍
        header_layout.addSpacing(10)
        header_layout.addWidget(self.lineEdit,8)
        header_layout.addStretch(20)#增加一个弹簧填补空间，参数是所占的比例
        header_layout.addWidget(self.btn_min,1)
        header_layout.addWidget(self.btn_close,1)
    def set_bottom_layout(self):
        self.bottom_widget = QWidget(self)
        self.bottom_widget.resize(1024, 60)
        self.bottom_widget.move(0,610)

        self.bottom_widget.setStyleSheet('background-color:#222225')

        bottom_layout = QHBoxLayout(self.bottom_widget)

        bottom_layout.setContentsMargins(15,15,0,10) #设置内容的内边距 左 上 右 下
        bottom_layout.addWidget(self.btn_last, 1)
        bottom_layout.addSpacing(10)
        bottom_layout.addWidget(self.btn_play,1)
        bottom_layout.addSpacing(10)
        bottom_layout.addWidget(self.btn_next, 1)
        bottom_layout.addSpacing(12)  # 增加空白间距
        bottom_layout.addWidget(self.now_time_label)
        bottom_layout.addSpacing(6)  # 增加空白间距
        bottom_layout.addWidget(self.time_slider,1)
        bottom_layout.addSpacing(6)  # 增加空白间距
        bottom_layout.addWidget(self.all_time_label)
        bottom_layout.addSpacing(10)  # 增加空白间距
        bottom_layout.addWidget(self.btn_volume)
        bottom_layout.addWidget(self.volumeSlider,6)
        bottom_layout.addStretch(15)
    def set_left_layout(self):
        self.left_Widget = QWidget(self)
        self.left_Widget.resize(200, 555)
        self.left_Widget.move(0,55)
        self.left_Widget.setObjectName('left_Widget')
        self.left_Widget.setStyleSheet('background-color:#16181C;')
        #self.left_Widget.setStyleSheet('background-color:pink;')


        header_layout = QVBoxLayout(self.left_Widget)
        header_layout.setContentsMargins(0,5,0,0)
        header_layout.addWidget(self.recommendLabel)
        header_layout.addWidget(self.left_header_List)
        header_layout.addWidget(self.myMusicLabel)
        header_layout.addWidget(self.left_mid_List)
        header_layout.addWidget(self.singsListLabel)
        header_layout.addStretch(25)
    def set_right_layout(self):
        self.right_Widget = NativeWidget(self)

    #信号与槽的链接
    def set_slot(self):
        #顶部按钮
        self.btn_close.clicked.connect(self.win_close)
        self.btn_min.clicked.connect(self.win_mix)
        #左侧按钮
        self.left_header_List.itemClicked.connect(self.changeLeft_H)
        self.left_mid_List.itemClicked.connect(self.changeLeft_M)
        #底部按钮
        self.btn_play.clicked.connect(self.play_pause_chick)
        self.btn_play.objectNameChanged.connect(self.btn_play_NameChanged)
        self.btn_last.clicked.connect(self.btn_last_chick)
        self.btn_next.clicked.connect(self.btn_next_chick)
        #底部时间滑块
        self.time_slider.sliderReleased.connect(self.adjust_time)
        #右侧布局

        #当前媒体音乐列表索引改变触发 让显示列表页同时指向新索引 使其高亮
        self._first_meida.player_list.currentIndexChanged.connect(self.sync_right_Widget)
        self.right_Widget.benDi_table.itemDoubleClicked.connect(self.new_Music_play)
        #音量滑块
        self.volumeSlider.valueChanged.connect(self.set_Volume)
        #时间显示
        self._first_meida.player.durationChanged.connect(self.AllTimeSet)


    #**********槽函数分割线***********
    #顶部按钮操作
    def win_close(self):
        self.close()
    def win_mix(self):
        self.showMinimized()
        #self.showMaximized()#最大化窗口
    #底部按钮操作
    def play_pause_chick(self):
        if self.btn_play.objectName() =='btn_play':
            self.btn_play.setObjectName('btn_pause')
            self._first_meida.playMusic()
        else:
            self.btn_play.setObjectName('btn_play')
            self._first_meida.pauseMusic()
    def btn_last_chick(self):
        #记录切歌前的歌曲索引值
        self.Pre_Mic_Index = self._first_meida.player_list.currentIndex()
        self.changeFlag = True
        #设置播放键的类名，因为他该变化图标和功能了
        self.btn_play.setObjectName('btn_pause')
        self._first_meida.player_list.previous()

        #此处有bug 在无播放的时候 切歌 不会自动播放 很好解决 但怕遗忘
    def btn_next_chick(self):
        # 记录切歌前的歌曲索引值
        self.Pre_Mic_Index = self._first_meida.player_list.currentIndex()
        self.changeFlag = True
        # 设置播放键的类名，因为他该变化图标和功能了
        self.btn_play.setObjectName('btn_pause')
        self._first_meida.player_list.next()

    def btn_play_NameChanged(self):
        with open(r'styleByQss\btn_play.qss', 'r') as f:
            self.btn_play.setStyleSheet(f.read())
    def new_Music_play(self,name_info):
        self.btn_play.setObjectName('btn_pause')
        music_name = name_info.text()
        print(music_name)
        index = name_info.row()
        self._first_meida.changeMusic(music_name,index)
    #调整时间（快进，快退）
    def adjust_time(self):
        ok_time = self.time_slider.value()
        alltime = self._first_meida.player.duration()
        nowtime = (ok_time/1000)*alltime
        self._first_meida.player.setPosition(nowtime)
    #playlist 与 right_Widget.benDi_table 的索引同步
    def sync_right_Widget(self,index):
        #切换媒体后 暂停音乐 等进度条和label设置好好 在开启音乐 在stopMusic与playMusic中也重新开启定时器

        self._first_meida.stopMusic()
        self.time_slot()#然后设置一下进度条 和当前时间

        if self.changeFlag:#如果按钮切换的 才执行这里的代码。如果是双击，TableWidget直接把双击的item设置为高亮，其他取消高亮
            self.changeFlag = False
            #设置前一首音乐行 为取消选中状态
            pre_item = self.right_Widget.benDi_table.item(self.Pre_Mic_Index, 0)  # 获取第pre_row行第0列元素
            #QItemSelectionModel.Rows 是选中item所在的行，QItemSelectionModel.Deselect把改行设置为不选中状态
            self.right_Widget.benDi_table.setCurrentItem(pre_item,QItemSelectionModel.Rows|QItemSelectionModel.Deselect)
        #设置当前播放音乐行高亮(为选中状态)
        now_item = self.right_Widget.benDi_table.item(index,0)#获取第index行第0列元素
        #QItemSelectionModel.Rows 是选中item所在的行，QItemSelectionModel.Select把改行设置为选中状态
        self.right_Widget.benDi_table.setCurrentItem(now_item,QItemSelectionModel.Rows|QItemSelectionModel.Select)

        self._first_meida.playMusic()
    #音量滑块
    def set_Volume(self,volume_info):
        #print(volume_info)
        self._first_meida.player.setVolume(volume_info)

    # 定时器 - 歌曲进度时间显示
    def time_slot(self):
        #更新进度条的进度
        self.set_time_slider()
        #设置当前时间
        currentTime = self._first_meida.player.position() / 1000
        self.now_time_label.setText(self.getTimeFormal(currentTime))

        # time = QTime.currentTime() 获取当前时间
        # print(time.toString(Qt.DefaultLocaleLongDate)) 把当前时间转换为当地时分秒后打印
        # self.player.setPosition(1000000)#设置当前进度

    # 时间显示
    def AllTimeSet(self):

        alltime = int(self._first_meida.player.duration() / 1000)  # 获取歌曲总时长 单位是毫秒 先进性 秒的转换
        self.all_time_label.setText(self.getTimeFormal(alltime))
        # alltime = self._first_meida.player.position() / 1000
        # self.now_time_label.setText(self.getTimeFormal())
    #右侧窗口切换
    def changeLeft_H(self,info=None):
        self.right_Widget.hide()
        self.w1.show()
    def changeLeft_M(self,info=None):
        if self.left_mid_List.currentRow() == 0:
            self.right_Widget.show()
            self.w1.hide()
        else:
            self.changeLeft_H()
    #**********槽函数end***********

    #时间格式设定
    def getTimeFormal(self,time):
        m = int(time // 60)
        s = int(time - m * 60)
        m = str(m)
        s = str(s)
        if len(m)<2:
            m = '0'+m
        if len(s)<2:
            s = '0'+s
        finish_time = str(m) + ':' + str(s)
        return finish_time

    # 更新进度条的进度
    def set_time_slider(self):
        nowtime = self._first_meida.player.position()
        alltime = self._first_meida.player.duration()
        percentage = (nowtime/alltime)*1000
        #print('当前歌曲'+str(int(percentage))+'s')
        self.time_slider.setValue(percentage)

class headerWidget(QWidget):
    def __init__(self,mParent):

        super().__init__(mParent)
        self.newMove = False    #设置鼠标事件的判定参数
        self.mParent = mParent #传递的参数 是主窗口，也就是其父控件
    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        #如果是鼠标左键的点击 才执行
        if event.buttons() == Qt.LeftButton:
            #属性设为true 这样鼠标move事件才可以运行
            #如果没有这个变量，触发移动事件时候 窗口就会一直跟着鼠标 无法终止
            self.newMove = True
            #一个直接 桌面坐标x，y 一个是窗口xy
            #self.get_extent = event.globalPos() - self.pos()

            #得到点击时候 鼠标距离 桌面原点的 坐标
            self.mouseX = event.globalX()
            self.mouseY = event.globalY()

            #得到窗口原点的坐标
            self.originX = self.mParent.x()
            self.originY = self.mParent.y()

            #event.accept()

    def mouseMoveEvent(self, event):
        if self.newMove:
            #新的鼠标距离桌面原点的坐标 与 点击时，鼠标距离桌面原点距离相减 得到一个位移向量
            move_x = event.globalX()-self.mouseX
            move_y = event.globalY()-self.mouseY

            #窗口原点的坐标 + 位移向量得到新位置
            new_x = self.originX + move_x
            new_y = self.originY + move_y

            #设置新位置
            self.mParent.move(new_x,new_y)

        #print(self.mParent.pos())
        #event.accept()

    def mouseReleaseEvent(self, event):
        #鼠标释放时，属性变为False
            self.newMove = False


if __name__ =='__main__':
    app = QApplication(sys.argv)

    window = MainUi()

    window.show()

    sys.exit(app.exec_())