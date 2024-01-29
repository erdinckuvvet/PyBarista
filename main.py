import random
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import pandas as pd

#from excel to pandas data frame
df = pd.ExcelFile('coffee.xlsx').parse('Sayfa1')



parameters = {
    "order": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "index": []
}

widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "order": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": [],
    "barCounter": [],
    "hint": []
}

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Barista The Game")
window.setWindowIcon(QtGui.QIcon('icon.png'))
#window.setFixedWidth(900)
#window.setFixedHeight(600)
window.resize(900,600)
window.setStyleSheet("background: '#e0cfab';")
# setting layout
grid = QGridLayout()

def preload_data(index):
    order = df["ORDER"][index]
    correct = df["correct"][index]
    wrong = df["incorrect"][index].split(" ")

    parameters["order"].append(order)
    parameters["correct"].append(correct)

    all_answers = wrong + [correct] #all answer choices have merged in a list
    random.shuffle(all_answers)  # because, we do not want correct answer is in last choice all time
    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])


def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def clear_parameters():
    for param in parameters:
        if parameters[param] != []:
            for i in range(0, len(parameters[param])):
                parameters[param].pop()

    parameters["score"].append(0)
    parameters["index"].append(random.randint(0, 14))

def show_frameStart():
    clear_widgets()
    frameStart()

def start_game():
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    frameMain()

def create_buttons(answer, l_margin, r_margin):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(500) #384
    button.setStyleSheet(
        "*{border: 4px solid '#985a2a';" +
        "color: 'black';" +
        "background: '#e0cfab';"
        "font-family: 'shanti';" +
        "font-size: 16px;" +
        "border-radius: 25px;" +
        "padding: 15px 0;" +
        "margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        "margin-top: 20px;}" +
        "*:hover{background: '#985A2A';" +
        "color: 'black';}"
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):

    if btn.text() == parameters["correct"][-1]:
        # update score
        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        #new question
        parameters["index"].pop()
        parameters["index"].append(random.randint(0,14))
        preload_data(parameters["index"][-1])

        # update score on window
        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["order"][0].setText(parameters["order"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        if parameters["score"][-1] == 100:
            clear_widgets()
            frame_win()

    else:
        clear_widgets()
        frame_fail()

#**********************************
#   START FRAME

def frameStart():
    hint_show = 0
    clear_widgets()
    window.setGeometry(600,50,600,400)
    #logo displaying
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet("margin-top: 50px;")
    widgets["logo"].append(logo)


    # start button widget
    button = QPushButton("PLAY")
    # when the cursor on the button, it's shape will be pointing hand
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#985a2a';" +
        "border-radius: 45px;" +
        "font-size: 28px;" +
        "color: 'black';" +
        "padding: 25px 0;" +
        "margin: 75px 80px;}" +
        "*:hover{background: '#985a2a';" +
        "color: 'white';}"
    )
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    # integrating widgets to layout
    grid.addWidget(widgets["logo"][-1],0,0,1,2)
    grid.addWidget(widgets["button"][-1],1,0,1,2)

#**********************************
#   MAIN FRAME

def frameMain():
    clear_widgets()
    window.setGeometry(500, 50, 900, 800)

    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignCenter)
    score.setStyleSheet(
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 20px 0px;" +
        "margin-top: 20px;" +
        "margin-bottom: 20px;" +
        "margin-right: 20px;" +
        "margin-left: 400px;" +
        "background: '#985a2a';" +
        "border: 1px solid '985a2a';" +
        "border-radius: 40px;"
    )
    widgets["score"].append(score)

    # hint
    hint = QPushButton("Hint")
    hint.setStyleSheet(
        '''*{
            padding: 20px 0px;
            background: '#e0cfab';
            color: 'black';
            border: 1px solid '#985a2a';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 20px ;
            margin-right: 400px;
            margin-left: 20px;
        }
        *:hover{
            background: '#985a2a';
            color: 'white';
        }'''
    )
    hint.clicked.connect(lambda x: hint_function(hint))
    widgets["hint"].append(hint)




    order = QLabel(parameters["order"][-1])
    order.setAlignment(QtCore.Qt.AlignHCenter)
    order.setWordWrap(True)  # bazı sorular uzun olacak
    order.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'black';" +
        "padding: 75px;" +
        "border: 3px solid '985a2a';" +
        "border-radius: 35px;"
    )
    widgets["order"].append(order)

    button1 = create_buttons(parameters["answer1"][-1], 85, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 85)
    button3 = create_buttons(parameters["answer3"][-1], 85, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    # barista counter designed here
    image = QPixmap("barCounter.png")
    barCounter = QLabel()
    barCounter.setPixmap(image)
    barCounter.setAlignment(QtCore.Qt.AlignHCenter)
    widgets["barCounter"].append(barCounter)

    grid.addWidget(widgets["barCounter"][-1], 2, 0, 1, 2 )
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["order"][-1], 1, 0, 1, 2)  # we can also use row column parameters
    grid.addWidget(widgets["answer1"][-1], 3, 0)
    grid.addWidget(widgets["answer2"][-1], 3, 1)
    grid.addWidget(widgets["answer3"][-1], 4, 0)
    grid.addWidget(widgets["answer4"][-1], 4, 1)
    grid.addWidget(widgets["hint"][-1], 0, 0)

#**********************************
#   WIN FRAME
def frame_win():
    #win message
    message = QLabel("Tebrikler! \nMükemmel Bir Baristasın!\n Skorun:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'black'; margin: 75px 5px; padding:20px;"
    )
    widgets["message"].append(message)

    # score
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: 'black'; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # message2
    message2 = QLabel("Önemli olan kahvenin tadı değil onu kiminle içtiğinizdir:)")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'black'; margin-top 0px; margin-bottom: 75px;"
    )
    widgets["message2"].append(message2)

    # button
    button = QPushButton("TEKRAR DENE")
    button.setStyleSheet(
        "*{background:'#e0cfab'; padding:25px 0px; border: 1px solid '#985a2a'; color: 'black';font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#985a2a';}"
    )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frameStart)
    widgets["button"].append(button)

    # logo widget
    pixmap = QPixmap('alt_Logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)

#**********************************
#   FAIL FRAME
def frame_fail():
    #window.resize(400,600)
    # sorry widget
    message = QLabel("Üzgünüm! \nYanlış cevap\n Skorun:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'black'; margin: 75px 5px; padding:20px;"
    )
    widgets["message"].append(message)

    # score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: black; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    # button widget
    button = QPushButton('TEKRAR DENE')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#e0cfab';
            color: 'black';
            border: 1px solid '#985a2a';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#985a2a';
            color: 'white';
        }'''
    )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frameStart)
    widgets["button"].append(button)

    # logo widget
    pixmap = QPixmap('alt_Logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px;"
    )
    widgets["logo"].append(logo)

    # place widgets on the grid
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)


# when user clicked hint button
from PIL import Image
def hint_function(hint):
    im = Image.open('hint.png')
    im.show()
    hint.setEnabled(False)


frameStart()
window.setLayout(grid)

window.show()
sys.exit(app.exec())
