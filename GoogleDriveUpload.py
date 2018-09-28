import sys, getopt, os
from apiclient import errors
from apiclient.http import MediaFileUpload
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from datetime import datetime
from DBsql import DB


def grant_permissions(service, users, file_id):
  def callback(request_id, response, exception):
    if exception:
      print exception
    else:
      print "Permission Id: %s " % response.get('id')
    print "permissions to", file_id, "for", users

  batch = service.new_batch_http_request(callback=callback)
  for email in users:
    user_permission = {
              'type': 'user',
              'role': 'reader',
              'emailAddress': str(email)
    }
    batch.add(service.permissions().create(
                  fileId=file_id,
                  body=user_permission,
                  fields='id',
    ))
  try:
    batch.execute()
  except Exception, e:
    print "An error with granting permissions:", e


def create_folder(service, name, users):

  try:
    folder_metadata = {
        'name': name, # 'Auto_Generated_Reports',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    this_permission = {
        'type': 'domain',
        'domain': 'axpm.com',
        'role': 'reader'
    }    
    folder = service.files().create(body=folder_metadata, fields='id').execute()

    print 'Folder ID: %s' % folder.get('id')
    grant_permissions(service, users, folder.get('id'))
    return folder.get('id')

  except errors.HttpError, error:
      print 'An error creating folder occurred: %s' % error    
   

def upload_file(service, name, title, description, parent_id, mime_type, filename, users):
  """Insert new file.
  Args:
    See in def main() below
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'name': name,
    'title': title,
    'description': description,
    'mimeType': mime_type,
    'parents': [parent_id]
  }

  try:
    # ### need permitions to make it on team_drive:
    # team_drive_metadata = {
    #     'name': 'Report_Uploads',
    #     'mimeType': 'application/vnd.google-apps.folder'
    # }
    # team_drive = service3.teamdrives().create(body=team_drive_metadata, requestId="Report_Uploads_from_DA", fields='id').execute()
    # print 'Team Drive ID: %s' % team_drive.get('id')
    file = service.files().create(body=body,media_body=media_body).execute()
    print 'File ID: %s' % file['id']
    print 'File name: %s' % file['name']
      # ### test common credentials creation (instead of grant_permission())
      # return service3.permissions().create(fileId=id_f, body=new_permission).execute()
      # return service3.permissions().create(fileId=file['id'], body=new_permission).execute() # only if no batch credentials below
    grant_permissions(service, users, file['id'])

    return file['id']

  except errors.HttpError, error:
    print 'An error creating file occurred: %s' % error
    return None


def delete_file(service, file_id, permission_id):
  """Permanently delete a file, skipping the trash.
  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
    service.files().delete(fileId=file_id).execute()
    print file_id, "is deleted!"
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

  if permission_id:
    try:
      service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
    except errors.HttpError, error:
      print 'An error occurred: %s' % error


def print_about(service2, service3):
  """Print information about the user along with the Drive API settings.
  Args:
    service: Drive API service instance.
  """
  try:
    fields = {'fields' : '*'}
    about = service2.about().get().execute()
    print 'Current user name: %s' % about['name']
    print 'Root folder ID: %s' % about['rootFolderId']
    print 'Total quota (bytes): %s' % about['quotaBytesTotal']
    print 'Used quota (bytes): %s' % about['quotaBytesUsed']
    print 'Max Upload sizes(bytes): %s' % about['maxUploadSizes']
    return about['rootFolderId']
    # about = service3.about().get(fields="user, storageQuota").execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def write_down_info(jsonfile, this_file_id, parent_id, name, f_type, users):

  with open(jsonfile, "r") as jF:
    j_data = json.load(jF)
  
  new_users = []
  users_with_read_access = j_data['default_users']
  
  for u in users:
    if u not in users_with_read_access: 
      new_users.append(u)
  users_with_read_access = users_with_read_access + new_users
  if name == "" and f_type == "":
    # to update permissions only:
    j_data['default_users'] = users_with_read_access

  new_d = {}
  exists = 0
  for d in j_data["files"]:
      if d['google_source_id'] == this_file_id:
        print "A record with this Google ID already exists!"
        new_d['google_source_id'] = this_file_id + "=double"
        new_d['google_source_parent_id'] = parent_id
        new_d['name'] = name
        new_d['source_type'] = f_type
        exists = 1
      if d['name'] == name:
        print "A folder or file with this name already exists!"
        new_d['google_source_id'] = this_file_id
        new_d['google_source_parent_id'] = parent_id
        new_d['name'] = name + "=double"
        new_d['source_type'] = f_type
        exists = 1
  if exists == 0:
    new_d['google_source_id'] = this_file_id
    new_d['google_source_parent_id'] = parent_id
    new_d['name'] = name
    new_d['source_type'] = f_type

  if len(new_d) > 0:
    j_data["files"].append(new_d)
        
  print "new JSON: ", j_data

  with open(jsonfile, "w") as jF:
      jF.write(json.dumps(j_data, sort_keys=True, indent=4))

  return len(new_d)

def main(argv):
  this_path = os.path.dirname(sys.argv[0])
  this_path = this_path + "/" if this_path != "" else this_path  
  # print this_path
  SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.appdata']
  SERVICE_ACCOUNT_FILE = this_path + 'service.json'

  credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service2 = build('drive', 'v2', credentials=credentials)
  service3 = build('drive', 'v3', credentials=credentials)

  # put here files to delete
  hidden_files = []

  try:
    opts, arg = getopt.getopt(argv, "d:f:u:p:r:t:j:", ["del=", "folder=", "upload=", "ppl=", "report=", "parent=", "json="])
  except getopt.GetoptError:
    # automatic execution:
    print "options are incorrect, should be: -d, -f, -u, -p, -r, -t, -j (or --del, --folder, --upload, --ppl, --report, --parent, --json)"
    sys.exit(2)
  if len(opts) == 0:
    print "options are empty, should be: -d, -f, -u, -p, -r, -t, -j (or --del, --folder, --upload, --ppl, --report, --parent, --json)"
    sys.exit(2)    
  # execution by input arguments:
  file_id = ""
  for opt, arg in opts:
    if opt in ("-r", "--report"):
      file_id = arg

  UPLOADS_INFO = ''
  for opt, arg in opts:
    if opt in ("-r", "--json"):
      UPLOADS_INFO = arg
  try:
    with open(UPLOADS_INFO, "r") as jF:
      j_data = json.load(jF)
  
  except Exception, e:
    print "no json file specified!", e
    sys.exit(2)  
  users = j_data["default_users"]
  users = [str(u) for u in users]
  # print users

  parent_id = print_about(service2, service3)
  for opt, arg in opts:
    if opt in ("-t", "--parent"):
          for d in j_data["files"]:
            if d['source_type'] == "folder" and d['google_source_id'] == arg:
              parent_id = d['google_source_id']


  for opt, arg in opts:
    if opt in ("-d", "--del"):
      hidden_files = arg.split(",")

      print "files to delete:", hidden_files

      for f in hidden_files:
        delete_file(service3, f, "")
        
    elif opt in ("-f", "--folder"):
      folder_name = arg
      print "creating a folder:", folder_name
      folder_id = create_folder(service3, folder_name, users)
      write_down_info(UPLOADS_INFO, folder_id, parent_id, folder_name, 'folder', users)

    elif opt in ("-u", "--upload"):
      sql = arg
      current_time = datetime.now()
      date = "%s-%s-%s" % (current_time.month, current_time.day, current_time.year)
      report_name = sql + "_" + date + ".csv"
      upload_name = report_name.split("/")[-1]
      upload_name = upload_name.replace(".sql", "")

      print "creating a report:", upload_name
      # virtually unnecessary fields
      title = "Upload of a CSV report generated from SQL query"
      description = "Name of the SQL query is the name of the CSV file (+ date of report generation) and must explain the report purpose"

      mime_type = "text/csv"
      db = "vaxiom"
      tmpfile = "/var/lib/mysql-files/" + str(os.getpid()) + ".csv"
      DB(db, "").sql_from_the_file_to_csv(sql, tmpfile)

      print "uploading", upload_name
      # sudo chmod 755 /var/lib/mysql-files/
      this_file_id = upload_file(service3, upload_name.capitalize(), title, description, parent_id, mime_type, tmpfile, users)
      os.system("rm "+tmpfile)

      write_down_info(UPLOADS_INFO, this_file_id, parent_id, upload_name.capitalize(), 'file', users)

    elif opt in ("-p", "--ppl"):
      users_can_access = arg.split(",")
      if file_id != "":
        print "users, who can access the folder/file:", file_id, "emails:", users_can_access
        
        grant_permissions(service3, users_can_access, file_id)
        write_down_info(UPLOADS_INFO, file_id, "", "", "", users)
      else:
        print "no file_id (--report) is specified"

if __name__ == '__main__':
    main(sys.argv[1:])
