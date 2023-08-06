import os
import sys
import time
import shutil
import xlrd
import json
import configparser
import requests
import redis
from git import Repo
from x_sweetest import Autotest


class ApiRun:
    """
    API自动化测试执行端
    """

    def __init__(self, run_data):
        # 工作空间名
        self.NAME = run_data['name']
        # 平台URL
        self.PLATFORM_URL = run_data['platform_url']
        # 队列IP、队列KEY、队列端口号
        self.REDIS_IP = run_data['redis_ip']
        self.REDIS_KEY = int(run_data['redis_key'])
        self.REDIS_PORT = int(run_data['redis_port'])
        # GIT仓库URL
        self.GIT_URL = run_data['git_url']
        if self.GIT_URL.count('@') - 1 != 0:
            self.GIT_URL = self.GIT_URL.replace('@', '%40', self.GIT_URL.count('@') - 1)
        # 执行端注册ID
        self.EXECUTION_ID = int(run_data['execution_id'])
        # 通过队列IP、队列KEY、队列端口号参数连接Redis数据库
        self.POOL = redis.ConnectionPool(host=self.REDIS_IP, port=self.REDIS_PORT, db=self.REDIS_KEY,
                                         decode_responses=True)
        self.REDIS_POOL = redis.Redis(connection_pool=self.POOL)

    @staticmethod
    def mkdir_and_del(src_path):
        """
        删除旧文件夹再创建新文件夹
        """
        if os.path.isdir(src_path):
            shutil.rmtree(src_path)
        os.mkdir(src_path)

    @staticmethod
    def reset_file_tree(file_name, project_name, test_environment):
        """
        将Git用例仓库里的project_name项目目录中的file_name文件复制到执行目录中
        """
        case_path = os.path.join(os.getcwd(), "git_case")
        lib_dst_path = os.path.join(
            case_path, project_name + "-Project-api", test_environment, file_name)
        # 确定Git用例存储库中是否有一个lib_dst_path目录
        if os.path.isdir(lib_dst_path):
            lib_src_path = os.path.join(os.getcwd(), file_name)
            # 确定执行目录下是否有一个lib_src_path目录
            if os.path.isdir(lib_src_path):
                shutil.rmtree(lib_src_path)
            shutil.copytree(lib_dst_path, lib_src_path)

    def pull_case(self):
        """
        clone（拉取）和pull（更新）测试用例仓库的内容
        """
        git_case_path = os.path.join(os.getcwd(), "git_case")
        if os.path.isdir(git_case_path):
            print("[Api Server Run Info]> 发现 git_case 目录, 执行更新最新测试用例流程")
            repo = Repo.init(path=git_case_path)
            remote = repo.remote()
            remote.pull()
            print("[Api Server Run Info]> 已更新 GitLab 仓库中 git_case 项目的测试用例")
        else:
            print("[Api Server Run Info]> 找不到 git_case 目录, 执行下载新测试用例流程")
            Repo.clone_from(url=self.GIT_URL, to_path=git_case_path)
            print("[Api Server Run Info]> 已下载 GitLab 仓库中 git_case 项目的测试用例")

    def all_mkdir_copy(self, test_project, test_environment):
        """
        复制指定测试项目、测试类型、测试环境中的相关目录到自动化运行目录下
        """
        self.reset_file_tree(file_name="lib", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="data", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="element", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="testcase", project_name=test_project, test_environment=test_environment)
        self.reset_file_tree(file_name="files", project_name=test_project, test_environment=test_environment)
        ApiRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "JUnit"))
        ApiRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "report"))
        ApiRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "details"))

    @staticmethod
    def exec_api_test(test_name):
        """
        复制指定测试项目、测试类型、测试环境中的相关目录到自动化运行目录下
        """
        # X-Sweetest的测试用例集名称
        plan_name = test_name
        # 拼接测试用例集文件路径
        book = xlrd.open_workbook('testcase/' + test_name + '-TestCase.xlsx')
        # 测试用例集文件里的Sheet表单名称
        sheet_name = book.sheet_names()
        # X-Sweetest的测试参数
        desired_caps = {'platformName': 'api'}
        # 通过X-Sweetest执行自动化测试
        server_url = ''
        sweet = Autotest(plan_name, sheet_name, desired_caps, server_url)
        sweet.plan()
        # 创建并写入测试详情文件
        details_file = open('details/details.txt', 'w', encoding='utf-8')
        details_file.write(str(sweet.report_data))
        details_file.close()

    def post_heartbeat(self, status, localtime=None, task_dict=None, remark=None):
        """
        # 描述:
            发送心跳请求到ATP服务器（失败重试，直至恢复连接）
        # 用法0（第一次）:
            self.post_heartbeat(status=0)
        # 用法1（正常）:
            self.post_heartbeat(status=1, localtime=[调用时间])
        # 用法2（任务无法完成/放弃任务，需要在备注中提交错误信息）:
            self.post_heartbeat(status=2, localtime=[调用时间], task_dict=[任务字典], remark=[备注])
        # 用法3（开始执行任务）:
            self.post_heartbeat(status=3, localtime=[调用时间], task_dict=[任务字典])
        # 用法4（任务执行完成，上传测试报告）:
            self.post_heartbeat(status=4, localtime=[调用时间], task_dict=[任务字典])
        # 用法5（执行端异常，需要在备注中提交异常信息）:
            self.post_heartbeat(status=5, remark=[备注])
        """
        if not localtime:
            localtime = time.asctime(time.localtime(time.time()))
        # ATP平台端上执行端心跳的API接口
        heartbeat_api_url = self.PLATFORM_URL + 'software/execution/heartbeat/'
        # 心跳请求连接次数
        connect = 0
        # 开始发送心跳请求（不成功便成仁，真男人从不回头看爆炸）
        while True:
            # 捕获异常
            try:
                # 执行端心跳参数
                up_data = {'id': self.EXECUTION_ID, 'status': status, 'task_dict': json.dumps(task_dict),
                           'remark': remark}
                # 状态为4时，组织待上传的次数报告文件
                if status == 4:
                    # 拔高变量的层级
                    files_report = None
                    files_junit = None
                    # 取出XXX-Report@XXXXXX_XXX.xlsx的测试报告文件名
                    for _root, _dirs, files in os.walk(os.path.join('report', task_dict['test_name'])):
                        files_report = files[0]
                    # 取出XXX-Report@XXXXXX_XXX.xml的测试汇总文件名
                    for _root, _dirs, files in os.walk('JUnit'):
                        files_junit = files[0]
                    # 读取测试报告文件
                    with open(os.path.join('report', task_dict['test_name'], files_report), 'rb') as fp1:
                        files_report_obj = fp1.read()
                    # 读取测试汇总文件
                    with open(os.path.join('JUnit', files_junit), 'rb') as fp2:
                        files_junit_obj = fp2.read()
                    # 读取测试详情文件
                    with open(os.path.join('details', 'details.txt'), 'rb') as fp3:
                        files_details_obj = fp3.read()
                    # 汇总XXX-Report@XXXXXX_XXX.xlsx、XXX-Report@XXXXXX_XXX.xml、details.txt文件对象
                    files_obj = {
                        'file_obj': (str(task_dict['queue_id']) + '.xlsx', files_report_obj),
                        'file_obj_junit': (str(task_dict['queue_id']) + '.xml', files_junit_obj),
                        'file_obj_details': (str(task_dict['queue_id']) + '.txt', files_details_obj)
                    }
                else:
                    files_obj = {}
                # 向ATP平台端发送执行端心跳请求
                requests_data = requests.post(heartbeat_api_url, data=up_data, files=files_obj)
                requests_json = requests_data.json()
                # 判断平台端心跳状态处理结果
                if requests_json['code'] == 200:
                    # 心跳请求响应成功，结束死循环
                    print('[Heartbeat][' + localtime + ']> ' + str(requests_json['data']))
                    break
                # 服务器内部错误错误
                else:
                    print('[Heartbeat Error][' + localtime + ']> > ' + str(requests_json))
            # 网络请求错误
            except Exception as exc:
                print('[Heartbeat Error][' + localtime + ']> ' + str(exc))
            # 30秒后重新发送心跳请求
            time.sleep(30)
            connect += 1
            print('[Heartbeat Error][' + localtime + ']> 进行第 ' + str(connect) + ' 次重新连接')

    def run(self):
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "log"))
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "snapshot"))
        self.pull_case()
        print('[Api Server Run Info]> 检测是否有历史任务未完成')
        # 上报第一次/刚启动执行端的心跳
        self.post_heartbeat(status=0)
        while True:
            time.sleep(10)
            try:
                # 获取Redis任务队列的信息长度
                length = self.REDIS_POOL.llen(self.EXECUTION_ID)
                # 生成当前时间字符串，用于打印输出
                localtime = time.asctime(time.localtime(time.time()))
                # 如果Redis任务队列的信息长度小于0，那就说明没有任务
                if length > 0:
                    print('[Api Server Run Info][' + localtime + ']> ' + '发现新的任务信息')
                    self.pull_case()
                    value_dict = json.loads(self.REDIS_POOL.lpop(self.EXECUTION_ID))
                    # 上报开始执行任务的心跳
                    self.post_heartbeat(status=3, localtime=localtime, task_dict=value_dict)
                    try:
                        print('[Queue Task Dict]> ' + str(value_dict))
                        print('[Api Server Run Info]> 重置 X-Sweetest 测试运行环境')
                        self.all_mkdir_copy(test_project=value_dict['test_project'],
                                            test_environment=value_dict['test_environment'])
                        print('[Api Server Run Info]> X-Sweetest 测试运行环境就绪')
                        self.exec_api_test(test_name=value_dict['test_name'])
                        print('[Api Server Run Info]> X-Sweetest 测试完成并上传测试报告')
                        # 上报任务执行完成的心跳
                        self.post_heartbeat(status=4, localtime=localtime, task_dict=value_dict)
                        print('[Api Server Run Info]> 测试报告上传完毕')
                    except Exception as exc:
                        # 上报任务无法完成的心跳
                        self.post_heartbeat(status=2, localtime=localtime, task_dict=value_dict, remark=str(exc))
                        print('[Api Server Run Error]> ' + str(exc))
                else:
                    # 上报正常的心跳
                    self.post_heartbeat(status=1, localtime=localtime)
                # 调用Flush，从内存中刷入日志文件
                sys.stdout.flush()
            except Exception as exc:
                # 上报执行端异常的心跳
                self.post_heartbeat(status=5, remark=str(exc))
                print('[Api Server Run Error]> ' + str(exc))


if __name__ == '__main__':
    # 读取工作空间目录下的config配置文件
    config_file = 'config.ini'
    config = configparser.RawConfigParser()
    config.read(config_file, encoding='utf-8')
    # 读取配置中的ATP-Server内容
    data = dict(config.items('ATP-Server'))
    # 创建API自动化测试执行端对象
    r = ApiRun(run_data=data)
    # 启动API自动化测试执行端
    r.run()
