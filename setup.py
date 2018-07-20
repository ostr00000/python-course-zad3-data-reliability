from setuptools import setup

setup(name='comparetool',
      version='1.0',
      description='compare artice on web',
      url='https://github.com/ostr00000/python-course-zad3-data-reliability',
      author='ostr00000',
      license='MIT',
      packages=['comparetool'],
      install_requires=[
            "matplotlib",
            "numpy",
            "google",
            "newspaper3k"
      ],
      zip_safe=False)
