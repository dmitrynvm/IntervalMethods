from distutils.core import setup
import py2exe

setup(windows=[{"script":"WidgetIA.py"}], options={"py2exe":{"includes":["sip","interval"]}})
