from setuptools import setup
setup(name='isBestTool',
      version='1.0',
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