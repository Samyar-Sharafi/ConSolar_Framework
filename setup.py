from setuptools import setup, find_packages

setup(
       name='consolar',
       version='0.0.1',
       author='Samyar-Sharafi',
       author_email='samyar.sharafi.ss@gmail.com',
       description='A Console Framework for Interactive Applications',
       long_description=open('docs/README.md').read(),
       long_description_content_type='text/markdown',
       url='https://github.com/Samyar-Sharafi/Consolar',
       packages=find_packages(),
       install_requires=[
           'click', 'rich', 'prompt_toolkit', 'inquirer', 'tqdm', 'textual', 'pandas', 'yaml'
       ],
       classifiers=[
           'Programming Language :: Python :: 3',
           'License :: OSI Approved :: MIT License',
           'Operating System :: OS Independent',
       ],
       python_requires='>=3.6',
       entry_points={
           'console_scripts': [
               'consolar=ConSolar.main:main',  # Adjust this to your main entry point
           ],
       },
)
