# Exceptions

# If login error (failed or error)
class LoginError(ValueError):
	pass

# If scrap error
class FailedScrap(ValueError):
	pass

# If not login
class LoginRequired(ValueError):
	pass

# if change error or failed
class ChangeFailed(ValueError):
	pass

# If ListError or Null
class ListError(ValueError):
	pass
