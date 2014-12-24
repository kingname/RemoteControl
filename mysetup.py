from distutils.core import setup  
import py2exe  
  
setup(  
    console=["auto.py"],  
    options = { "py2exe": { "dll_excludes": ["MSVCP90.dll"] } }  
)  