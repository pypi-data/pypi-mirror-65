from os import environ
#from gitversion import rewritable_git_version

print (environ)

__VERSION__ = '0.0.33'

if environ.get('MajorMinorPatch') is not None:
    __VERSION__ = environ.get('MajorMinorPatch')
#else:
#    __VERSION__ = rewritable_git_version(__file__)