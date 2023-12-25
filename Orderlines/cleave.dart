/// 这是Cleave的命令行
/// 命令行下分三种模式：无参数命令、widget模式、信息模式
/// # 无参数命令
/// 无输入即直接启动Cleave主程序
/// # widget模式
/// -e、excel：启动excel核心
/// -p、plugin：插件拓展部件
/// -c、cml：打开拓展编辑器
/// -d、debug：使用调试功能，前提是你需要有一个搭建好的Python环境
/// # 信息模式
/// -v、version：查看版本信息
/// -a、author：作者信息
/// -l、license：查看许可证
/// -h、help：帮助
/// -w、where：查看Cleave的路径
/// -list：查看插件列表
/// 当然了，命令出错，则抛出“没有此类命令”

import 'package:args/args.dart';

class OrderLines {
  static const String outlines = '''
Usage:
    Cleave <command> [options]
Commands:
    excel
    plugin
    cml
    debug
    version
    author
    license
    help
    where
    list
General Options:
    -e、excel：启动excel核心
    -p、plugin：插件拓展部件
    -c、cml：打开拓展编辑器
    -d、debug：使用调试功能，前提是你需要有一个搭建好的Python环境
    -v、version：查看版本信息
    -a、author：作者信息
    -l、license：查看许可证
    -h、help：帮助
    -w、where：查看Cleave的路径
    -t、list：查看插件列表
  ''';

  static const Map<int, String> commandDescriptions = {
    0: '无命令启动',
    1: '启动excel核心',
    2: '插件拓展部件',
    3: '打开拓展编辑器',
    4: '使用调试功能，前提是你需要有一个搭建好的Python环境',
    5: '查看版本信息',
    6: '作者信息',
    7: '查看许可证',
    8: outlines,
    9: '查看Cleave的路径',
    10: '查看插件列表'
  };

  // 解析命令行参数
  static int analysisOrders(List<String> args) {
    final parser = ArgParser();
    parser.addFlag('excel', abbr: 'e', negatable: false, help: '启动excel核心');
    parser.addFlag('plugin', abbr: 'p', negatable: false, help: '插件拓展部件');
    parser.addFlag('cml', abbr: 'c', negatable: false, help: '打开拓展编辑器');
    parser.addFlag('debug', abbr: 'd', negatable: false, help: '使用调试功能，需要有一个搭建好的Python环境');
    parser.addFlag('version', abbr: 'v', negatable: false, help: '查看版本信息');
    parser.addFlag('author', abbr: 'a', negatable: false, help: '作者信息');
    parser.addFlag('license', abbr: 'l', negatable: false, help: '查看许可证');
    parser.addFlag('help', abbr: 'h', negatable: false, help: '帮助');
    parser.addFlag('where', abbr: 'w', negatable: false, help: '查看Cleave的路径');
    parser.addFlag('list', abbr: 't', negatable: false, help: '查看插件列表');

    final results = parser.parse(args);

    if (results['excel']) return 1;
    else if (results['plugin']) return 2;
    else if (results['cml']) return 3;
    else if (results['debug']) return 4;
    else if (results['version']) return 5;
    else if (results['author']) return 6;
    else if (results['license']) return 7;
    else if (results['help']) return 8;
    else if (results['where']) return 9;
    else if (results['list']) return 10;
    else {
      throw Exception('没有此类命令');
    }
  }

  // 打印帮助信息
  static void printHelp() {
    print(outlines);
  }

  // 打印命令描述
  static void printCommandDescription(int command) {
    if (commandDescriptions.containsKey(command)) {
      print(commandDescriptions[command]);
    } else {
      throw Exception('没有此类命令');
    }
  }
}

void main(List<String> args) {
  try {
    final command = OrderLines.analysisOrders(args);
    OrderLines.printCommandDescription(command);
  } catch (e) {
    print(e);
    OrderLines.printHelp();
  }
}
