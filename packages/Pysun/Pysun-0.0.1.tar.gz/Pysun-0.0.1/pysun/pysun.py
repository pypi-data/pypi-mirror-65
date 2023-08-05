import sys, PySide2, PySide2.QtWidgets as w, components as cnts, time

PySide2._setupQtDirectories()

class Window:
    def __init__(self, size: list, title):
        self.app = w.QApplication(sys.argv)
        self.widget = w.QWidget()
        self.size = size
        self.size_x = size[0]
        self.size_y = size[1]
        self.title = title
        self.rendererer = object()
        self.load()
        self.widget.show()
        self.app.exec_()
        sys.exit(0)

    def get(self, name)->any:
        return getattr(self, name)

    def set(self, name, value)->any:
        setattr(self, name, value)
        
    def load(self):
        self.widget.setGeometry(self.widget.x() or 500,self.widget.y() or 500,self.size[0],self.size[1])
        self.widget.setWindowTitle(self.title)
