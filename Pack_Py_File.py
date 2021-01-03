"""
打包py文件
"""

from distutils.core import setup
import py2exe

setup(console=["self_sim.py"])
