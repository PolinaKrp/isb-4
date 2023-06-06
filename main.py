import multiprocessing as mp
import re
import sys
import time


from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QProgressBar,
                             QPushButton)

from graph import graph_drawing
from hashing import algorithm_Luhn, check_hash
from work_with_file import read_settings, write_settings

class Window(QMainWindow):
    def __init__(self) -> None:
        """
        Initialization function
        """
        super(Window, self).__init__()
        self.setWindowTitle('Search of bank card')
        self.setFixedSize(800, 600)
        self.background = QLabel(self)
        self.background.setGeometry(100, 0, 800, 800)
        self.background.setPixmap(QPixmap("icon.jpg").scaled(800, 800))
        self.info = QLabel(self)
        self.info.setText("Select the beginning of the card")
        self.info.setGeometry(280, 0, 500, 50)
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setGeometry(600, 800, 400, 800)
        self.progress.hide()
        self.button_card = QPushButton('Find a bank card', self)
        self.button_card.setStyleSheet("QPushButton{\n"
                                       "color:black;\n"
                                       "background-color: #CCCCFF;\n"
                                       "border-radius: 10;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color:#FFCCFF;\n"
                                       "}\n"
                                       "")
        self.button_card.setGeometry(290, 190, 200, 50)
        self.button_card.clicked.connect(self.preparation)
        self.button_card.hide()
        self.result = QLabel(self)
        self.result.setGeometry(220, 250, 400, 100)
        self.pool_size = QtWidgets.QComboBox(self)
        self.pool_size.setStyleSheet("QComboBox{\n"
                                       "background-color: #CCCCFF;}\n"
                                       )
        self.pool_size.addItems([str(i) for i in range(1, 33)])
        self.pool_size.setGeometry(290, 120, 200, 50)
        self.pool_size.hide()
        self.number = QtWidgets.QComboBox(self)
        self.number.setStyleSheet("QComboBox{\n"
                                       "background-color: #CCCCFF;}\n"
                                       )
        self.number.addItems(settings["begin_digits"])
        self.number.setGeometry(290, 50, 200, 50)
        self.number.activated[str].connect(self.on_activated)
        self.graph = QPushButton('Build graph', self)
        self.graph.setStyleSheet("QPushButton{\n"
                                       "color:black;\n"
                                       "background-color: #CCCCFF;\n"
                                       "border-radius: 10;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color:#FFCCFF;\n"
                                       "}\n"
                                       "")
        self.graph.setGeometry(290, 400, 200, 50)
        self.graph.clicked.connect(self.show_graph)
        self.graph.hide()
        self.show()

    def on_activated(self, text: str) -> None:
        """
        Number assignment function
        """
        self.graph.hide()
        self.pool_size.show()
        try:
            self.number = int(re.findall('(\d+)', text)[0])
        except:
            self.number = settings['begin_digits'][0]
        self.pool_size.activated[str].connect(self.choose_pool)

    def choose_pool(self, text: str) -> None:
        """
        Pool sizing function
        """
        try:
            self.size = int(re.findall('(\d+)', text)[0])
        except:
            self.size = 0
        self.button_card.show()

    def preparation(self) -> None:
        """
        The function prepares the progress line and the list for the pool
        """

        items = [(i, self.number) for i in range(99999, 10000000)]
        start = time.time()
        self.progress.show()
        QApplication.processEvents()
        self.progress_bar(start, items)

    def progress_bar(self, start: float, items: list) -> None:
        """
        Search progress display function
        """
        with mp.Pool(self.size) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    self.success(start, result)
                    p.terminate()
                    break
                self.update_progress_bar(i)
            else:
                self.result.setText("Don't find!")
                self.progress.setValue(0)

    def update_progress_bar(self, i: int) -> None:
        """
        Progress update feature
        """

        self.progress.setValue(int((i)/9900000*100))
        QApplication.processEvents()

    def success(self, start: float, result: int) -> None:
        """
        Card information output function
        """
        self.result_card = result
        self.progress.setValue(100)
        end = time.time() - start
        result_text = f'Decoded number: {result}\n'
        result_text += f'Checking for the Luhn algorithm: {algorithm_Luhn(result)}\n'
        result_text += f'Time: {end:.2f} seconds'
        self.result.setText(result_text)
        self.graph.show()

    def show_graph(self) -> None:
        """
        Graph inference function
        """
        graph_drawing(self.result_card)


def application() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()