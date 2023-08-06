from setuptools import setup, find_packages

setup(name='geomexp',
      version='0.2.1',
      description='2-d gemometric illusion experiments',
      url='https://github.com/mm-crj/geomexp',
      author='Mainak Mandal',
      author_email='mm.crjx@gmail.com',
      license='GNU LGPLv3',
#      long_description=open('README.md').read(),
#      long_description_content_type='text/markdown',
      packages=find_packages(),
      package_data={'': ['*.png']},
      python_requires='<= 2.8',
      classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Education',
      'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
      'Programming Language :: Python :: 2.7'],
       install_requires=['numpy>=1.16.6',
                         'psychopy>=1.85.2',
                         'pandas>=0.24.2',
                         'pygments>=2.4.2'
                         'wxPython>=4.0.4',
                         'pyyaml>=5.1.2',
                         'psutil>=5.6.3',
                         'msgpack>=1.0.0',
                         'gevent>=1.3.0',
                         'python-xlib>=0.26']
)
