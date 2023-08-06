# -*- coding:utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description ='''
##mini深度框架
https://hellotrik.github.io/trik
'''

install_requires = [
    'numpy>=1.13',
]

if __name__ == '__main__':
    setup(name='trik',
          version="0.0.4",
          author='hellotrik',
          url='https://space.bilibili.com/489142974',
          author_email="hellotrik@foxmail.com",
          description='改自paradox的 练习用 深度框架',
          long_description_content_type="text/markdown",
          long_description=long_description,          
          platforms=['MS Windows', 'Mac X', 'Unix/Linux'],
          license='MIT',
          keywords=['深度学习', '机器学习', '自动微分', '符号计算'],
          packages=['trik',
                    'trik.sheng',
                    'trik.ya',
                    'trik.sheng.conv',
                    'trik.yu',
                    'trik.yu.data_handler',
                    'trik.sheng.lstm',
                    'trik.yu.data_set'],
          install_requires=install_requires,
          classifiers=["Natural Language :: English",
                       "Programming Language :: Python",
                       "Operating System :: Microsoft :: Windows",
                       "Operating System :: Unix",
                       "Operating System :: MacOS",
                       "Programming Language :: Python :: 3",
                       ],
          zip_safe=True)
