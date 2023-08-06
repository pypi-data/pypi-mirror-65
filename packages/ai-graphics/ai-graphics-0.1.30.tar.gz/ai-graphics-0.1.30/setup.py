from setuptools import setup, find_packages

requirements = [
    'numpy',
    'opencv-python',
    'flask',
    'tezign',
    'sklearn',
    'scenedetect',
    'moviepy==1.0.0',
    'Pillow<7.0.0',
    'torch',
    'torchvision',
]

__version__ = '0.1.30'

setup(
    # Metadata
    name='ai-graphics',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/Python_Cookbook',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='AI Graphics Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
