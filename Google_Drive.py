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

    # # uploads a file to the root folder of the google drive
    # file_id = deprecated_drive_service.upload_file('Test1IMG', 'C:\\Users\\HP\\Documents\\AI Frames\\TW3.jpg', "root",
    #                                  mime_type='image/jpeg')
    #
    # print(file_id)

    # Method to return all folders from google drive except for those in the ignore_list
    def get_all_folders_from_root(self, ignore_list=None):
        # list all folders in google drive and return a list
        folders_from_drive = self.drive_service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and parents in 'root' and trashed = false",
            spaces='drive',
            fields='nextPageToken, files(id, name, modifiedTime, mimeType, shared)',
            orderBy='folder, name'
        ).execute().get('files', [])

        # get all files except files in ignore_list
        folders_from_drive = self.ignore_items(folders_from_drive, ignore_list)

        return folders_from_drive

    # Method to ignore items that are in ignore_list
    def ignore_items(self, folders, ignore_list=None):
        num_of_folders = len(folders)
        i = 0

        # nothing to ignore
        if ignore_list is None:
            return folders

        # delete files in ignore_list from folders
        while i < num_of_folders:
            if folders[i]['name'] in ignore_list:
                del folders[i]
                num_of_folders = len(folders)
            i += 1
        return folders

    # # Method to get all files from root directory of Google Drive
    # def get_all_files_from_root(self):
    #     # list all files that are in root directory and haven't been trashed
    #     files_in_root = self.drive_service.files().list(
    #         q="mimeType!='application/vnd.google-apps.folder' and parents in 'root' and trashed = false",
    #         spaces='drive',
    #         fields='nextPageToken, files(id, name, modifiedTime, mimeType, shared)',
    #         orderBy='folder, name'
    #     ).execute().get('files', [])
    #
    #     return files_in_root

    # returns a list of files from the specified folder id
    def list_folders_from_folder_id(self, folder_id, ignore_list=None):
        foldersList = []

        # flag to inform us of whether there is another page or not
        page_token = None
        while True:
            # list all folders within the specified folder_id and haven't been trashed
            folders = self.drive_service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and '" + folder_id + "' in parents and trashed = false",
                spaces='drive',
                fields='nextPageToken, files(id, name, modifiedTime, mimeType, shared)',
                orderBy='folder, name',
                pageToken=page_token
            ).execute()

            # get the next page token
            page_token = folders.get('nextPageToken', None)

            # get all folders except folders in ignore_list
            folders = folders.get('files', [])
            folders = self.ignore_items(folders, ignore_list)

            # add folders to list
            foldersList.extend(folders)

            # if no next page then break
            if page_token is None:
                break

 

        return foldersList

    # returns a list of files from the specified folder id
    def list_files_from_folder_id(self, folder_id, ignore_list=None):
        filesList = []

        # flag to inform us of whether there is another page or not
        page_token = None
        while True:
            # list all files within the specified folder_id and haven't been trashed
            files = self.drive_service.files().list(
                q="mimeType!='application/vnd.google-apps.folder' and '" + folder_id + "' in parents and trashed = false",
                spaces='drive',
                fields='nextPageToken, files(id, name, modifiedTime, mimeType, shared)',
                orderBy='folder, name',
                pageToken=page_token
            ).execute()

            # get the next page token
            page_token = files.get('nextPageToken', None)

            # get all files except files in ignore_list
            files = files.get('files', [])
            files = self.ignore_items(files, ignore_list)

            # add files to list
            filesList.extend(files)

            # if no next page then break
            if page_token is None:
                break

        return filesList

    # 1. get all folders from google drive root and then loop through each folder and grab all files and add those to list
    # 2. get all files from google drive root and then add those to list
    def get_all_items_in_drive(self, ignore_list=None):
        # returns all folders from google drive except the ones found in ignore_list
        folders = self.get_all_folders_from_google_drive(ignore_list)

        # holds all the files within the folders
        files = []

        # get all files in root
        files.extend(self.list_files_from_folder_id('root'))

        # loop through folder and get all the files
        for folder in folders:
            files.extend(self.list_files_from_folder_id(folder['id']))

        return files

    # def get_all_items_in_drive(self):
    #     gotFolders = True
    #     foldersList = []
    #     filesList = []
    #     folder_id = 'root'
    #     while gotFolders is True:
    #         foldersList.extend(self.list_folders_from_folder_id(folder_id))
    #         if len(foldersList) == 0:
    #             gotFolders = False
    #             continue
    #         else:
    #             filesList.extend(self.list_files_from_folder_id(folder_id))
    #             folder_id = foldersList[0]['id']
    #             foldersList.pop(0)
    #
    #     return filesList
    #
    #     #
    #     # items = self.drive_service.files().list(
    #     #     # q="'" + folder_id + "' in parents",
    #     #     q="'root' in parents and trashed=false",
    #     #     spaces='drive',
    #     #     fields='nextPageToken, files(id, name, modifiedTime, mimeType, shared)',
    #     #     orderBy='folder, name'
    #     #     # page_token=page_token
    #     #     # trashed = False
    #     # ).execute().get('files', [])

    # Method to get all the new & updated files from documents folder and place them in google drive
    def pc_to_cloud(self, path, list=None):
        # get the documents directory
        print(os.listdir(path))
        print(os.scandir(path))
        pc_dir = os.listdir(path)

        files = []
        folders = []
        for index in range(0, len(pc_dir)):
            # get the folder/file name & create a path variable
            pc_element = pc_dir[index]
            pc_element_path = os.path.join(path, pc_element)

            # don't worry about files/folders that start with '.'
            if pc_element[0] == '.':
                continue
            # is folder?
            elif os.path.isdir(pc_element_path):
                # process as a folder
                # add to google drive if not there or if the windows version has a later date than the google drive version
                pc_folder = pc_element
                driveFolders = []
                driveFolders = google_object.list_folders_from_folder_id('root', list)
                # driveFiles = google_object.get_all_items_in_drive(list)

                #
                if pc_folder in driveFolders['name']:
                    # add to google drive if the windows version has a later date than the google docs version
                    pass
                else:
                    # add to google drive
                    pass


                # for document in 
                # page_token = None
                # while True:
                #     # response = self.drive_service.files().list(
                #     #                                            # driveId="root",
                #     #                                            # corpora="user",
                #     #                                            # q="mimeType='application/vnd.google-apps.folder'",
                #     #                                            # spaces='drive',
                #     #                                            # fields='nextPageToken, files(id, name)',
                #     #                                            # pageToken=page_token)
                #     #     q='root'
                #     # ).execute()
                #
                #     param = {}
                #
                #     if page_token:
                #         param['pageToken'] = page_token
                #     children = self.drive_service.folders().list(folderId="root", **param).execute()
                #     for i in range(0, len(children)):
                #         print(children[i])

                    # for child in children.get('items', []):
                    #     result.append(drive_get_file(child['id']))
                    #
                    # page_token = children.get('nextPageToken')
                    # if not page_token:
                    #     break

                    # for file in response.get('files', []):
                    #     # Process change
                    #     print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    # page_token = response.get('nextPageToken', None)
                    # if page_token is None:
                    #     break
                pass
            # is file?
            elif os.path.isfile(pc_element_path):
                # process as a file
                # add to google drive if not there or if the windows version has a later date than the google docs version
                pass

            print(os.path.join(path, element))
            print(element)


# DGOAT currently on line 53
list = ["G:"]
google_object = GoogleDrive()
google_object.pc_to_cloud('C:\\Users\\HP\\Documents\\', list)
# children = google_object.drive_service.files().list().execute()
# for i in range(0, len(children)):
#     print(children[i])

# # View all folders and file in your Google Drive
# fileList = google_object.drive_service.files().list().execute()
# for file in fileList:
#   print('Title: %s, ID: %s' % (file['title'], file['id']))

# x = google_object.list_files_from_folder_id('root')

# fileList = google_object.list_files_from_folder_id('root')
# fileList = google_object.list_folders_from_folder_id('root')

# read in the last time we ran this file and if the date of the folder/files is newer than last time

# list = ["G:"]
# filesList = google_object.get_all_items_in_drive(list)

# # list = ["G:"]
# folders = google_object.list_folders_from_folder_id('root')
# folders = google_object.ignore_items(folders, list)
#
# files = []
# files2 = []
# for folder in folders:
#     files.extend(google_object.list_files_from_folder_id(folder['id']))
#
# files.extend(google_object.get_all_files_from_root())

for file in filesList:
    print(file['name'])
