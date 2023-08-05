# Login Error
class LoginError(ValueError):
	pass

# File Error or File Not Found
class FileError(ValueError):
	pass

# Url Error or Url not found
class URLError(ValueError):
	pass

# If your connection is null
class ConnectionError(ValueError):
	pass
