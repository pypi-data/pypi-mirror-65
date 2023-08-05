# from setuptools import setup, find_packages

# with open('README.md') as readme_file:
#     README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

# setup_args = dict(
#     name='micro-pulse',
#     version='0.1.0',
#     description='Kafka Based Lightweight Python Microservice Framework',
#     # long_description_content_type="text/markdown",
#     long_description="long_description",
#     license='MIT',
#     packages=find_packages(),
#     author='Frog Dev',
#     author_email='dev@frog-mining.com',
#     keywords=['kafka', 'python', 'microservice', 'framework'],
#     url='https://gitlab.com/frog-network/micro-pulse',
#     download_url='https://pypi.org/project/micro-pulse/',
#     include_package_data=False
# )

# install_requires = [
#     'kafka-python==2.0.0'
# ]

# if __name__ == '__main__':
#     setup(**setup_args, install_requires=install_requires)
# oN*srH27@#bE


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="micro-pulse",
    version="1.0.4",
    author="Frog Dev",
    author_email="dev@frog-mining.com",
    description="Kafka Based Lightweight Python Microservice Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/frog-network/micro-pulse',
    download_url='https://pypi.org/project/micro-pulse/',
    packages=setuptools.find_packages(),
    keywords=['kafka', 'python', 'microservice', 'framework'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'kafka-python==2.0.0'
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
