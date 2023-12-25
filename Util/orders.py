# about cleave
def about() -> str:
    __ind__ = """           
    \033[1;31;40m                                                                                                                                                  
      ,----..    ,--,                                              
     /   /   \ ,--.'|                                              
    |   :     :|  | :                                              
    .   |  ;. /:  : '                              .---.           
    .   ; /--` |  ' |      ,---.     ,--.--.     /.  ./|   ,---.   
    ;   | ;    '  | |     /     \   /       \  .-' . ' |  /     \  
    |   : |    |  | :    /    /  | .--.  .-. |/___/ \: | /    /  | 
    .   | '___ '  : |__ .    ' / |  \__\/: . ..   \  ' ..    ' / | 
    '   ; : .'||  | '.'|'   ;   /|  ," .--.; | \   \   ''   ;   /| 
    '   | '/  :;  :    ;'   |  / | /  /  ,.  |  \   \   '   |  / | 
    |   :    / |  ,   / |   :    |;  :   .'   \  \   \ ||   :    | 
     \   \ .'   ---`-'   \   \  / |  ,     .-./   '---"  \   \  /  
      `---`               `----'   `--`---'               `----'    
  
    \033[0m      
    \033[31m                        
    *******************************************************************
            version = '1.1',
            author = 'A Lucky Boy',
            Platform = 'Windows 10 at least',
            __start_date__ = '2022/10/28',
            executable = 'Cleave.exe',
            name="Cleave",
            description="Analysis and design of data
            __ = "I will always love Python."
    *******************************************************************
    \033[0m        
    """
    return __ind__

def getInfos() -> dict:
    version = '1.1',
    author = 'A Lucky Boy',
    Platform = 'Windows 10 at least',
    __start_date__ = '2022/10/28',
    name = "Cleave",
    description = "Analysis and design of data"
    __ = "I will always love Python."

    return {
        'version' : version,
        'author' : author,
        'Platform' : Platform,
        'date' : __start_date__,
        'name' : name,
        'description' : description,
        'start' : __
    }

# 新添加
def endOf():
    description = "Give up today……"
    __end_date__ = '2023/12/25',
    return {
        description: "Give up today……",
        __end_date__ : '2023/12/25',
    }
