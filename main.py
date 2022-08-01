from genericpath import isfile
import os

class Organizer:

    def __init__(self):
        self.__folder_loc = input('Enter folder location: ')
        self.__folders = []
        self.__type = []
    
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
        for file in os.listdir(self.__folder_loc):
            if os.path.isfile(os.path.join(self.__folder_loc, file)):
                if file.split('.')[-1] in self.__type:
                    os.rename(os.path.join(self.__folder_loc, file), os.path.join(self.__folder_loc, file.split('.')[-1], file))
                    print('Moved file: ' + file)

def main():
    organizer = Organizer()
    organizer.files()
    organizer.create_files()
    organizer.move_files()
    print('Done!')
    input('Press enter to exit...')
    exit()

if __name__ == '__main__':
    main()