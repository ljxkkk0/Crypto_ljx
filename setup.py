import setuptools
import os
import codecs

package_name = "Crypto_ljx"

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r", encoding="utf-8") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


FILE_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(FILE_PATH, "README.md"), "r", encoding="utf-8") as fh:
    try:
        long_description = fh.read()
    except UnicodeDecodeError:
        pass

requirements_path = os.path.join(FILE_PATH, "requirements.txt")
with open(requirements_path, "r", encoding="utf-8") as f:
    required = f.read().splitlines()

setuptools.setup(
    name=package_name,
    version=get_version("__init__.py"),
    author="Jason_ljx",  # 作者名称
    author_email="2395034115@qq.com", # 作者邮箱
    description="A crypto package , including Hash-SM3/Public key encryption algorithm - SM4 / Private key encryption algorithm --SM2/ Siganature algorithm -- SM2  ", # 库描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ljxkkk0/Crypto_ljx", # 库的官方地址
    packages=setuptools.find_packages(),
    data_files=["requirements.txt"], # yourtools库依赖的其他库
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
    install_requires=required,
)



