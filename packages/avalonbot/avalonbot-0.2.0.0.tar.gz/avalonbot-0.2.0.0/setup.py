from setuptools import setup

config = {
    'include_package_data': True,
    'description': 'Bot for doing initial avalon card assignments',
    'url': 'https://github.com/AvantiShri/avalon-bot',
    'author': 'Av Shrikumar',
    'author_email': 'avanti.shrikumar@gmail.com',
    'version': '0.2.0.0',
    'packages': ['avalonbot'],
    'setup_requires': [],
    'install_requires': [], #I believe I only use the standard library
    'dependency_links': [],
    'scripts': ['run_avalon_bot'],
    'name': 'avalonbot'
}

if __name__== '__main__':
    setup(**config)
