import setuptools

setuptools.setup(
    name="g2pM",
    version="0.1",
    license='Apache License 2.0',
    author="Seanie Lee",
    author_email="lsnfamily02@gmail.com",
    description="g2pM: A Neural Grapheme-to-Phoneme Conversion Package for MandarinChinese",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kakaobrain/g2pM",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    package_data={'g2pM': ['g2pM/digest_cedict.pkl',
                           'g2pM/char2idx.pkl', 'g2pM/class2idx.pkl', 'g2pM/np_ckpt.pkl']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
