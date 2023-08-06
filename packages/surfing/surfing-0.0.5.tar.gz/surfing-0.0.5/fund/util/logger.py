import os
from ..util.config import SurfingConfigurator
from tlclient.linker.logger import Logger

class SurfingLogger(Logger):

    @classmethod
    def _get_log_path_from_env(cls):
        log_path = SurfingConfigurator().get_sys_settings().log_dir
        
        return log_path
