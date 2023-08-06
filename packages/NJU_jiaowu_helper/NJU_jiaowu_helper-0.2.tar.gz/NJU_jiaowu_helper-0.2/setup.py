from setuptools import setup, find_packages

setup(name = "NJU_jiaowu_helper",
    version = "0.2",
    description = "nju helper",
    author = "Tomsawyerhu",
    author_email = "181250046@smail.nju.edu.cn",
    url = "",
    packages = find_packages(),
    #'runner' is in the root.
    entry_points={'console_scripts': [
          'chatwithconsole=jiaowu.console.runner:main'
    ]},

    zip_safe=False

)