#coding=gbk
import sys
import os
import inspect
import traceback



def search_py_from_dir(TestPyList, TestDir):
    # 遍历目录文件过滤,py文件筛选
    for dir_path,subpath,files in os.walk(TestDir,True):
        for file in files:
            if file[-3:] == '.py':
                TestPyList.append(os.path.join(dir_path, file))

 
def set_environ():
    # 服务路径
    TestSeverPath = os.path.dirname(os.path.abspath(__file__))
    # 环境变量
    os.environ['_BASIC_PATH_'] = TestSeverPath
    SeverDir = os.listdir(TestSeverPath)
    # 默认服务目录
    SetDirName = ['libs','mod']
    # 目录存在筛选
    TestDir = list(set(SetDirName) & set(SeverDir))
    # 用于搜索的列表
    TestPyList = []
    # 遍历服务文件
    for Dir in TestDir:
        search_py_from_dir(TestPyList, os.path.join(TestSeverPath, Dir))

    # 服务模块导入环境
    sys.path.append(TestSeverPath + '/lib')
    sys.path.append(TestSeverPath + '/lib/common')
    sys.path.append(TestSeverPath + '/lib/esunlib')
    if 'libs' in TestDir:
        sys.path.append(TestSeverPath + '/libs')
    sys.path.append(TestSeverPath + '/mod')

    return TestPyList


def method_search(TestPyList):
    # 方法搜索
    for mod_py in TestPyList:
        # 包检测
        if _check_packag(mod_py, TestPyList):
            if '__init__' in mod_py:
                # '检测到包文件__init__.py,退出'
                continue 
            mod = '%s.%s' % (os.path.basename(os.path.dirname(mod_py)),os.path.basename(mod_py))
        else:
            mod = os.path.basename(mod_py)
        # 后缀处理
        mod = mod[:-3]
        # print '导入的mod:'+mod
        m = __import__(mod)
        Methods = dir(m)

        # 包模块，实例化处理
        if '.' in mod:
            # 模块类名,规则与模块同名
            modname = os.path.basename(mod_py)[:-3]
            # 调出模块
            module = eval('m.%s' % modname)
            # 实例化
            instance = eval('module.%s()' % modname)
            # 类方法列表
            class_method = dir(instance)
            # 定位装饰器
            for method in class_method:
                m1 = eval('instance.%s' % method)
                try:
                    if m1.__name__ == '__test':
                        return m1
                # 非方法
                except:
                    pass
        # 非包模块
        else:
            # 方法级别
            for method in Methods:
                m1 = eval('m.%s' % method)
                try:
                    if m1.__name__ == '__test':
                        return m1
                except:
                    pass
            # 类级别
            if mod in Methods:
                # 实例化
                instance = eval('m.%s()' % mod)
                # 类方法列表
                class_method = dir(instance)
                # 定位方法
                for method in class_method:
                    m1 = eval('instance.%s' % method)
                    try:
                        if m1.__name__ == '__test':
                            return m1
                    except:
                        pass

            


def _check_packag(name, TestPyList):
    '''python包检测'''
    if os.path.join(os.path.dirname(name), '__init__.py') in TestPyList:
        return True
    else:
        return False


def main():
    # 初始化环境,获取列表
    TestPyList = set_environ()
    method = method_search(TestPyList)
    if not method:
        return '定位方法失败!'
    _args,_kwargs = method.func_globals['_args'],method.func_globals['_kwargs']
    return method(*_args,**_kwargs)


def Test(*args, **kwargs):
    # 装饰器参数
    global _args,_kwargs
    _args,_kwargs = args,kwargs
    def _deco(func):
        # 改变函数名的装饰器
        def __test(*args, **kwargs):
            return func(*args, **kwargs)
        return __test
    return _deco



if __name__ == '__main__':

    print main()

