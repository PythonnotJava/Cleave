from os import PathLike
from json import load, dump
from importlib.util import module_from_spec, spec_from_file_location
from typing import Callable

# 工具插件的解释器
class PluginsLoader:
    __slots__ = ('CoreFile', 'CoreData', 'keys', 'versions', 'infos', 'deses', 'icons', 'links', 'shortcuts')
    def __init__(self, plugins_json: PathLike | str):
        self.CoreFile = plugins_json
        self.CoreData = load(open(plugins_json, 'r', encoding='U8'))
        self.keys = []
        self.versions = []
        self.infos = []
        self.deses = []
        self.icons = []
        self.links = []
        self.shortcuts = []

    def analysis(self):
        core_data: dict = self.CoreData['Packages']
        # such-like
        # "Help": {
        #     "version": "插件版本，可以不指定",
        #     "info": "作者信息，可以不指定",
        #     "des": "插件的描述，可以不指定",
        #     "icon": "插件相关图标名字，可以不指定",
        #     "link": "插件所连接的功能文件，可以不指定",
        #     "shortcuts": "插件被标记的快捷键，可以不指定；若快捷键重复，则视为无效"
        # },
        for key in core_data:
            current : dict = core_data[key]
            self.keys.append(key)
            self.versions.append(current.get('version', None))
            self.infos.append(current.get('info', None))
            self.deses.append(current.get('des', None))
            self.icons.append(current.get('icon', None))
            self.links.append(current.get('link', None))
            self.shortcuts.append(current.get('shortcuts', None))

    # 核心函数，根据链接的文件找到主函数入口
    @staticmethod
    def linkMainFunction(linkFile : PathLike | str = None) -> Callable:
        if linkFile is not None:
            spec = spec_from_file_location("pkg", linkFile)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            # 插件的主函数入口查找，这里打算拓展一个基于父控件展示的判别，传入参数为父控件self(A Widget)
            if hasattr(module, 'main') :
                return getattr(module, 'main')
            else:
                return lambda : print("没有main入口!!")
        else:
            return lambda : print('没有相关文件!')

    def writeBack(self): dump(self.CoreData, open(self.CoreFile, 'w', encoding='U8'))

