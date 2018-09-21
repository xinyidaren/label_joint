import sys
import cv2
import os
from lxml import etree
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt,QPoint
from show_widget import *

class MyShowWidget(QWidget, Ui_show_widget):
    myclicked = QtCore.pyqtSignal(str,int,int)
    def __init__(self, parent=None):
        super(MyShowWidget, self).__init__(parent)
        self.setupUi(self)
        self.pix = QPixmap(self.width(), self.height())
        self.pix.fill(Qt.white)
        self.minipix = QPixmap(32,32)
        self.minipix.fill(Qt.white)
        self.imageDir = None
        self.RGBimageDir = None
        self.annotationDir = None
        self.xmltree = None
        self.tempPix = QPixmap(self.width(), self.height())
        self.tempPix.fill(Qt.white)
        self.mousePoint = QPoint(0,0)
        self.str_body = None
        self.dict_body = dict()
        self.dict_body["Head"] = None
        self.dict_body["LShouder"] = None
        self.dict_body["LAncon"] = None
        self.dict_body["LHand"] = None
        self.dict_body["RShouder"] = None
        self.dict_body["RAncon"] = None
        self.dict_body["RHand"] = None

    def show_frame(self,frame):
        show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        show = cv2.applyColorMap(show, cv2.COLORMAP_OCEAN)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(showImage)
        self.update()

    def save_files(self,imageDir,RGBimageDir,annotationDir,fileName):
        root = etree.Element('root')
        ImageInfo = etree.SubElement(root, 'ImageInfo')
        ImageDir = etree.SubElement(ImageInfo, 'DepthImageDir')
        ImageDir.text = imageDir
        RGBImageDir = etree.SubElement(ImageInfo, 'RGBImageDir')
        RGBImageDir.text = RGBimageDir
        ImageName = etree.SubElement(ImageInfo, 'ImageName')
        ImageName.text = fileName
        Head = etree.SubElement(ImageInfo, 'Head')
        Head.text = str(0) + ',' + str(0)
        LShouder = etree.SubElement(ImageInfo, 'LShouder')
        LShouder.text = str(0) + ',' + str(0)
        LAncon = etree.SubElement(ImageInfo, 'LAncon')
        LAncon.text = str(0) + ',' + str(0)
        LHand = etree.SubElement(ImageInfo, 'LHand')
        LHand.text = str(0) + ',' + str(0)
        RShouder = etree.SubElement(ImageInfo, 'RShouder')
        RShouder.text = str(0) + ',' + str(0)
        RAncon = etree.SubElement(ImageInfo, 'RAncon')
        RAncon.text = str(0) + ',' + str(0)
        RHand = etree.SubElement(ImageInfo, 'RHand')
        RHand.text = str(0) + ',' + str(0)
        etree.ElementTree(root).write(annotationDir, pretty_print=True)


    def modify_files(self):
        if self.xmltree:
            root = self.xmltree.getroot()  # 获得该树的树根
            for article in root:  # 这样便可以遍历根元素的所有子元素(这里是article元素)
                if article.tag == 'ImageInfo':
                    article.find(self.str_body).text = str(int(self.dict_body[self.str_body][0]/2)) \
                                                           + ',' + str(int(self.dict_body[self.str_body][1]/2))
            etree.ElementTree(root).write(self.annotationDir, pretty_print=True)
        else:
            self.save_files(self.imageDir,self.RGBimageDir,self.annotationDir,self.imageDir.split('/')[-1])
        self.update()


    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        x, y = self.frame.x(), self.frame.y()
        w, h = self.frame.width()-100,self.frame.height()-100
        if self.pix:
            self.tempPix = self.pix.copy()
            self.minitempPix = self.minipix.copy()
            pp = QPainter(self.tempPix)
            minipp = QPainter(self.minitempPix)
            pp.setPen(QPen(QColor(0, 160, 80),2))
            minipp.setPen(QPen(QColor(255, 0, 0),2))

            pp.drawPoint(self.mousePoint)

            if 'LAncon' in self.dict_body:
                if 'LShouder' in self.dict_body:
                    if self.dict_body["LAncon"] and self.dict_body["LShouder"]:
                        pp.drawLine(self.dict_body["LAncon"][0],self.dict_body["LAncon"][1],
                                self.dict_body["LShouder"][0],self.dict_body["LShouder"][1])
                if 'LHand' in self.dict_body:
                    if self.dict_body["LAncon"] and self.dict_body["LHand"]:
                        pp.drawLine(self.dict_body["LAncon"][0],self.dict_body["LAncon"][1],
                                self.dict_body["LHand"][0],self.dict_body["LHand"][1])
            if 'RAncon' in self.dict_body:
                if 'RShouder' in self.dict_body:
                    if self.dict_body["RAncon"] and self.dict_body["RShouder"]:
                        pp.drawLine(self.dict_body["RAncon"][0],self.dict_body["RAncon"][1],
                                self.dict_body["RShouder"][0],self.dict_body["RShouder"][1])
                if 'RHand' in self.dict_body:
                    if self.dict_body["RAncon"] and self.dict_body["RHand"]:
                        pp.drawLine(self.dict_body["RAncon"][0],self.dict_body["RAncon"][1],
                                self.dict_body["RHand"][0],self.dict_body["RHand"][1])
            if ('LShouder' in self.dict_body) and ('RShouder' in self.dict_body):
                if self.dict_body["LShouder"] and self.dict_body["RShouder"]:
                    pp.drawLine(self.dict_body["LShouder"][0], self.dict_body["LShouder"][1],
                            self.dict_body["RShouder"][0],self.dict_body["RShouder"][1])
                if('Head' in self.dict_body):
                    if self.dict_body["Head"] and self.dict_body["LShouder"] and self.dict_body["RShouder"]:
                        pp.drawLine((self.dict_body["LShouder"][0] + self.dict_body["RShouder"][0]) // 2,
                                (self.dict_body["LShouder"][1] + self.dict_body["RShouder"][1]) // 2,
                                self.dict_body["Head"][0], self.dict_body["Head"][1])
            pp.setPen(QPen(QColor(0, 230, 160), 5))
            pp.setFont(QFont('SansSerif', 20));
            if self.dict_body.values():
                for value in self.dict_body.values():
                    if value:
                        pp.setPen(QPen(QColor(255, 0, 0), 2))
                        pp.drawEllipse(value[0]-1,value[1]-1,1,1)
                        minipp.drawPoint(value[0]*64/self.tempPix.width(),value[1]*64/self.tempPix.height())
            painter.drawPixmap(x, y, self.tempPix)
            painter.drawPixmap(w, h, self.minitempPix)
            painter.setPen(QPen(QColor(0, 230, 160), 5))
            painter.setFont(QFont('SansSerif', 20));
            painter.drawText(self.mousePoint, self.str_body)

    def showImageFromDir(self,imageDir,RGBImageDir,annotationDir,type):

        self.imageDir = imageDir
        self.annotationDir = annotationDir
        self.RGBimageDir = RGBImageDir
        self.type = type
        if(type == 'depth'):
            img = cv2.imread(imageDir)
            show = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
            cv2.imshow("ddd",show)
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            show = cv2.resize(show,(show.shape[1]*2,show.shape[0]*2))
        elif(type =='color'):
            img = cv2.imread(RGBImageDir)
            show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            show = cv2.resize(show,(show.shape[1]*2,show.shape[0]*2))
        showImage = QImage(show.data, show.shape[1], show.shape[0],show.shape[1]*3, QImage.Format_RGB888)
        self.pix = QPixmap.fromImage(showImage)
        mini_show = cv2.resize(show, (64, 64), interpolation=cv2.INTER_AREA)
        minishowImage = QImage(mini_show.data, mini_show.shape[1], mini_show.shape[0],mini_show.shape[1]*3, QImage.Format_RGB888)
        self.minipix = QPixmap.fromImage(minishowImage)
        if os.path.exists(annotationDir):
            self.xmltree = etree.parse(annotationDir)  # 将xml解析为树结构
            root = self.xmltree.getroot()  # 获得该树的树根
            for article in root:  # 这样便可以遍历根元素的所有子元素(这里是article元素)
                if article.tag == 'ImageInfo':
                    self.dict_body["Head"] = [int(i)*2 for i in article.find('Head').text.split(',')]
                    self.dict_body["LShouder"] = [int(i)*2 for i in article.find('LShouder').text.split(',')]
                    self.dict_body["LAncon"] = [int(i)*2 for i in article.find('LAncon').text.split(',')]
                    self.dict_body["LHand"] = [int(i)*2 for i in article.find('LHand').text.split(',')]
                    self.dict_body["RShouder"] = [int(i)*2 for i in article.find('RShouder').text.split(',')]
                    self.dict_body["RAncon"] = [int(i)*2 for i in article.find('RAncon').text.split(',')]
                    self.dict_body["RHand"] = [int(i)*2 for i in article.find('RHand').text.split(',')]
        else:
            self.dict_body["Head"] = None
            self.dict_body["LShouder"] = None
            self.dict_body["LAncon"] = None
            self.dict_body["LHand"] = None
            self.dict_body["RShouder"] = None
            self.dict_body["RAncon"] = None
            self.dict_body["RHand"] = None
        self.update()

    def mouseMoveEvent(self, Event):
        self.mousePoint = Event.pos()
        self.update()

    def mousePressEvent(self, Event):
        if self.str_body:
            self.dict_body[self.str_body] = Event.pos().x(), Event.pos().y()
            self.modify_files()
            self.myclicked.emit(self.str_body,Event.pos().x(), Event.pos().y())
        self.update()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyShowWidget()
    myWin.show()
    sys.exit(app.exec_())