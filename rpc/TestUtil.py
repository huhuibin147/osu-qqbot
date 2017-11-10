#coding=gbk
import sys
import os
import inspect
import traceback



def search_py_from_dir(TestPyList, TestDir):
    # ����Ŀ¼�ļ�����,py�ļ�ɸѡ
    for dir_path,subpath,files in os.walk(TestDir,True):
        for file in files:
            if file[-3:] == '.py':
                TestPyList.append(os.path.join(dir_path, file))

 
def set_environ():
    # ����·��
    TestSeverPath = os.path.dirname(os.path.abspath(__file__))
    # ��������
    os.environ['_BASIC_PATH_'] = TestSeverPath
    SeverDir = os.listdir(TestSeverPath)
    # Ĭ�Ϸ���Ŀ¼
    SetDirName = ['libs','mod']
    # Ŀ¼����ɸѡ
    TestDir = list(set(SetDirName) & set(SeverDir))
    # �����������б�
    TestPyList = []
    # ���������ļ�
    for Dir in TestDir:
        search_py_from_dir(TestPyList, os.path.join(TestSeverPath, Dir))

    # ����ģ�鵼�뻷��
    sys.path.append(TestSeverPath + '/lib')
    sys.path.append(TestSeverPath + '/lib/common')
    sys.path.append(TestSeverPath + '/lib/esunlib')
    if 'libs' in TestDir:
        sys.path.append(TestSeverPath + '/libs')
    sys.path.append(TestSeverPath + '/mod')

    return TestPyList


def method_search(TestPyList):
    # ��������
    for mod_py in TestPyList:
        # �����
        if _check_packag(mod_py, TestPyList):
            if '__init__' in mod_py:
                # '��⵽���ļ�__init__.py,�˳�'
                continue 
            mod = '%s.%s' % (os.path.basename(os.path.dirname(mod_py)),os.path.basename(mod_py))
        else:
            mod = os.path.basename(mod_py)
        # ��׺����
        mod = mod[:-3]
        # print '�����mod:'+mod
        m = __import__(mod)
        Methods = dir(m)

        # ��ģ�飬ʵ��������
        if '.' in mod:
            # ģ������,������ģ��ͬ��
            modname = os.path.basename(mod_py)[:-3]
            # ����ģ��
            module = eval('m.%s' % modname)
            # ʵ����
            instance = eval('module.%s()' % modname)
            # �෽���б�
            class_method = dir(instance)
            # ��λװ����
            for method in class_method:
                m1 = eval('instance.%s' % method)
                try:
                    if m1.__name__ == '__test':
                        return m1
                # �Ƿ���
                except:
                    pass
        # �ǰ�ģ��
        else:
            # ��������
            for method in Methods:
                m1 = eval('m.%s' % method)
                try:
                    if m1.__name__ == '__test':
                        return m1
                except:
                    pass
            # �༶��
            if mod in Methods:
                # ʵ����
                instance = eval('m.%s()' % mod)
                # �෽���б�
                class_method = dir(instance)
                # ��λ����
                for method in class_method:
                    m1 = eval('instance.%s' % method)
                    try:
                        if m1.__name__ == '__test':
                            return m1
                    except:
                        pass

            


def _check_packag(name, TestPyList):
    '''python�����'''
    if os.path.join(os.path.dirname(name), '__init__.py') in TestPyList:
        return True
    else:
        return False


def main():
    # ��ʼ������,��ȡ�б�
    TestPyList = set_environ()
    method = method_search(TestPyList)
    if not method:
        return '��λ����ʧ��!'
    _args,_kwargs = method.func_globals['_args'],method.func_globals['_kwargs']
    return method(*_args,**_kwargs)


def Test(*args, **kwargs):
    # װ��������
    global _args,_kwargs
    _args,_kwargs = args,kwargs
    def _deco(func):
        # �ı亯������װ����
        def __test(*args, **kwargs):
            return func(*args, **kwargs)
        return __test
    return _deco



if __name__ == '__main__':

    print main()

