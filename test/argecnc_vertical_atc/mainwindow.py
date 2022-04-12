#!/usr/bin/python
# -*- coding: utf-8 -*-
from qtpyvcp.widgets.form_widgets.main_window import VCPMainWindow
from qtpyvcp.actions import program_actions, machine_actions
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from qtpyvcp import hal
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize
#from fullscreenshow import Ui_MainWindow
from PyQt5.QtGui import *
from qtpy.QtWidgets import QListWidgetItem
from qtpyvcp.actions.base_actions import setTaskMode
import qtpyvcp.actions.program_actions as pa
from apscheduler.schedulers.background import BackgroundScheduler
import os
import platform
import re
import sys
import linuxcnc
import time
# Setup logging
global temp
global puan
global font_size
temp = ""
puan = 1
font_size = 15
started = False
sched = BackgroundScheduler()
from qtpyvcp.utilities import logger
LOG = logger.getLogger('qtpyvcp.' + __name__)

class MyMainWindow(VCPMainWindow):
    """Main window class for the VCP."""
    def __init__(self, *args, **kwargs):
        global temp
        global started
        super(MyMainWindow, self).__init__(*args, **kwargs)
        self.newBigScreen()
        self.running()
        self.mdiButtonGroup.buttonClicked.connect(self.mdiHandleKeys)
        self.offsetButtonGroup.buttonClicked.connect(self.offsetHandleKeys)
        #self.message.clicked.connect(self.clickMethod)
        self.navParent.clicked.connect(self.goToBack)
        self.navSelect.clicked.connect(self.goFront)
        self.filesystemtable.setRootPath("/media/" + platform.node() + "/")
        temp = self.filesystemtable.getCurrentDirectory()
        self.mediaButton.clicked.connect(self.goToMedia)
        self.filesystemtable.doubleClicked.connect(self.wentInside)
        self.gcode_tw_plus.clicked.connect(self.fontBigger)
        self.gcode_tw_minus.clicked.connect(self.fontSmaller)
        self.toolBox.currentChanged.connect(self.changeFont)
        self.actionbutton_4.clicked.connect(self.fileDisabled)
        self.actionbutton_7.clicked.connect(self.fileEnabled)
        self.actionbutton_2.clicked.connect(self.fileEnabled)
        self.actionbutton_3.clicked.connect(self.fileEnabled)
        self.jog_slider_linear.valueChanged[int].connect(self.changeValueLinear)
        self.jog_slider_angular.valueChanged[int].connect(self.changeValueAngular)
        self.runFrom.clicked.connect(self.runFromFunc)
        #self.sendCode.clicked.connect(self.sendingCode)
        sched.add_job(self.running, 'interval', seconds = 2)
        sched.start()
	
        hal_comp = hal.COMPONENTS['qtpyvcp']
        self.carleft_x = hal_comp.addPin("carleft.in", "bit", "in")
        #self.carleft_x.value = self.isEnabled()
        #self.carleft_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.carright_x = hal_comp.addPin("carright.in", "bit", "in")
        #self.carright_x.value = self.isEnabled()
        #self.carright_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.pdbOpen_x = hal_comp.addPin("pdbOpen.in", "bit", "in")
        #self.pdbOpen_x.value = self.isEnabled()
        #self.pdbOpen_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.carhomed_x = hal_comp.addPin("carhomed.in", "bit", "in")
        #self.carhomed_x.value = self.isEnabled()
        #self.carhomed_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.curPos_x = hal_comp.addPin("curPos.flash-rate", "bit", "in")
        #self.curPos_x.value = self.isEnabled()
        #self.curPos_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.toolSpindle_x = hal_comp.addPin("toolSpindle.flash-rate", "bit", "in")
        #self.toolSpindle_x.value = self.isEnabled()
        #self.toolSpindle_x.valueChanged.connect(self.onCycleReadyPinChanged)
        #self.fullscreen_button.clicked.connect(self.newBigScreen)
        # add any custom methods here

    def onCycleReadyPinChanged(self, value):
        if value:
            self.cycle_start_button.setStyleSheet('border-color: green')
        else:
            self.cycle_start_button.setStyleSheet('border-color: red')

    def running(self):
        global started
        print("__")
        print(pa._run_ok())
        print(started)
        if pa._run_ok() == True and started == False:
            print("Running! Run OK, Started NOPE")
        elif pa._run_ok() == True and started == True:
            print("Running! Run OK, Started OK")
            self.notifyNow("NEKACNC", "Progam is finished!")
            self.fileEnabled2()
            print("VuhuUuUuUuU")
            started = False
        else:
            print("Running! Run NOPE")

    def sendingCode(self, button):
        s = linuxcnc.stat()
        c = linuxcnc.command()
        if setTaskMode(linuxcnc.MODE_MDI):
            ###
            #cmd = "G28"
            #c.mdi(cmd) #tek bir komut çalıştırmak istersen bunu kullanabilirsin
            ###

            #bir dosyadan tüm komutları çekmek istersen de bunu kullanabilirsin
            f = open("/media/" + platform.node() + "/Desktop/mfg.ngc", "r")
            for x in f:
                print(x)
                print("Now going to {}".format(x))
                c.mdi(x)
        else:
            LOG.error("Failed to issue MDI command: {}".format(command))

    def runFromFunc(self, button):
        line = self.gcodetextedit.focused_line
        program_actions.run(line)

    def fileEnabled(self, button):
        global started
        started = False
        ##ggggg
        self.toolBox.setEnabled(True)
        self.toolBox_3.setEnabled(True)
        self.actionbutton_17.setEnabled(True)
        self.actionbutton_18.setEnabled(True)
        self.actionbutton_19.setEnabled(True)
        self.actionbutton_35.setEnabled(True)
        self.actionbutton_36.setEnabled(True)
        self.actionbutton_37.setEnabled(True)
        self.actionbutton_38.setEnabled(True)

    def fileEnabled2(self):
        global started
        started = False
        self.toolBox.setEnabled(True)
        self.toolBox_3.setEnabled(True)
        self.actionbutton_17.setEnabled(True)
        self.actionbutton_18.setEnabled(True)
        self.actionbutton_19.setEnabled(True)
        self.actionbutton_35.setEnabled(True)
        self.actionbutton_36.setEnabled(True)
        self.actionbutton_37.setEnabled(True)
        self.actionbutton_38.setEnabled(True)

    def fileDisabled(self, button):
        global started
        started = True
        ####
        self.toolBox.setEnabled(False)
        self.toolBox_3.setEnabled(False)
        self.actionbutton_17.setEnabled(False)
        self.actionbutton_18.setEnabled(False)
        self.actionbutton_19.setEnabled(False)
        self.actionbutton_35.setEnabled(False)
        self.actionbutton_36.setEnabled(False)
        self.actionbutton_37.setEnabled(False)
        self.actionbutton_38.setEnabled(False)
        self.notifyNow("NEKACNC", "Progam is now working!")

    def changeValueLinear(self, value):
        val = '{}%'.format(value)
        self.jog_linear_label.setText(val)

    def changeValueAngular(self, value):
        val = '{}%'.format(value)
        self.jog_angular_label.setText(val)

    def changeFont(self):
        global font_size
        msgBox = QMessageBox()
        msgBox = setIcont(QMessageBox.Information)
        msgBox = setText("New file is loaded!")
        msgBox = setWindowTitle("Information")
        msgBox = setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue:
            font_size += 1
            self.gcodetextedit.setFont(QFont("Arial",font_size))
            font_size -= 1
            self.gcodetextedit.setFont(QFont("Arial",font_size))

    def fontBigger(self, button):
        global font_size
        if font_size < 30:
            font_size += 1
        self.gcodetextedit.setFont(QFont("Arial",font_size))

    def fontSmaller(self, button):
        global font_size
        if font_size > 10:
            font_size -= 1
        self.gcodetextedit.setFont(QFont("Arial",font_size))

    def goToMedia(self, button):
        global temp
        global puan
        puan = 1
        print(puan)
        self.filesystemtable.setRootPath("/media/" + platform.node() + "/")
        temp = self.filesystemtable.getCurrentDirectory()
        print(self.filesystemtable.getCurrentDirectory())

    def wentInside(self, button):
        global temp
        global puan
        x = re.search("/media/" + platform.node() + "/", self.filesystemtable.getCurrentDirectory())
        if x:
            puan += 1
        print(puan)
        temp = self.filesystemtable.getCurrentDirectory()
        print(self.filesystemtable.getCurrentDirectory())

    def goToBack(self, button):
        global temp
        global puan
        x = re.search("/media/" + platform.node() + "/", self.filesystemtable.getCurrentDirectory())
        if x:
            puan -= 1
            if puan <= 0:
                puan = 1
                self.filesystemtable.setRootPath("/media/" + platform.node() + "/")
                return
        print(puan)
        self.filesystemtable.viewParentDirectory()
        temp = self.filesystemtable.getCurrentDirectory()
        print(temp)

    def goFront(self, button):
        global temp
        global puan
        x = re.search("/media/" + platform.node() + "/", self.filesystemtable.getCurrentDirectory())
        if x:
            puan += 1
        print(puan)
        self.filesystemtable.openSelectedItem()
        temp = self.filesystemtable.getCurrentDirectory()
        print(self.filesystemtable.getCurrentDirectory())

    def newBigScreen(self):
        self.showFullScreen()

    def notifyNow(self, title, msg):
        os.system("notify-send -u critical " + title + " \"" + msg + "\"")

    def clickMethod(self, button):
        QMessageBox.about(self, "Title", "Message2")

    def mdiHandleKeys(self, button):
        char = str(button.text())
        text = self.mdiEntry.text() or '0'
        if text != '0':
            text += char
        else:
            text = char
        self.mdiEntry.setText(text)

    def offsetHandleKeys(self, button):
        char = str(button.text())
        text = self.offsetLabel.text() or '0'
        if text != '0':
            text += char
        else:
            text = char
        self.offsetLabel.setText(text)