
# python setup.py sdist upload
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
############################################# 
from setuptools import setup, find_packages,Extension
from kcweb import config
import os
confkcw=config.kcweb
def get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
b=get_file("kcweb",['kcweb'])
setup(
    name = confkcw["name"],
    version = confkcw["version"],
    # keywords = confkcw["keywords"],
    description = confkcw["description"],
    long_description = confkcw["long_description"],
    license = confkcw["license"],
    author = confkcw["author"],
    author_email = confkcw["author_email"],
    maintainer = confkcw["maintainer"],
    maintainer_email = confkcw["maintainer_email"],
    url=confkcw['url'],
    packages =  b,
    # install_requires = ['pymongo==3.10.0','six==1.12.0','requests==2.22.0','watchdog==0.9.0','Mako==1.1.0','paramiko==2.6.0','webssh==1.4.5'], #第三方包
    install_requires = ['pymongo==3.10.0','Mako','requests====2.23.0','six==1.12.0','watchdog==0.9.0'], #第三方包
    package_data = {
        '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif'],
    }
)