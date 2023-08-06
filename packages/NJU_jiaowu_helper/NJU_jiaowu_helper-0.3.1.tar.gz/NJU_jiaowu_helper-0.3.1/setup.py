from setuptools import setup, find_packages

setup(name = "NJU_jiaowu_helper",
    version = "0.3.1",
    description = "nju helper",
    author = "Tomsawyerhu",
    author_email = "181250046@smail.nju.edu.cn",
    url = "https://github.com/Tomsawyerhu/NJU-jiaowuweb",
    packages = find_packages(),
    install_requires=[
        'setuptools >= 16.0',
        'xlwt >= 1.3.0',
        'pytesseract >= 0.3.3',
        'scrapy >= 2.0.1',
        'requests >= 2.23.0',
        'pillow >= 7.1.1',
],
    #'runner' is in the root.
    entry_points={'console_scripts': [
          'chatwithconsole=jiaowu.console.runner:main'

    ]},

    zip_safe=False

)