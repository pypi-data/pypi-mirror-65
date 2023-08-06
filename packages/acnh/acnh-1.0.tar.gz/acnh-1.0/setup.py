from setuptools import setup

setup(
    name='acnh',
    version='1.0',
    description='Dataset containing fish, fossils, bugs, etc for Animal Crossing: New Horzions',
    url='https://github.com/valknight/ACNH-Dataset',
    author='Val Knight',
    author_email='val@valknight.xyz',
    license='MIT license',
    packages=['acnh'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
)
