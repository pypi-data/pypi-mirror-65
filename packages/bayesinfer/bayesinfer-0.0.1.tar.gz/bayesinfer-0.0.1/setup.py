from setuptools import setup, find_packages

VERSION = '0.0.1'

tests_require = []

install_requires = []

setup(name='bayesinfer', # 模块名称
      url='https://github.com/daixinyu/Bayes-infer',  # 项目包的地址
      author="tonydai",  # Pypi用户名称
      author_email='1320379472@qq.com',  # Pypi用户的邮箱
      keywords='python bayes inference event series',
      description='Automatically identify causal effects with Bayesian model.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],

      version=VERSION, 
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': [] },
      packages=find_packages(),
)
