from distutils.core import setup

with open('requirements.txt') as file:
    requirements = '\n'.join(file.readlines())

setup(
    name='dvdp.ha_mqtt',
    version='0.1.0',
    packages=['dvdp.ha_mqtt'],
    download_url='https://github.com/davidvdp/ha_mqtt/archive/v0.1.0.tar.gz',
    url='https://github.com/davidvdp/ha_mqtt',
    author='David van der Pol',
    author_email='david@davidvanderpol.com',
    license='MIT',
    description='Home assistant mqtt devices interface',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
        'MQTT',
        'Home',
        'Assistant',
    ],
)