import re
import sys
import uuid
import json
import zipfile
import argparse
import platform
import requests
from pathlib import Path
from atp.api_server import api_workspace


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='X ATP CLI Client (X 自动化测试平台命令行客户端)')
    parser.add_argument('-v', '--version', help='输出客户端版本信息', action='version', version='%(prog)s v0.2.2')
    parser.add_argument('-d', '--demo', help='在当前目录下创建 `x_sweetest_example` 项目',
                        action='store_true')
    parser.add_argument('-r', '--run', dest='atp_server_url',
                        help='运行 X-ATP 自动测试执行端服务 (E.g x-atp-cli -r http://127.0.0.1 -api)',
                        action='store')
    parser.add_argument('-api', '--api', help='运行 API 测试执行端 (used with parameter -r)',
                        action='store_true', default=False)
    parser.add_argument('-n', '--name', dest='workspace_name', help='执行端工作区的标识名称 (used with parameter -r)',
                        action='store', default='')
    args = parser.parse_args()
    if args.demo:
        x_sweetest_dir = Path(__file__).resolve().parents[0]
        example_dir = x_sweetest_dir / 'example' / 'x_sweetest_example.zip'
        extract(str(example_dir), Path.cwd())
        print('成功创建 `x_sweetest_example` 项目\n' +
              '快速体验, 请输入以下命令 (进入演示目录并开始运行脚本):\n\n' +
              'cd x_sweetest_example\npython echo.py\n')
    if args.atp_server_url:
        if not re.match(r'(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?',
                        args.atp_server_url,
                        re.IGNORECASE):
            print('[Cli Error]> 这不是有效的URl地址')
            return
        if args.api:
            data_json = get_initialization(test_type=0, atp_server_url=args.atp_server_url,
                                           workspace_name=args.workspace_name)
            api_workspace(sys_name=platform.system(), data=data_json['data'])
        else:
            print('[Cli Error]> 缺少 -api|-android|-ios|-web 参数')


def extract(z_file, path):
    """
    解压缩文件到指定目录
    """
    f = zipfile.ZipFile(z_file, 'r')
    for file in f.namelist():
        f.extract(file, path)


def get_initialization(test_type, atp_server_url, workspace_name):
    # 对输入的URL做判断，末尾没加"/" 统一处理加上"/"
    if not atp_server_url.endswith('/'):
        atp_server_url += '/'
    # ATP平台端初始化执行端的API接口
    initialization_api_url = atp_server_url + 'software/execution/initialization/'
    # 如果执行工作区名称为默认值，生成随机数
    if workspace_name == '':
        # 根据当前网卡和时间组成随机数
        workspace_name = uuid.uuid4().hex
    # api、android、ios、web执行端的通用参数
    up_data = {'name': workspace_name, 'execution_type': test_type}
    # api执行端的特殊参数
    if test_type == 0:
        up_data['information'] = json.dumps({'system': platform.system()})
    # 向ATP平台端发送初始化执行端请求
    requests_data = requests.post(initialization_api_url, data=up_data)
    requests_json = requests_data.json()
    print('[Cli info]> ' + str(requests_json))
    # 判断平台端初始化结果
    if requests_json['code'] != 200:
        print('[Cli Error]> 执行端服务初始化失败')
        sys.exit()
    # 附带上经过上面处理的ATP平台URl
    requests_json['data']['platform_url'] = atp_server_url
    return requests_json


if __name__ == '__main__':
    main()
