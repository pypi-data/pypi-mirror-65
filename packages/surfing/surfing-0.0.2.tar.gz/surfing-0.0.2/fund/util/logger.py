import os
from ..util.config import SurfingConfigurator
from tlclient.linker.logger import Logger

class SurfingLogger(Logger):

    @classmethod
    def _get_log_path_from_env(cls):
        log_path = SurfingConfigurator().get_sys_settings().get_log_dir()
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        return log_path
