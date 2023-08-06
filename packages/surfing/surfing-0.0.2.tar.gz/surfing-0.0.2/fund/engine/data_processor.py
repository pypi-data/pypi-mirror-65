from collections import OrderedDict
from fund.util.logger import SurfingLogger

class DpModule(object):
    '''
    数据处理组件，执行具体计算任务
    （输入数据）-> DpModule -> （输出数据）
    '''

    def __init__(self):
        '''
        初始化，定义计算必须的输入数据字典项
        '''
        self._necessary_keys = []
        self._logger = SurfingLogger.get_logger(type(self).__name__)

    def run(self, data_in):
        '''
        数据处理主函数，供外部调用
        此函数调用内部计算流程
        :param data_in: 输入数据（字典，字典 key 为数据名称，value 为数据体）
        :return: 如果成功，输出数据字典（字典 key 为数据名称，value 为数据体）；如果失败输出 None
        '''
        if not self._verify_data_in(data_in):
            return None

        try:
            self._logger.info(f'{type(self).__name__} starts to run')
            return self._run(data_in)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self._logger.error(f'{type(self).__name__} run failed, error: {traceback.format_exc()}')
            return None

    def _verify_data_in(self, data_in):
        '''
        验证输入数据是否满足需求
        :param data_in: 输入数据（字典，字典 key 为数据名称，value 为数据体）
        :return Bool: True 表示满足，False 表示不满足
        '''
        for necessary_key in self._necessary_keys:
            if necessary_key not in data_in:
                self._logger.error(f'Missing necessary key {necessary_key} in PositionProcessor data_in, processor stopped')
                return False
        return True

    # TO BE OVERRIDDEN
    def _run(self, data_in):
        '''
        数据处理逻辑函数
        :param data_in: 输入数据（字典，字典 key 为数据名称，value 为数据体）
        :return: 如果成功，输出数据字典（字典 key 为数据名称，value 为数据体）；如果失败输出 None
        '''
        self._logger.error('_run(self, data_in) in DpModule is not overridden')
        return None

class DataProcessor(object):
    '''
    数据处理调度器，调度 DpModule 执行计算逻辑
    （输入数据）-> DataProcessor -> （输出数据）
    '''

    def __init__(self):
        '''
        初始化带有优先级的数据处理组件列表
        优先级数字越小代表优先级越高，同一优先级下组件无相互依赖，低优先级组件可依赖高优先级组件
        modules: {priority(int)->[DpModule]}
        '''
        self._logger = SurfingLogger.get_logger(type(self).__name__)
        
        self.modules = {}
        self.priorities = []
    
    def attach(self, priority, dp_module):
        if priority not in self.modules:
            self.modules[priority] = []
            self.priorities.append(priority)
            self.priorities.sort()

        self.modules[priority].append(dp_module)

    def process(self, data, **kwargs):
        '''
        数据处理主函数，供外部调用
        此函数调用内部计算流程
        :param data: 输入数据（字典，字典 key 为数据名称，value 为数据体）
        :return: True or False
        '''
        for priority in self.priorities:
            to_break = False
            for module in self.modules[priority]:
                module_output = module.run(data)
                if module_output is not None:
                    # TODO
                    data.update(module_output)
                else:
                    self._logger.error(f'Module {type(module).__name__} failed in processing')
                    to_break = True
            if to_break:
                return False
        return True