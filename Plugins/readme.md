# 关于插件设计
## 插件分类
* 调用可执行文件（如window截图）
* 依赖于当前控件（指的是核心控件的AppCore，下同）的插件区（PluginArea控件）显示的Widget
* 依赖于当前控件的独立程序

## 所有插件的共性
- 插件文件路径必须指定在plugins.json文件中，可以通过插件导入器来载入新插件（日后我会实现）
- 所有的插件必须要有main函数入口作为启动函数

## 调用可执行文件（如window截图）
- main函数中参数不被调用且main参数无返回值，但千万不能声明widget参数，可以使用所有os库下面的system方法，如下
```python
from os import system as os_system
main = lambda : os_system("可执行文件路径")
```

## 依赖于当前控件的插件区显示的Widget
1. 这时候，你需要传入如下几个参数
- widget参数，必须参数，声明这是一个依赖于当前控件的插件区显示的Widget，参数可以是任何值，仅仅用于标识
- icon、text、tips，可选参数，分别用于表示插件标签页的图标、标题、作用提示
- 入口函数main的返回值必须是一个字典，返回至少包含widget参数的键值对，其中此时widget的值必须是你要呈现的插件，该widget会作为一个Tab展示在插件区
- 建议在参数声明就带这些参数，而不是只在返回时声明，因为日后可以会做参数优化

```text
def main(widget: '',
         icon=qticon('ri.markdown-fill', color='darkblue'),
         text='MD编辑器',
         tips='内置的Markdown编辑器',
         ) -> dict:
    return dict(
        widget=MDEditor().setWidgets(),
        icon=icon,
        text=text,
        tips=tips
    )
```

## 依赖于当前控件的独立程序
- 预计不开发此功能


# 关于插件载入器的使用
...