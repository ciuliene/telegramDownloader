import os

class EnvTool:
    def __init__(self) -> None:
        pass

    def get_env_var(self, var_name: str, raise_ex: bool = False):
        try:
            return os.environ[var_name]
        except Exception as ex:
            if raise_ex:
                raise ex
            else:
                return None
        
    def set_env_var(self, var_name: str, var_value: str):
        os.environ[var_name] = var_value

    def set_env_vars_from_file(self, file_path: str = '.env'):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                if '=' in line:
                    var_name, var_value = line.split('=', 1)
                    self.set_env_var(var_name, var_value.strip())