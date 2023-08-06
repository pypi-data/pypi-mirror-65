import setuptools

setuptools.setup(
    name='pyuni',  # Replace with your own username
    version='0.0.2',
    author='Anh Pham',
    author_email="anhphamduy@outlook.com",
    description='A tool to get classes timetable',
    url="https://github.com/anhphamduy/pyuni",
    packages=setuptools.find_packages(),
    install_requires=[
        'selenium',
    ],
    classifiers=[],
    python_requires='>=3.6',
)
