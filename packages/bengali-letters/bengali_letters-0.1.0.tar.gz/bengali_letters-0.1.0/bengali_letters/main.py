"""

Extremely simple multiple choice quiz app that displays a Bengali letter and asks
for English (well, Latin) equivalent.

"""

from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtCore import pyqtSlot
import random
import numpy as np

letters=[['k',      'ক'],
         ['kh',     'খ'],
         ['g',      'গ'],
         ['gh',     'ঘ'],
         ['ng',     'ঙ'],
         ['ch',     'চ'],
         ['chh',    'ছ'],
         ['j',     'জ'],
         ['jh',      'ঝ'],
         ['yn',     'ঞ'],
         ['t (hard)',      'ট'],
         ['th (hard)',     'ঠ'],
         ['d',      'ড'],
         ['dh',     'ঢ'],
         ['n (nasal)',      'ণ'],
         ['t (soft)',      'ত'],
         ['th (soft)',     'থ'],
         ['d',      'দ'],
         ['dh',     'ধ'],
         ['n',      'ন'],
         ['p',      'প'],
         ['ph',     'ফ'],
         ['b',      'ব'],
         ['bh',     'ভ'],
         ['m',      'ম'],
         ['y (j)',  'য'],
         ['r (soft)',      'র'],
         ['l',      'ল'],
         #['b',      'ব'],  # yes, this is duplicated in the book (slightly different pronounciation)
         ['sh',     'শ'],
         ['sh (retroflex)',     'ষ'],
         ['s',      'স'],
         ['h',      'হ'],
         ['r (hard)', 'ড়'],
         ['rh',     'ঢ়'],
         ['yo',     'য়'],
         ['a (o)',  'অ'],
         ['a',      'আ'],
         ['i',      'ই'],
         ['i (long, ee)', 'ঈ'],
         ['u', 'উ'],
         ['u (long, oo)', 'ঊ'],
         ['ri', 'ঋ'],
         ['e (ae)', 'এ'],
         ['oi',     'ঐ'],
         ['o', 'ও'], 
         ['ou', 'ঔ'] 
                    #ঢ়
    ]

class LettersQuiz(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
                
        self.score=0
        self.highScore=0
        self.hbox=QtWidgets.QHBoxLayout()
        self.scoreLabel=QtWidgets.QLabel("Score: %d" % (self.score))
        self.scoreLabel.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.scoreLabel.setAlignment(QtCore.Qt.AlignTop)
        self.highScoreLabel=QtWidgets.QLabel("High Score: %d" % (self.highScore))
        self.highScoreLabel.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        self.highScoreLabel.setAlignment(QtCore.Qt.AlignTop)

        self.scoreBox=QtWidgets.QHBoxLayout()
        self.scoreBox.addWidget(self.scoreLabel)
        self.scoreBox.addStretch(1)
        self.scoreBox.addWidget(self.highScoreLabel)
        
        self.banglaLabel=QtWidgets.QLabel("Bangla")
        self.banglaLabel.setFont(QtGui.QFont("Times", 220))#, QtGui.QFont.Bold))
        #self.banglaLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.banglaLabel.setAlignment(QtCore.Qt.AlignCenter)
        #self.banglaLabel.setAlignment(QtCore.Qt.AlignTop)
        
        self.buttonGroup=QtWidgets.QButtonGroup()
        self.buttonGroup.setExclusive(True)
        self.aButton=QtWidgets.QPushButton("a")
        self.bButton=QtWidgets.QPushButton("b")
        self.cButton=QtWidgets.QPushButton("c")
        self.dButton=QtWidgets.QPushButton("d")
        self.buttonGroup.addButton(self.aButton)
        self.buttonGroup.addButton(self.bButton)
        self.buttonGroup.addButton(self.cButton)
        self.buttonGroup.addButton(self.dButton)
        self.buttonGroup.setId(self.aButton, 0)
        self.buttonGroup.setId(self.bButton, 1)
        self.buttonGroup.setId(self.cButton, 2)
        self.buttonGroup.setId(self.dButton, 3)
        self.buttonGroup.buttonClicked[QtWidgets.QAbstractButton].connect(self.letterChosen)

        self.hbox=QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.aButton)
        self.hbox.addWidget(self.bButton)
        self.hbox.addWidget(self.cButton)
        self.hbox.addWidget(self.dButton)

        self.vbox=QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.scoreBox)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.banglaLabel)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.setWindowTitle("Bengali Letters Quiz")
        self.setLayout(self.vbox)
        self.setGeometry(10, 10, 640, 640)

        self.chooseLetters()
        self.show()
        
        
    def letterChosen(self, button):
        chosen=self.buttonGroup.id(button)
        if chosen == self.answerButtonIndex:
            self.score=self.score+1
        else:
            if self.score > self.highScore:
                self.highScore=self.score
            self.score=0
        self.scoreLabel.setText("Score: %d" % (self.score))
        self.scoreLabel.repaint()
        self.highScoreLabel.setText("High Score: %d" % (self.highScore))
        self.highScoreLabel.repaint()
        self.chooseLetters()
        
        
    def chooseLetters(self):
        usedLetterIndices=[]
        usedButtons=[]
        self.answerIndex=np.random.randint(0, len(letters))
        self.banglaLabel.setText(letters[self.answerIndex][1])
        self.answerButtonIndex=np.random.randint(0, len(self.buttonGroup.buttons()))
        self.buttonGroup.buttons()[self.answerButtonIndex].setText(letters[self.answerIndex][0])
        usedButtons.append(self.answerButtonIndex)
        usedLetterIndices.append(self.answerIndex)
        buttonIndex=0
        while len(usedButtons) < len(self.buttonGroup.buttons()):
            if buttonIndex in usedButtons:
                buttonIndex=buttonIndex+1
            else:
                letterIndex=-1
                while letterIndex not in usedLetterIndices:
                    letterIndex=np.random.randint(0, len(letters))
                    if letterIndex not in usedLetterIndices:
                        usedLetterIndices.append(letterIndex)
                        self.buttonGroup.buttons()[buttonIndex].setText(letters[letterIndex][0])
                        usedButtons.append(buttonIndex)
