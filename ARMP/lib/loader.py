import ARMP.params.config as config
from ARMP.lib.convention import Case, Case_clim, Setting

dic = {var: getattr(config, var) for var in dir(config) if not var.startswith('__')}


def init_dataclass(dc, dic):
    keys = dc.__annotations__.keys()
    subset = {key: dic[key] for key in keys if key in dic}
    return dc(**subset)


setting = init_dataclass(Setting, dic)
