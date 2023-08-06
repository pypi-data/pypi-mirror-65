from setuptools import setup
setup(name='myBestTool',
      version='1.1',
      description='my Tool',
      author='Du HongYu',
      author_email='837058201@qq.com',
      packages=['tool'],
      zip_safe=False,
      install_requires=[
            'pika',
            'requests',
            'lxml',
            'redis',
      ]
      )