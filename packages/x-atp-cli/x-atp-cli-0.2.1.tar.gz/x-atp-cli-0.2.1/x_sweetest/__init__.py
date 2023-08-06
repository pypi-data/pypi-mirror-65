import sys
import shutil
import zipfile
from pathlib import Path
from x_sweetest.autotest import Autotest
from x_sweetest.report import reporter


def extract(zfile, path):
    f = zipfile.ZipFile(zfile, 'r')
    for file in f.namelist():
        f.extract(file, path)


def x_sweetest():
    x_sweetest_dir = Path(__file__).resolve().parents[0]
    example_dir = x_sweetest_dir / 'example' / 'x_sweetest_example.zip'
    extract(str(example_dir), Path.cwd())

    print('\n\n生成 x_sweetest example 成功\n快速体验，请输入如下命令(进入示例目录，启动运行脚本):\n\ncd x_sweetest_example\npython start.py')
