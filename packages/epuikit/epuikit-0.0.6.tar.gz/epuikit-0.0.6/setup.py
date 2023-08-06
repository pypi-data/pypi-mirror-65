import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except:
    long_description = 'UIKit for Raspberry on E-Paper'

setuptools.setup(
    name='epuikit',
    version='0.0.6',
    description='UIKit for Raspberry on E-Paper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='raspberry epaper uikit',
    install_requires=['interval'],
    packages=setuptools.find_packages(),
    author='jinsihou',
    author_email='540097546@qq.com',
    url='https://github.com/jinsihou19/E-Paper-UI-Kit',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
