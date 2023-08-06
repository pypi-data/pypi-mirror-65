import yapsy.IPlugin


def build(collectors):
    return Builder.build(collectors)


class Builder(object):
    @staticmethod
    def build(collectors):
        plugins = Builder.collect(collectors)
        chain = ChainNode(None, EndChainNode())
        chain = Builder.add_plugins_to_chain(chain, plugins)
        return chain

    @staticmethod
    def collect(collectors):
        plugins = []
        for collector in collectors:
            plugins += collector.collect()
        return plugins

    @staticmethod
    def add_plugins_to_chain(chain, plugins):
        for plugin in plugins:
            chain = ChainNode(chain, plugin)
        return chain


class ChainNode(object):
    def __init__(self, successor, plugin):
        self.successor = successor
        self.plugin = plugin

    def handle(self, *args, **kwargs):
        if self.plugin.check(*args, **kwargs):
            return self.plugin.handle(*args, **kwargs)
        else:
            if self.successor:
                return self.successor.handle(*args, **kwargs)

    def description(self):
        if self.successor is None:
            return []
        else:
            descriptions = self.successor.description()
            descriptions.append(self.plugin.description())
            return descriptions


class ChainNodePlugin(yapsy.IPlugin.IPlugin):
    def handle(self, *args, **kwargs):
        raise NotImplemented

    def check(self, *args, **kwargs):
        raise NotImplemented

    def description(self):
        raise NotImplemented


class EndChainNode(ChainNodePlugin):
    def check(self, *args, **kwargs):
        return True

    def handle(self, *args, **kwargs):
        return None

    def description(self):
        return None

