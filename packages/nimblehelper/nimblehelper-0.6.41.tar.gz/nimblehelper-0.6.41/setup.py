from setuptools import setup

setup(name='nimblehelper',
      version='0.6.41',
      description='Nimble Infrastructure Helper',
      author='Brendan Kamp',
      author_email='brendan@tangentsolutions.co.za',
      license='MIT',
      packages=['nimblehelper'],
      install_requires=[
          'djangorestframework>=3.3.2',
          'requests',
          'django>=1.9.2',
          'django-log-labeler==1.2.4'
      ],
      zip_safe=False)
