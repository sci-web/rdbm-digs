import sys, getopt, os

def main(argv):
  this_path = os.path.dirname(sys.argv[0])
  this_path = this_path + "/" if this_path != "" else this_path
  print this_path
  # print this_path
  SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.appdata']
  SERVICE_ACCOUNT_FILE = this_path + 'service.json'
  UPLOADS_INFO = this_path + 'uploads_and_permissions.json'
  print SERVICE_ACCOUNT_FILE

if __name__ == '__main__':
  main(sys.argv[1:])
