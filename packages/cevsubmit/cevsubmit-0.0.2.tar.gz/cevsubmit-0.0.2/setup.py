from setuptools import setup
setup(
    author="Ujjwal (CEVian)",
    author_email="contact@cevgroup.org",
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Utilities"
    ],
    message_extractors = {
        'cevsubmit': [('**.py', 'python', None),],
    },
    description="This is cevsubmit, with which you can submit solutions to github.",
    install_requires=["lib50>=2.1,<3", "requests>=2.19", "termcolor>=1.1"],
    keywords=["submit", "cevsubmit"],
    name="cevsubmit",
    python_requires=">=3.6",
    license="GPLv3",
    packages=["cevsubmit"],
    url="https://github.com/cutting-edge-visionaries/cevsubmit",
    entry_points={
        "console_scripts": ["cevsubmit=cevsubmit.__main__:main"]
    },
    version="0.0.2",
    include_package_data=True
)
