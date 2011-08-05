from distutils.core import setup
import py2exe

setup(windows=['notifierwx.pyw'],
      zipfile=None,
      options = {"py2exe":
                 { "bundle_files":1,
                     'dll_excludes': [
                    'MSVCP90.dll' ]
                  }
                }
)
