from PyQt5 import QtWidgets,QtGui,QtCore
import math

#prozor
SIRINA=1200
VISINA=700
#sunce
PRECNIK=20
MASA=1.98892*10**30 

#konstante
AU=149.6e6*1000 #rastojanje od zemlje do sunca u metrima
G=6.67428e-11 #gravitaciona konstanta
SCALE=100/AU #1AU=100px
DAN=60*60*24 #dan u sekundama

class Kometa:
    def __init__(self,x,y,precnik,masa):
        self.x=x
        self.y=y
        self.precnik=precnik
        self.masa=masa

        self.orbit=[]
        self.rastojanje=0
        self.x_brzina=0
        self.y_brzina=0
        self.brzina=0
        self.dan=0

    def draw(self,qp):
        if(len(self.orbit))>2:
            koordinate=[]
            for tacka in self.orbit:
                x,y=tacka
                x=x*SCALE+SIRINA/2
                y=y*SCALE+VISINA/2
                koordinate.append((x,y))
            pen=QtGui.QPen(QtCore.Qt.white,2)
            qp.setPen(pen)
            for i in range(len(koordinate)-1):
                qp.drawLine(QtCore.QPoint(*koordinate[i]),QtCore.QPoint(*koordinate[i+1]))
        
        pen=QtGui.QPen(QtCore.Qt.white,2)
        qp.setPen(pen)
        qp.setFont(QtGui.QFont('Arial',24))
        A=round(self.rastojanje/AU,1)
        qp.drawText(100,100,f'rasojanje od Sunca:{self.rastojanje} km ({A}AU)')
        qp.drawText(100,150,f'brzina:{self.brzina} km/h')
        qp.drawText(100,200,f'dan:{self.dan}')

        x=self.x*SCALE+SIRINA/2
        y=self.y*SCALE+VISINA/2
        color=QtGui.QColor(250,250,250)
        qp.setBrush(color)
        qp.drawEllipse(x-self.precnik,y-self.precnik,2*self.precnik,2*self.precnik)

    def pozicija(self):
        other_x,other_y = 0,0 
        distance_x = other_x-self.x
        distance_y = other_y-self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = G*self.masa*MASA/distance**2 #F=GmM/r^2
        ugao = math.atan2(distance_y, distance_x) #ugao=arctg(y/x)
        force_x = math.cos(ugao)*force
        force_y = math.sin(ugao)*force
        
        self.x_brzina += (force_x/self.masa)*DAN #v=v0+at=v0+(F/m)*t
        self.y_brzina += (force_y/self.masa)*DAN

        self.x += self.x_brzina*DAN #s=vt
        self.y += self.y_brzina*DAN
        self.orbit.append((self.x,self.y))
        self.rastojanje=round(math.sqrt(self.x**2+self.y**2),1)
        self.brzina=round(math.sqrt(self.x_brzina**2+self.y_brzina**2)*3.6,1)

kometa=Kometa(5*AU,0,3,1000000)
kometa.y_brzina=-5000 #m/s(20000km/h)

class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initGui()
        self.show()

    def initGui(self):
        self.setGeometry(100,100,SIRINA,VISINA)
        self.setWindowTitle('KOMETA')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(1000/60) #60fps

    def update_positions(self):
        kometa.pozicija()
        kometa.dan+=1
        self.update()

    def paintEvent(self,e):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.fillRect(self.rect(),QtGui.QColor(0,0,0)) #pozadina
        self.sunce(qp)
        kometa.draw(qp)
        qp.end()

    def sunce(self,qp):
        color=QtGui.QColor(250,250,0)
        qp.setBrush(color)
        qp.drawEllipse(SIRINA/2-PRECNIK,VISINA/2-PRECNIK,2*PRECNIK,2*PRECNIK)

app=QtWidgets.QApplication([])
window=Gui()
app.exec_()
