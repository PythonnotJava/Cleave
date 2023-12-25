from typing import Optional, Union
class FileLoadError(Exception):
    ...

# 含有代码属性标注的错误
class _ErrorCode(Exception):
    # 0表示非定义错误
    def __init__(self, errorCode : int, fromError : Optional[type[Exception]] = None):
        self.errorCode = errorCode
        self.fromError = fromError

# 上面的解析器
class ErrorCode:
    def __init__(self, ErrorType : Union[Exception, _ErrorCode]):
        if isinstance(ErrorType, _ErrorCode):
            self.__exceptionType = ErrorType
        else:
            self.__exceptionType = _ErrorCode(0)

    @property
    def statusCode(self) -> dict:
        return {"Code" : self.__exceptionType.errorCode}

    def __str__(self):
        return "ErrorCode : %d" % self.__exceptionType.errorCode

