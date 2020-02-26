from PyQt5.Qt import *
import sys
from  Main_CLASS import *


app = QApplication(sys.argv)

window = MainUi()

window.show()

sys.exit(app.exec_())