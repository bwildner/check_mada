# Check_Mada
# von Bernd Wildner 11-2017

# Python 2.7 und PYQT4

# Eingaber der Maschinennummer
# Die Zwischenablage wird uebernommen
# Suchen der NCSerienIBN der Maschine
# Pruefen ob 17400 (SW Version) enthalten und Ausgabe der Daten 
# Bei mehreren NCSerienIBN, werden alle ausgegeben 
# Eingabe von 3 Maschinendaten moeglich

import os
import sys
from PyQt4 import uic 
from PyQt4.QtGui import QWidget, QMainWindow, QVBoxLayout, QTextEdit, QMessageBox, QApplication
from test.test_pep277 import filenames
from time import clock, ctime
import logging
import codecs
import locale



 
form_class = uic.loadUiType("mnummer_gui.ui")[0]                 # Load the UI



logging.basicConfig(filename="check_mada.log",level = logging.DEBUG,format = "%(asctime)s [%(levelname)-8s] %(message)s")

 
logging.info("****************Start Logging****************")


def searchfiles(path, extension):
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
        
        if self.checkBox17400.checkState() ==2:
            search17400=True
        else:
            search17400=False
            
            
        if len(self.mada1.text())>0:
            searchMada=True
        else:
            searchMada=False
            
            
        logging.debug( "17400: " + str(search17400))
        logging.debug("Mada: " + str(searchMada))
        
        
        #pruefen der eingabe und Fehlermeldung wenn noetig
        if not eingabe.isdigit() or len(eingabe)<>5:
            QMessageBox.warning(self, "Eingabefehler","Bitte die MNummer 5stellig eingeben.",QMessageBox.Cancel, QMessageBox.NoButton,QMessageBox.NoButton)
            return
    
    
#        \\heller.biz\hnt\ControlArch-MNo\M55xxx\ARCHIVE-M55022\Backups\Series-Start-up
    
#   \\Heller.biz\hnt\Steuerungstechnik\Projects-Machines\M-Numbers\M55xxx\M55022-H-5000-AAM-Silao-Guanajuato-MX
#  \\heller.biz\hnt\ControlArch-MNo\M52xxx\ARCHIVE-M52009\DataMovement-2014-12-24

        #Pfad zusammenbauen 
        #ordner = "e:\\M"
        #ordner="//N0204/Dateien/" #zuhause
        #bei heller ordner="//heller.biz/hnt/ControlArch-MNo/"
        ordner="//heller.biz/hnt/ControlArch-MNo/"
        
        
        verzeichnis = ordner+"M"+eingabe[0:2]+"xxx/ARCHIVE-M"+eingabe
        #verzeichnis ="d:\\M"+eingabe
        logging.debug(str( verzeichnis))
        t1= clock()        
        result = list(searchfiles(verzeichnis, '.arc')) #Alle .arc Dateien im betreffenden Verz suchen
        logging.info("Dateien suchen: " +str( (clock()-t1)))
        laengedateiname1=0
        laengedateiname2=0
        
        i = 0 #zaehler fuer dateien
        anzahl17400 =0 #zaehler fuer fenstergroesse
        anzahlmada=0
        #Alle Dateien mit .arc nach 17400 durchsuchen
        t1= clock() 
        while i < len(result):
            with open(result[i],'r') as myfile:
                
                t2=clock()
                #Kontrolle ob ;nckcomp in den ersten 1000byte steht
                inhalt1 = myfile.read(1000)
                logging.info(str(i)+str(myfile.name) + " Datei einlesen zur Headerkontrolle")
                #logging.info(str(i)+str(myfile.name) + " Datei einlesen zur Headerkontrolle"+ str((clock()-t2)))
                
                if (inhalt1.find(";NCKComp",1,1000) or inhalt1.find("CFG_GLOBAL.INI",1,1000))>0: #Nckcomp vorhanden dann komplett einlesen und 17400 suchen
                    logging.info("NCKComp vorhanden, weiter auswerten")
                    t3=clock()
                    inhalt = myfile.read()
                    #logging.info( str(i)+ " Nur Datei komplett einlesen ohne durchsuchen: " +str((clock()-t3)))
                    if search17400 == True:
                        
                        FileEncoding = "ISO-8859-15"
                        IN_File = codecs.open(result[i], 'r', FileEncoding).read()
                        startpos = IN_File.find ('17400') #Position von 17400 im File ermitteln
                        
                        #startpos = inhalt.find ('17400') #Position von 17400 im File ermitteln
                        
                        logging.info("Position 17400: "+str(startpos))
                        
                        if startpos > 0:
                            endpos = IN_File.find('17500', startpos) #Position von 17500 im File ermitteln
                            #endpos = inhalt.find('17500', startpos) #Position von 17500 im File ermitteln
                            
                            #Text zwischen 17400 und 17500 im Ausgabefenster anzeigen
                            ausgabefenster.edit.append("Dateiname:\n "+ result[i] + "\n Datum: "+ ctime(os.path.getmtime(result[i])))
                            
                            if len(result[i])>laengedateiname1:
                                laengedateiname1= len(result[i])
                                                  
                            #ausgabefenster.edit.append(inhalt[startpos-1:endpos-1])
                            ausgabefenster.edit.append(IN_File[startpos-1:endpos-1])
                            
                            
                            anzahl17400=anzahl17400+1 
                            #logging.info(str(i)+" Datei nach 17400 durchsuchen: " +str((clock()-t3))+" und bisherige Gesamtzeit: "+str( (clock()-t1)))
                        else:
                            ausgabefenster.edit.append("Dateiname:\n "+ result[i] + "\n Datum: "+ ctime(os.path.getmtime(result[i])))
                            ausgabefenster.edit.append("FEHLER DATEI kann nicht durchsucht werden!!!!!!\n\n")
                            
                             
                    if searchMada == True:
                        logging.info("searchMada Schleife")
                        ausgabefenster2.edit.append("\n\nDateiname:\n "+ result[i] + "\n Datum: "+ ctime(os.path.getmtime(result[i])))
                            
                        filezeiger=0
                        while inhalt.find (self.mada1.text(), filezeiger)>0:
                            startpos = inhalt.find (self.mada1.text(), filezeiger) #Position von mada1 im File ermitteln
                            logging.info("Mada gefunden an: "+str(startpos))
                            if startpos > 0:
                                endpos = inhalt.find('\n', startpos) #Zeilenende ermitteln
                                #Text zwischen 17400 und 17500 im Ausgabefenster anzeigen
                                
                                ausgabefenster2.edit.append(inhalt[startpos-1:endpos])
                                if len(result[i])>laengedateiname2:
                                    laengedateiname2= len(result[i])
                            
                                anzahlmada=anzahlmada+1 
                                filezeiger=endpos
                                logging.info(str( i)+ " Datei nach Mada durchsuchen: " +str((clock()-t3))+" und bisherige Gesamtzeit: "+str((clock()-t1)))
                    
            i=i+1
            myfile.close() #Dateien schliessen
        
        if len(result) ==0:
            QMessageBox.warning(self, "Ergebnis","Keine Dateien mit diesen Daten gefunden", QMessageBox.Cancel, QMessageBox.NoButton, QMessageBox.NoButton)
        else:
            if search17400==True:
                ausgabefenster.setGeometry(50,50,laengedateiname1*6+100,anzahl17400*130+20)
                ausgabefenster.show()
                
            if searchMada==True:
                if filezeiger==0:
                    QMessageBox.warning(self, "Ergebnis","Keine Dateien mit Madatum "+self.mada1.text()+ " gefunden", QMessageBox.Cancel, QMessageBox.NoButton, QMessageBox.NoButton)    
                else:
                    ausgabefenster2.setGeometry(500,50,laengedateiname2*6+100,anzahlmada*100)
                    ausgabefenster2.show()
        
            
        myWindow.close()

        
        logging.info(str( i)+ " Dateien durchsuchen: " +str( (clock()-t1)))
        
        
           
 
 
app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
ausgabefenster = AusgabefensterClass()
ausgabefenster.setWindowTitle("Ergebnisse 17400")
ausgabefenster2 = AusgabefensterClass()
ausgabefenster2.setWindowTitle("Ergebnisse Maschinendaten")

#zwischenablage auslesen, pruefen und in das Textfeld kopieren
zwischenablage = str(QApplication.clipboard().text())
if len(zwischenablage) >5:
    QApplication.clipboard().setText("")
myWindow.mnummer_textfeld.setText(QApplication.clipboard().text())


myWindow.show()


app.exec_()

"""
    \\heller.biz\hnt\ControlArch-MNo\M55xxx\ARCHIVE-M55022\Backups\Series-Start-up
    
    \\Heller.biz\hnt\Steuerungstechnik\Projects-Machines\M-Numbers\M55xxx\M55022-H-5000-AAM-Silao-Guanajuato-MX
    
    \\heller.biz\hnt\ControlArch-MNo\M52xxx\ARCHIVE-M52009\DataMovement-2014-12-24
"""
