from setuptools import setup

setup(
    name='covid19_certificate_pos',
    version='1.1',
    license='GPL v3',
    author="Emmanuel C",
    author_email="manuco@users.noreply.github.com",
    long_description=open('README.md').read(),
    download_url="https://github.com/manuco/covid19_certificate_pos/archive/1.1.tar.gz",
    packages=["attestation"],
    install_requires=[
        "python-escpos >= 3.0a, < 3.1",
        "PyQt5 < 5.15",
    ],
    entry_points = {
        'console_scripts': [
            'att_covid19 = attestation:run_ui',
        ],
    }
)
