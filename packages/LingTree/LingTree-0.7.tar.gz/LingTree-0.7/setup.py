#!/usr/bin/env python
from setuptools import setup

__doc__='''
Utility functions to read and write common treebank formats.
'''

setup(name='LingTree',
      version='0.7',
      description='Python Package for Eclectic Linguistic Processing',
      author='Yannick Versley',
      author_email='yannick@inteligile.com',
      url='https://github.com/yv/LingTree',
      packages=['lingtree', 'lingtree.eval'],
      package_dir={'':'py_src'},
      install_requires=['future', 'PyYAML', 'mock >= 2.0.0'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Text Processing :: Linguistic"],
      entry_points={
            'console_scripts': [
                  'lingtree_convert=lingtree:convert_main',
                  'lingtree_totext=lingtree:totext_main',
                  'lingtree_merge=lingtree.conll:merge_main',
                  'lingtree_recombine=lingtree.conll:recombine_main',
                  'lingtree_html=lingtree.csstree:csstree_main'
            ]}
      )
