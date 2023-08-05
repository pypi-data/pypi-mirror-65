#  MIT License
#
#  Copyright (c) 2020 TorrentofShame
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

_Hooks = {}


def GetTable():
	""":returns Dictionary of all _Hooks."""
	return _Hooks


def Add(event_name: str, name: str = None, nsoc = False):
	"""
	Adds a hook to listen to the event specified.
	:param event_name: The name of the event to hook on to.
	:param name: An identifier for this hook, will use decorated func's name if None
	:param nsoc: set True if deco on classmethod or staticmethod - default False
	"""

	def decorator(func):
		if nsoc:
			def wrapper(*args, **kwargs):
				if event_name not in _Hooks: _Hooks[event_name] = {};
				_Hooks[event_name][name if name else func.__name__] = dict(f=func, a=args, k=kwargs)
				return func
			return wrapper
		else:
			if event_name not in _Hooks: _Hooks[event_name] = {};
			_Hooks[event_name][name if name else func.__name__] = dict(f=func, a=[], k=dict())
			return func
	return decorator


def Run(event_name: str, **kwargs):
	"""
	Runs specified event, and therefore any attached _Hooks.
	:param event_name: The name of the event to call
	:param kwargs: kwargs to pass to hook functions.
	:returns: dict of values returned from Hook
	"""
	if event_name not in _Hooks: _Hooks[event_name] = {};
	for f in filter(lambda fn: callable(fn["f"]), _Hooks[event_name].values()):
		returned_hook = f["f"](*f["a"], **f["k"], **kwargs) # Look @ the stars
		if returned_hook:
			return returned_hook  # If the hook returned anything, we return the Run function here.
