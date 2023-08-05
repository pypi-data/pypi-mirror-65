from setuptools import setup


setup(name='rbpros',
      version='0.4',
      description='ROS2 on Raspberry PI',
      url='',
      author='Dirk Zhou',
      author_email='dontbmh2011@gmail.com',
      license='MIT',
      packages=['rbpros', 'rbpros/suite'],
      install_requires=[
          'rpi.gpio',
          'smbus',
          'spidev'
      ],
      entry_points={
          'console_scripts': [
              'rbpros = rbpros.__main__:main',
          ]
      },
      python_requires='>=3.6',
      zip_safe=False)
