from setuptools import setup, find_packages

setup(
   name  = 'simplewsgi',
   version = '0.0.2',
   description = 'A sample Python project',
   long_description = open('README.md').read(),
   long_description_content_type="text/markdown",
   license = 'MIT',
   author = 'Chinen',
   author_email = 'q304023zm@gmail.com',
   url='https://github.com/q304023zm/first_package',
   keywords = 'sample',
   packages = find_packages(),
   install_requires = ['requests'],
   python_requires=">=3.5.0",
   classifiers = [
     'Development Status :: 5 - Production/Stable',
     'Programming Language :: Python',
     'Programming Language :: Python :: 3',
     'Programming Language :: Python :: 3.7',
     'Intended Audience :: Developers',
     'Topic :: Software Development :: Libraries :: Python Modules',
     'License :: OSI Approved :: MIT License'
   ]
)