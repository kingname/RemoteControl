#-*-coding:utf8-*-
from distutils.core import setup
import py2exe

'''
生成exe文件以后，请将logo.jpg放在dist文件夹里面，否则程序会报错。
'''
setup(windows=['Master.py'],
      options={'py2exe': {'dll_excludes': ['MSVCP90.dll']}}
      )
