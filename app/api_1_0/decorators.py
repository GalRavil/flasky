from functools import wraps

from flask import g

from .errors import forbidden


def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_functoin(*args, **kwargs):
			if not g.current_user.can(permisson):
				return forbidden('Insufficient permission')
			return f(*args, **kwargs)
		return decorated_functoin
	return decorator
