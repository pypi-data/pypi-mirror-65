from setuptools import setup, find_packages

setup(
    name='covid19-full-stat',
    version='0.0.2.2',
    packages=find_packages(),
    url='https://github.com/Sergii-Lak/covid19-info-stats',
    package_dir={'': 'C:\\Proje\covid19-info-stats\\'},
    license='MIT',
    author='Sergii-Lak',
    install_requires=["pandas", "numpy"],
    author_email='serg1509@yandex.ru',
    description='Сovid19 statistics per countries and for the world'
)
