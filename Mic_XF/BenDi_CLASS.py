from PyQt5.Qt import *
import sys
import os
import eyed3#获取歌曲时间长度

'''
    本文件目前一个类 
    NativeWidget 实现本地文件的窗口UI，以及生产本地 音乐的url
'''
class NativeWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(820, 555)
        self.move(204,55)
        self.setObjectName('right_Widget')
        with open(r'styleByQss\text.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.benDi_table = QTableWidget()
        self.set_UI()

    def set_Label(self):
        self.loc_File_label = QLabel("本地音乐")
        self.loc_File_label.setObjectName("loc_File_label")
        self.loc_File_label.setContentsMargins(20,18,0,10)
    def set_Frame(self):
        self.right_line = QFrame()
        self.right_line.setObjectName("right_line")
        self.right_line.setFrameShape(QFrame.HLine)#设置样式 有盒子 有水平线 有垂线
        self.right_line.setFrameShadow(QFrame.Plain)#设置线的样式，是实线 还是填充线
        self.right_line.resize(1024, 5)
        self.right_line.setLineWidth(2)#设置线的宽度
        #self.right_line.setMidLineWidth(2)  # 设置中线宽度

    def set_UI(self):
        self.set_Label()
        self.set_Frame()

        music_files = self.getMusicFiles()
        row_count = len(music_files)
        self.set_right_Table(row_count)  # 初始化并且设置播放tabel 参数是行数
        self.music_OK_list = [] #用来保存好已经处理过的音乐信息
        self.set_music_format(music_files) #这个函数会处理好music_OK_list
        self.set_rTable_context(row_count)#设置tabel里面的内容 参数是行数



        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(0,0,0,0)#设置布局的内容与布局的边框的距离都为0
        right_layout.setSpacing(0)#设置布局内 部件与部件之间的距离为0
        right_layout.addWidget(self.loc_File_label)
        right_layout.addWidget(self.right_line)
        right_layout.addWidget(self.benDi_table)
    #设置列表的样式，属性
    def set_right_Table(self,row_count):
        header_titles = ['', '音乐标题', '歌手', '时长']


        self.benDi_table.setRowCount(row_count)  # 行数
        self.benDi_table.setColumnCount(4)  # 列数
        self.benDi_table.setHorizontalHeaderLabels(header_titles)  # 设置第一行的标题
        self.benDi_table.verticalHeader().setVisible(False)  # 设置垂直标题行不显示
        self.benDi_table.setShowGrid(False)  # 设置单元格的边框没有线
        self.benDi_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 标题栏的宽度锁定（每一列的宽度锁定）不可拖拽
        self.benDi_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置单元格内容为只能读 不能编辑
        self.benDi_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 当选择时 为选择整行

        self.benDi_table.setColumnWidth(0, 80)  # 设置每一列的宽度
        self.benDi_table.setColumnWidth(1, 310)
        self.benDi_table.setColumnWidth(2, 310)
        self.benDi_table.setColumnWidth(3, 120)
        #设置第一行为选中状态
        self.benDi_table.setCurrentCell(0,0, QItemSelectionModel.Rows | QItemSelectionModel.Select)
    #向列表中添加内容
    def set_rTable_context(self,row_count):
        i = 0   #用于记录第一列的歌曲个数
        qTableItem_List = []
        for item in self.music_OK_list:
            digit = str(i)
            if len(digit)<2:
                digit = '0'+str(i)
            music_number = QTableWidgetItem(digit)
            music_number.setTextAlignment(Qt.AlignCenter)#设置内容居中显示
            music_author = QTableWidgetItem(item[0])
            music_name   = QTableWidgetItem(item[1])
            music_time = QTableWidgetItem(item[2])
            music_time.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)#实现居中，只是实现方式不一样
            qTableItem_List.append([music_number,music_name,music_author,music_time])
            i+=1
        for r in range(row_count):#行和列添加内容
            for c in range(4):
                self.benDi_table.setItem(r, c, qTableItem_List[r][c])

    # 调整歌曲信息，适配歌曲列表
    def set_music_format(self,music_files):
        path = self.getMusicPath()
        for file in music_files:
            url = path+file
            try:
                # 加载本地文件
                voice_file = eyed3.load(url)
                # 获取音频时长
                secs = int(voice_file.info.time_secs)
            except:
                secs = 0
            if file.find('-') == -1:
                onelist = file.split('.')
                t = onelist[0].rstrip()
                onelist[1] = t
                onelist[0] = "未知歌手"

            else:
                onelist = file.split('-')
                onelist[0] = onelist[0].rstrip()
                onelist[1] = onelist[1].lstrip().split('.')[0]
            onelist.append(self.getTimeFormal(secs))
            self.music_OK_list.append(onelist)
    # 时间格式设定
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
    def getMusicPath(self):
        pwd = os.getcwd()  # 获取当前文件路径
        music_pwd = pwd + '\music\\'  # 获取当前音乐文件夹路径
        return music_pwd

    def getMusicFiles(self):
        music_pwd = self.getMusicPath()
        files = os.listdir(music_pwd)  # 获取音乐文件夹下的音乐文件
        return files
    def getMusicUrls(self):
        music_pwd = self.getMusicPath()
        files = os.listdir(music_pwd)  # 获取音乐文件夹下的音乐文件
        music_Urls = []
        for i in files:
            url = music_pwd + i
            music_Urls.append(url)
        return music_Urls




def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setContentsMargins(0,0,0,0)
    # window.resize(1024, 600)
    # window.move(450, 185)
    gui = NativeWidget(window)
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()