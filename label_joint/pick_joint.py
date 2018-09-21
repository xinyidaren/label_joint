
from untitled import Ui_MainWindow
from PyQt5.QtCore import Qt,QPoint,QSettings
from my_show_widget import *
import cv2
import os

class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置ini文件
        self.settings = QSettings("./QtPad.ini", QSettings.IniFormat)
        self.lineEdit_dirSaveImage.setText(self.settings.value('dirSaveImage'))
        self.lineEdit_dirSaveAnnotation.setText(self.settings.value('dirSaveAnnotation'))
        self.lineEdit_RGBdirSaveImage.setText(self.settings.value('RGBdirSaveImage'))

        self.listWidget_image_list.clear()
        self.listWidget_image_list.addItems(self.getFileList(self.settings.value('dirSaveImage')))
        self.cap_depth = None
        self.jump_frame = 1
        self.last_choice = None
        self.dir_depth_video = None
        self.initUI()
        self.action_last_page.triggered.connect(self.last_page)
        self.action_next_page.triggered.connect(self.next_page)
        self.pushButton_delete_files.clicked.connect(self.delete_files)
        self.pushButton_dirSaveAnnotation.clicked.connect(self.change_dir_annotation)
        self.pushButton_dirSaveImage.clicked.connect(self.change_dir_image)
        self.pushButton_RGBdirSaveImage.clicked.connect(self.change_dir_RGBimage)
        self.pushButton_Head.clicked.connect(self.change_body_part)
        self.pushButton_LShouder.clicked.connect(self.change_body_part)
        self.pushButton_LAncon.clicked.connect(self.change_body_part)
        self.pushButton_LHand.clicked.connect(self.change_body_part)
        self.pushButton_RShouder.clicked.connect(self.change_body_part)
        self.pushButton_RAncon.clicked.connect(self.change_body_part)
        self.pushButton_RHand.clicked.connect(self.change_body_part)
        self.action_openImageFolder.triggered.connect(self.openImageFolder)
        self.action_openDepthVideo.triggered.connect(self.openDepthVideo)
        self.listWidget_image_list.itemClicked.connect(self.listChange)
        self.listWidget_image_list.setCurrentRow(0)
        self.listWidget_image_list.itemClicked.emit(self.listWidget_image_list.item(0))
        self.update()

    def initUI(self):

        self.frame1 = MyShowWidget()
        self.frame1.setMinimumSize(QtCore.QSize(500, 500))
        self.frame1.setObjectName("frame1")
        self.horizontalLayout.addWidget(self.frame1)
        self.frame1.myclicked.connect(self.update_frame2_annotation)
        self.frame2 = MyShowWidget()
        self.frame2.setMinimumSize(QtCore.QSize(500, 500))
        self.frame2.setObjectName("frame2")
        self.horizontalLayout.addWidget(self.frame2)
        self.frame2.myclicked.connect(self.update_frame1_annotation)

    def last_page(self):
        if(self.listWidget_image_list.currentRow() > 0):
            self.listWidget_image_list.itemClicked.emit(
                self.listWidget_image_list.item(self.listWidget_image_list.currentRow() - 1))
            self.listWidget_image_list.setCurrentRow(self.listWidget_image_list.currentRow() - 1)

    def next_page(self):
        self.listWidget_image_list.itemClicked.emit(
            self.listWidget_image_list.item(self.listWidget_image_list.currentRow()+1))
        self.listWidget_image_list.setCurrentRow(self.listWidget_image_list.currentRow()+1)
    def delete_files(self):
        file = self.listWidget_image_list.currentItem().text()
        self.listWidget_image_list.takeItem(self.listWidget_image_list.currentRow())
        self.listWidget_image_list.removeItemWidget(self.listWidget_image_list.currentItem())
        self.listWidget_image_list.itemClicked.emit(self.listWidget_image_list.currentItem())

        os.remove(self.lineEdit_RGBdirSaveImage.text()+ '/' +
                                     file.split('/')[-1])
        os.remove(file)

    def update_frame1_annotation(self,ann,x,y):
        self.frame1.dict_body[ann] = x,y
        self.frame1.update()

    def update_frame2_annotation(self,ann,x,y):
        self.frame2.dict_body[ann] = x,y
        self.frame2.update()

    def change_dir_annotation(self):
        dir = QFileDialog.getExistingDirectory(self,"选择标注保存路径",'/home/learn/PycharmProjects/test/')
        self.lineEdit_dirSaveAnnotation.setText(dir)


    def change_dir_image(self):
        dir = QFileDialog.getExistingDirectory(self,"选择图片保存路径",'/home/learn/PycharmProjects/test/')
        self.lineEdit_dirSaveImage.setText(dir)

    def change_dir_RGBimage(self):
        dir = QFileDialog.getExistingDirectory(self,"选择RGB图片保存路径",'/home/learn/PycharmProjects/test/')
        self.lineEdit_RGBdirSaveImage.setText(dir)

    def change_body_part(self):
        sender = self.sender()
        if not self.last_choice:
            self.last_choice = sender
            self.frame1.str_body = sender.objectName()[11:]
            self.frame2.str_body = sender.objectName()[11:]

        elif self.last_choice == sender:
            self.last_choice = None
            self.frame1.str_body = None
            self.frame2.str_body = None
        else :
            self.last_choice.setChecked(False)
            self.last_choice = sender
            self.frame1.str_body = sender.objectName()[11:]
            self.frame2.str_body = sender.objectName()[11:]

        self.frame1.update()
        self.frame2.update()


    def openImageFolder(self):
        dir = QFileDialog.getExistingDirectory(self,"打开",'/')

    def openDepthVideo(self):
        self.dir_depth_video,ok = QFileDialog.getOpenFileName(self,"打开",'/home/learn/PycharmProjects/test/',"All Files (*);;Video Files(*.avi)")
        if not self.cap_depth:
            self.cap_depth = cv2.VideoCapture(self.dir_depth_video)

    def closeEvent(self,event):
        self.settings.setValue("dirSaveImage",self.lineEdit_dirSaveImage.text())
        self.settings.setValue("dirSaveAnnotation", self.lineEdit_dirSaveAnnotation.text())
        self.settings.setValue("RGBdirSaveImage", self.lineEdit_RGBdirSaveImage.text())
        del self.settings

    def getFileList(self,fileDir):
        _list = os.listdir(fileDir)  # 列出文件夹下所有的目录与文件
        dirlist = []
        for i in range(0, len(_list)):
            path = os.path.join(fileDir, _list[i])
            if os.path.isfile(path):
                dirlist.append(path)
        dirlist.sort()
        return dirlist

    def listChange(self,imageChoice):
        self.frame2.showImageFromDir(imageChoice.text(),self.lineEdit_RGBdirSaveImage.text()+ '/' +
                                     imageChoice.text().split('/')[-1],
                                self.lineEdit_dirSaveAnnotation.text()+'/'+
                                     imageChoice.text().split('/')[-1][:-4]+'.xml','depth')

        self.frame1.showImageFromDir(imageChoice.text(),self.lineEdit_RGBdirSaveImage.text()+ '/' +
                                     imageChoice.text().split('/')[-1],
                                self.lineEdit_dirSaveAnnotation.text() + '/' +
                                     imageChoice.text().split('/')[-1][:-4] + '.xml','color')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())