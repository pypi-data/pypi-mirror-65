from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(
    name='centeridentity',         # How you named your package folder (MyLib)
    packages=['centeridentity'],   # Chose the same as "name"
    version='0.4',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='API wrapper for center identity',   # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matthew Vogel',                   # Type in your name
    author_email='info@centeridentity.com',      # Type in your E-Mail
    url='https://github.com/pdxwebdev/pycenteridentity',   # Provide either the link to your github or to your website
    download_url='https://github.com/pdxwebdev/pycenteridentity/archive/v0.0.1.tar.gz',    # I explain this later on
    keywords=['blockchain', 'identity'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
