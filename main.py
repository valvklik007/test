import json
from PyQt5.QtWidgets import QButtonGroup, QTabWidget
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QRadioButton
import sys


class SaveJson:
    def __init__(self, path):
        self.__path = path

    def save(self, data):
        with open(self.__path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        with open(self.__path, 'r', encoding='utf-8') as f:
            return json.load(f)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        self.__numProgressBar = int(0)
        self.checkBox.stateChanged.connect(self.loadProgresBar)
        self.checkBox_2.stateChanged.connect(self.loadProgresBar)
        self.checkBox_3.stateChanged.connect(self.loadProgresBar)
        self.checkBox_4.stateChanged.connect(self.loadProgresBar)

        self.horizontalSlider.valueChanged.connect(lambda value: self.label.setText(f'<html><head/><body><p align=\"center\">{str(value)}</p></body></html>'))

        self.lineEdit.setValidator(QtGui.QIntValidator())

        self.pushButton.clicked.connect(self.modifyComboBox)

        self.__buttonGroup = QButtonGroup(self)
        for idx, button in enumerate(self.frame_3.findChildren(QRadioButton), start=1):
            self.__buttonGroup.addButton(button, idx)

        self.saveJson = SaveJson("config.json")
        self.pushButton_2.clicked.connect(self.saveJsonConfig)

        self.loadJsonConfig()

    def loadJsonConfig(self):
        data = self.saveJson.load()
        self.checkBox.setChecked(data['checkBox'])
        self.checkBox_2.setChecked(data['checkBox_2'])
        self.checkBox_3.setChecked(data['checkBox_3'])
        self.checkBox_4.setChecked(data['checkBox_4'])
        self.horizontalSlider.setValue(int(data['horizontalSlider']))
        self.textEdit.setText(data['text'])

    def saveJsonConfig(self):
        data = {
            "checkBox": self.checkBox.isChecked(),
            "checkBox_2": self.checkBox_2.isChecked(),
            "checkBox_3": self.checkBox_3.isChecked(),
            "checkBox_4": self.checkBox_4.isChecked(),
            "horizontalSlider": self.horizontalSlider.value(),
            "text": self.textEdit.toPlainText(),
        }
        self.saveJson.save(data)

    def loadProgresBar(self, state):
        if state == QtCore.Qt.Checked:
            self.__numProgressBar += 25
        else:
            self.__numProgressBar -= 25
        self.progressBar.setValue(self.__numProgressBar)

    def modifyComboBox(self):
        num = int(self.comboBox.count() - 1)
        if self.__buttonGroup.checkedId() == 1:
            self.comboBox.removeItem(num)
        else:
            self.comboBox.addItem(str(num+2))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())