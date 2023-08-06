from setuptools import setup, find_packages

def requirements():
    with open(r'requirements.txt') as f:
        required = f.read().splitlines()
    return required

def readme():
    with open('README.md') as f:
        README = f.read()
        return README

setup(
        name = 'resume_classification',
        version = '1.0',
        description = 'It a simple package for training and classification of resumes.',
        long_description = readme(),
        long_description_content_type = 'text/markdown',
        url = "https://github.com/shreyas2306/ResumeParser",
        author = "Shreyas Nanaware/Krushna Kumar Nalange",
        license = "MIT",
        classifiers = [
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",

        ],
        packages = find_packages(),
        include_package_data =  True,
        package_data = {'resume_classification': ['model/*']},
        install_requires = requirements()

    )