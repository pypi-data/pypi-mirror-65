from setuptools import setup

setup(
    name = 'gym_wumpus',
    packages = ['gym_wumpus'],
    version = '0.1',
    license = 'MIT',
    install_requires = ['gym', 'numpy'],
    description = 'Wumpus World environment for gym',
    author = 'David Mosallanezhad',
    author_email = 'amosalla@asu.edu',
    url = 'https://github.com/Davood-M/gym_wumpus_world',
    download_url = 'https://github.com/Davood-M/gym_wumpus_world/archive/0.1.tar.gz',
    keywords = ['wumpus world', 'wumpus', 'gym'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)