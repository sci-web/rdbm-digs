from apiclient import errors
# ...

def remove_permission(service, file_id):
  """Remove a permission.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to remove the permission for.
    permission_id: ID of the permission to remove.
  """
  permissions = ["07202669905482576069","04924977322168841224","04924977322168841224","07202669905482576069"]
  print permissions
  for permission_id in permissions:
	  print "removing permission", permission_id 
	  try:
	    service.permissions().delete(fileId=file_id, permissionId=permission_id).execute()
	  except errors.HttpError, error:
	    print 'An error occurred: %s' % error

def main(argv):
	
