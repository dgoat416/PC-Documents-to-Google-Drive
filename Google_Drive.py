from Set_Up_Google_Drive import get_credentials
from googleapiclient.discovery import build
import os


class GoogleDrive:

    # google drive instance
    drive_service = None

    # google docs instance
    docs_service = None

    # google sheets instance
    sheets_service = None

    # google slides instance
    slides_service = None

    # credentials
    creds = None

    # Default Constructor
    def __init__(self):
        self.creds = get_credentials()
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.doc_service = build('docs', 'v1', credentials=self.creds)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)

    # Method to add a file to the root folder of google drive
    def add_file_to_drive(self, path, fileName):
        file_id = self.drive_service.upload_file('Test1IMG', 'C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg',
                                                "root", mime_type='image/jpeg')
        return

    # Method to add folder to the root folder of google drive
    def add_folder_to_drive(self, path, filename):
        pass

    # Method to get all the new & updated files from documents folder and place them in google drive
    def pc_to_cloud(self, path):
        # get the documents directory
        print(os.listdir(path))
        print(os.scandir(path))
        documents_dir = os.listdir(path)

        files = []
        folders = []
        for index in range(0, len(documents_dir)):
            # get the folder/file name
            element = documents_dir[index]

            # don't worry about files/folders that start with '.'
            if element[0] != '.':
                continue
            # is folder?
            elif os.path.isdir(os.path.join(path, element)):
                #process as a folder
                # add to google drive if not there or if the windows version has a later date than the google docs version
                pass
            # is file?
            elif os.path.isfile(os.path.join(path, element)):
                # process as a file
                # add to google drive if not there or if the windows version has a later date than the google docs version
                pass

            print(os.path.join(path, element))
            print(element)


google_object = GoogleDrive()
google_object.pc_to_cloud(r"C:\Users\HP\Documents")