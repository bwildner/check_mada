# Check_Mada
# von Bernd Wildner 11-2017

# Python 2.7 und PYQT4

# Eingaber der Maschinennummer
# Die Zwischenablage wird uebernommen
# Suchen der NCSerienIBN der Maschine
# Pruefen ob 17400 (SW Version) enthalten und Ausgabe der Daten 
# Bei mehreren NCSerienIBN, werden alle ausgegeben 

import os
import sys
from PyQt4 import uic 
from PyQt4.QtGui import QWidget, QMainWindow, QVBoxLayout, QTextEdit, QMessageBox, QApplication


 
form_class = uic.loadUiType("mnummer_gui.ui")[0]                 # Load the UI



def search2(path, extension):
    """
        sucht alle Dateien in path mit der angegebenen extension
        extension with leading point, for example: ".png"
        Rueckgabe ist eine Liste der Dateien mit Pfadangabe
    """
    for root, dirs, filenames in os.walk(path): 
        for filename in filenames:
            if os.path.splitext(filename)[-1] == extension:
                yield os.path.join(root, filename)
           
                    
           
class AusgabefensterClass(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)
        self.edit = QTextEdit()
        layout.addWidget(self.edit)
        
  
        
                 
class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.button_eingabe.clicked.connect(self.eingabe_clicked) #Button oder Enter schliesst die Eingabe ab
        self.mnummer_textfeld.returnPressed.connect(self.eingabe_clicked)  # Bind the event handlers
               
        
    def eingabe_clicked(self):                  #  button event handler
        eingabe = str(self.mnummer_textfeld.text())
        
        #pruefen der eingabe und Fehlermeldung wenn noetig
        if not eingabe.isdigit() or len(eingabe)<>5:
            QMessageBox.warning(self, "Eingabefehler","Bitte die MNummer 5stellig eingeben.",QMessageBox.Cancel, QMessageBox.NoButton,QMessageBox.NoButton)
            return
        
        #Pfad zusammenbauen 
        ordner = "e:\\M"
        verzeichnis = ordner + eingabe
        
        result = list(search2(verzeichnis, '.arc')) #Alle .arc Dateien im betreffenden Verz suchen
        
        i = 0
        anzahl17400 =0
        #Alle Dateien mit .arc nach 17400 durchsuchen
        while i < len(result):
            with open(result[i],'r') as myfile:
                inhalt = myfile.read()
                startpos = inhalt.find ('17400') #Position von 17400 im File
                if startpos > 0:
                    endpos = inhalt.find('17500', startpos) #Position von 17500 im File
                    #Text zwischen 17400 und 17500 im Ausgabefenster anzeigen
                    ausgabefenster.edit.append(result[i])
                    ausgabefenster.edit.append(inhalt[startpos-1:endpos-1])
                    anzahl17400=anzahl17400+1 #zaehler fuer fenstergroesse
            i=i+1
        self.close() #Dateien schliessen
        
        if len(result) ==0:
            QMessageBox.warning(self, "Ergebnis","Keine Dateien mit 17400 gefunden", QMessageBox.Cancel, QMessageBox.NoButton, QMessageBox.NoButton)
        
        myWindow.destroy()
        ausgabefenster.setGeometry(100,100,500,anzahl17400*100+20)
        ausgabefenster.show()

           
 
 
app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
ausgabefenster = AusgabefensterClass()
zwischenablage = str(QApplication.clipboard().text())
if len(zwischenablage) >5:
    print ("Hallo")
    
myWindow.mnummer_textfeld.setText(QApplication.clipboard().text())
myWindow.show()
app.exec_()

"""
    \\heller.biz\hnt\ControlArch-MNo\M55xxx\ARCHIVE-M55022\Backups\Series-Start-up
    
    \\Heller.biz\hnt\Steuerungstechnik\Projects-Machines\M-Numbers\M55xxx\M55022-H-5000-AAM-Silao-Guanajuato-MX
    
    \\heller.biz\hnt\ControlArch-MNo\M52xxx\ARCHIVE-M52009\DataMovement-2014-12-24
"""
