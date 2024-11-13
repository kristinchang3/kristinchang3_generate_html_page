import params.config as a
from lib.convention import Case, Case_clim, Setting

dic = {var: getattr(a, var) for var in dir(a) if not var.startswith('__')}


def init_dataclass(dc, dic):
    keys = dc.__annotations__.keys()
    subset = {key: dic[key] for key in keys if key in dic}
    return dc(**subset)


setting = init_dataclass(Setting, dic)
