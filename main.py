import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QTimer
lst = []
flag = False
h = ''


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.timer = QTimer()
        self.timer.start()
        self.timer.timeout.connect(self.display)
        self.tableWidget.cellClicked.connect(self.aaa)
        self.pushButton.clicked.connect(self.fl)

    def display(self):
        try:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            result = cur.execute("SELECT * FROM инфа").fetchall()
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            self.tableWidget.setColumnWidth(0, 10)
            self.tableWidget.setColumnWidth(1, 100)
            self.tableWidget.setColumnWidth(2, 150)
            self.tableWidget.setColumnWidth(3, 150)
            self.tableWidget.setColumnWidth(4, 350)
            self.tableWidget.setColumnWidth(6, 200)
            self.tableWidget.setHorizontalHeaderLabels(('ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                                                        'Описание вкуса', 'Цена (руб.)', 'Объем упаковки (г)'))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        except IndexError:
            pass

    def aaa(self):
        global flag, h, lst
        flag = True
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM инфа").fetchall()
        row = self.tableWidget.currentRow()
        for x in range(len(result[0])):
            value = self.tableWidget.item(row, x)
            value = value.text()
            lst.append(value)

    def fl(self):
        global flag
        flag = False


class Clss(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.ins)

    def ins(self):
        global flag
        global lst
        global h
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM инфа").fetchall()
        if not flag:
            if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text() \
                    and self.lineEdit_5.text() and self.lineEdit_6.text():
                cur.execute("INSERT INTO инфа VALUES (?, ?, ?, ?, ?, ?, ?)", (len(result) + 1, self.lineEdit.text(),
                            self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                            self.lineEdit_5.text(), self.lineEdit_6.text()))
                self.close()
        else:
            if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text() \
                    and self.lineEdit_5.text() and self.lineEdit_6.text():
                s = "UPDATE инфа SET 'Название сорта' = '"
                s += self.lineEdit.text()
                s += "' WHERE ID = "
                s += h
                s1 = "UPDATE инфа SET 'Степень обжарки' = '"
                s1 += self.lineEdit_2.text()
                s1 += "' WHERE ID = "
                s1 += h
                s2 = "UPDATE инфа SET 'Молотый/в зернах' = '"
                s2 += self.lineEdit_3.text()
                s2 += "' WHERE ID = "
                s2 += h
                s3 = "UPDATE инфа SET 'Описание вкуса' = '"
                s3 += self.lineEdit_4.text()
                s3 += "' WHERE ID = "
                s3 += h
                s4 = "UPDATE инфа SET 'Цена (руб.)' = '"
                s4 += self.lineEdit_5.text()
                s4 += "' WHERE ID = "
                s4 += h
                s5 = "UPDATE инфа SET 'Объем упаковки (г)' = '"
                s5 += self.lineEdit_6.text()
                s5 += "' WHERE ID = "
                s5 += h
                cur.execute(s)
                cur.execute(s1)
                cur.execute(s2)
                cur.execute(s3)
                cur.execute(s4)
                cur.execute(s5)
                self.close()

        con.commit()
        con.close()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")

    def edit(self):
        global lst, h
        h = lst[0]
        self.lineEdit.setText(lst[1])
        self.lineEdit_2.setText(lst[2])
        self.lineEdit_3.setText(lst[3])
        self.lineEdit_4.setText(lst[4])
        self.lineEdit_5.setText(lst[5])
        self.lineEdit_6.setText(lst[6])
        lst = []

    def dele(self):
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    yx = Clss()
    ex.pushButton.clicked.connect(yx.show)
    ex.pushButton.clicked.connect(yx.dele)
    ex.tableWidget.cellClicked.connect(yx.show)
    ex.tableWidget.cellClicked.connect(yx.edit)
    ex.show()
    sys.exit(app.exec())