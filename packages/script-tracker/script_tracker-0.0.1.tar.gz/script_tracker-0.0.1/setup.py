from setuptools import setup

setup(name='script_tracker',
      version='0.0.1',
      description='Script Tacker provides an Android and Ios mobile application based dashboard to perform live tracking of your scripts. Currently this is only supporting python. Users can track the progress of their scripts from anywhere. Mobile applications are created using Flutter platform and server side is managed using Firebase.',
      url='https://github.com/asad1996172/Script-Tracker',
      download_url='https://github.com/asad1996172/Script-Tracker',
      uthor='Asad Mahmood, Zeeshan Ahmad',
      author_email='asad007mahmood@gmail.com, ahmadzee26@gmail.com',
      license='MIT',
      packages=['script_tracker'],
      install_requires=[
          'requests',
          'firebase_admin',
      ],
      zip_safe=False,
      include_package_data=True)