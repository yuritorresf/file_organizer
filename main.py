from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget
import os, sys
import time

class Organizer:

    def __init__(self):
        # self.__folder_loc = input('Enter folder location: ')
        self.__folders = []
        self.__type = []

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = uic.loadUi('file_organizer.ui')

        self.window.show()

        self.window.search_button.clicked.connect(self.action)

        self.app.exec()
        
    def action(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.window.input_text.setText(path)
        for file in os.listdir(path):
            self.window.list_filesfolders.addItem(str(file))

    def files(self):
        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1] not in self.__type:
                    self.__type.append(file.split('.')[-1])

            if not os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file not in self.__folders:
                    self.__folders.append(file)

    def create_files(self):
        for file in self.__type:
            if not os.path.exists(os.path.join(self.__folder_loc, file)):
                os.makedirs(os.path.join(self.__folder_loc, file))
                print('Created folder: ' + file)

    def move_files(self):
        d=0
        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1] in self.__type:
                    os.rename(os.path.join(self.__folder_loc, file), os.path.join(self.__folder_loc, file.split('.')[-1], file))
                    print('Moved file: ' + file)
                    d+=1
                    print(f'{d/100}')


def main():
    organizer = Organizer()
    #organizer.files()
    #organizer.create_files()
    #organizer.move_files()
    #print('Done!')
    input('Press enter to exit...')
    #exit()
    
    # os.listdir("C:/Users/ASCOM/").__len__()

if __name__ == '__main__':
    main()