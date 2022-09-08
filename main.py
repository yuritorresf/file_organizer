from PyQt5 import uic, QtWidgets, QtCore, QtGui
import os, sys, time
from pathlib import Path

class Organizer:

    def __init__(self):
        self.__folder_loc = ''
        self.__folders = []
        self.__type = []
        self.__counter_actions = 0

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = uic.loadUi('file_organizer.ui')

        self.window.show()

        self.window.closeEvent = self.closeEvent
        QtWidgets.QMessageBox.about(self.window, "Seja bem-vindo ao File Organizer", "Antes de começar a organizar seus arquivos, certifique-se de que você está na pasta que deseja organizar.")
        self.window.search_button.clicked.connect(self.action)
        self.window.organizer_button.clicked.connect(self.start)
        if self.window.input_text.text() == '':
            self.window.search_button.setText('Buscar')
            self.window.organizer_button.setEnabled(False)

        sys.exit(self.app.exec())

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self.window, "Encerrar", "Tem certeza que deseja finalizar o programa?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if close == QtWidgets.QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def action(self):

        if self.window.input_text.text() == '':
            path = str(QtWidgets.QFileDialog.getExistingDirectory(self.window, 'Selecione a pasta que deseja organizar', str(Path.home())))
        else:
            path = self.window.input_text.text()
            self.window.search_button.setText('Selecionar')
        
        self.window.organizer_button.setEnabled(True)
        self.window.input_text.setText(path)
        self.__folder_loc = path
        self.window.list_filesfolders.clear()
        self.window.progress_bar.setValue(0)
        self.__folders = []
        self.__type = []
        self.__counter_actions = 0
    
    def start(self):
        proceder = QtWidgets.QMessageBox.question(self.window, "Iniciar organizaçao", "Tem certeza que deseja iniciar a organização?\n\nEsta ação não pode ser desfeita. Não feche o programa enquanto a organização estiver em andamento.", )
        
        if proceder == QtWidgets.QMessageBox.StandardButton.Yes:
            self.files()
            self.action_files()
            time.sleep(1)
            QtWidgets.QMessageBox.about(self.window, 'Sucesso', 'Arquivos organizados com sucesso!')
            self.window.search_button.setEnabled(True)
            self.window.organizer_button.setEnabled(False)
            self.window.progress_bar.setValue(0)

    def files(self):
        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1].lower() not in self.__type:
                    self.__type.append(file.split('.')[-1])

            if not os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file not in self.__folders:
                    self.__folders.append(file)    

    def action_files(self):

        self.window.search_button.setEnabled(False)
        self.window.organizer_button.setEnabled(False)

        d=0
        p=0

        dprint = '\nListando pasta e examinando as extensões dos arquivos...\n'
        self.window.list_filesfolders.setText(dprint)
        self.window.list_filesfolders.verticalScrollBar().setValue(1000)

        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1].lower() in self.__type:
                    self.__counter_actions += 1
        
        dprint += '\n{} arquivos encontrados.\n'.format(len(os.listdir(self.__folder_loc)))
        self.window.list_filesfolders.setText(dprint)
        self.window.list_filesfolders.verticalScrollBar().setValue(1000)

        dprint += '\nCriando pastas...\n'
        self.window.list_filesfolders.setText(dprint)
        self.window.list_filesfolders.verticalScrollBar().setValue(1000)

        for file in self.__type:
            if not os.path.exists(os.path.join(self.__folder_loc, file)):
                os.makedirs(os.path.join(self.__folder_loc, file))
                dprint+='Pasta {} criada.\n'.format(file)
                self.window.list_filesfolders.setText(dprint)
                p+=1

        dprint += '\nMovendo arquivos...\n'
        self.window.list_filesfolders.setText(dprint)
        self.window.list_filesfolders.verticalScrollBar().setValue(1000)
        
        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1].lower() in self.__type:
                    
                    # criar condição para renomear arquivos com mesmo nome
                    if os.path.exists(os.path.join(self.__folder_loc, file.split('.')[-1], file)):
                        os.rename(os.path.join(self.__folder_loc, file), os.path.join(self.__folder_loc, file.split('.')[-1], file.split('.')[0] + ' - copia' + '.' + file.split('.')[-1]))
                    else:
                        os.rename(os.path.join(self.__folder_loc, file), os.path.join(self.__folder_loc, file.split('.')[-1], file))
                    
                    d+=1
                    data = (d/self.__counter_actions)*100

                    dprint += 'Arquivo {} movido.\n'.format(file)
                    self.window.list_filesfolders.setText(dprint)
                    self.window.list_filesfolders.verticalScrollBar().setValue(1000)

                self.window.progress_bar.setValue(int(data))
        
        fp = ''
        fd = ''

        if p == 0:
            fp = 'Todas as pastas já existem'
        elif p == 1:
            fp = '{} pasta foi criada'.format(p)
        else:
            fp = '{} pastas foram criadas'.format(p)
        if d == 0:
            fd = 'nenhum arquivo foi movido'
        else:
            fd = '{} arquivos foram movidos'.format(d)
        
        dprint += '\n{fp} e {fd}.\n\nFeito...\n'.format(fp=fp, fd=fd)
        self.window.list_filesfolders.setText(dprint)
        self.window.list_filesfolders.verticalScrollBar().setValue(1000)

def main():
    Organizer()

if __name__ == '__main__':
    main()