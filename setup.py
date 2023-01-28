from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Win32GUI' if sys.platform=='win32' else None
icon = "./Untitled-1.ico"
executables = [
    Executable('guilog.py', base=base, icon=icon)
]

setup(name='CalLogTradeBinance',
      version = '1.0',
      description = 'Summary Log Binance Future',
      options = dict(build_exe = buildOptions),
      executables = executables)
