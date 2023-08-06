import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='sequence_cut',
    version='0.0.2',
    author='BlueSkyBubble',
    author_email='yajie.wagn@gmail.com',
    description='Cut a sequence to some sub-sequences by specifying a maxinum sub-sequence length.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/BlueSkyBubble/script',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]

)
