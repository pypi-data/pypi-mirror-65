from kts.core.cache import CachedMapping
from kts.settings import cfg

class SyncedList(CachedMapping):
    def sync(self, scope=None):
        if scope is None:
            scope = cfg.scope
        for name, value in self.items():
            scope[name] = value


class FeatureList(SyncedList):
    def __init__(self):
        super().__init__('features')

    def register(self, feature_constructor):
        if feature_constructor.name in self:
            if feature_constructor.source != self[feature_constructor.name].source:
                raise UserWarning(f"Source code mismatch. ")
            return
        self[feature_constructor.name] = feature_constructor


class HelperList(SyncedList):
    def __init__(self):
        super().__init__('helpers')

    def register(self, helper):
        self[helper.name] = helper


feature_list = FeatureList()
helper_list = HelperList()