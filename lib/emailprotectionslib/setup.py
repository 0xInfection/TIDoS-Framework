from distutils.core import setup

setup(
    name="emailprotectionslib",
    packages=["emailprotectionslib"],
    version="0.8.3",
    description="Python library to interact with SPF and DMARC",
    author="Alex DeFreese",
    author_email="alexdefreese@gmail.com",
    url="https://github.com/lunarca/pyemailprotectionslib",
    requires=['dnslib', 'tldextract'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
    ]
)