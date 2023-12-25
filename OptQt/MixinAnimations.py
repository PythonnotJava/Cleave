from typing import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 动画类
class OptAniamtion(QPropertyAnimation):
    def __init__(self,
                 _type: str,
                 target: QObject,
                 start: {QRect, QPoint, QPointF, QSize},
                 end: {QRect, QPoint, QPointF, QSize},
                 duration: int = 1000,
                 loop: int = 1,
                 objectName: Optional[str] = None,
                 easingCurve: QEasingCurve | Type | int = QEasingCurve.OutBack
                 ):
        super().__init__()

        self.setPropertyName(_type.encode())
        self.setTargetObject(target)
        self.setStartValue(start)
        self.setEndValue(end)
        self.setDuration(duration)
        self.setLoopCount(loop)

        if easingCurve is not None:
            self.setEasingCurve(easingCurve)

        if objectName is not None:
            self.setObjectName(objectName)


class OptParallelAniamtionGroup(QParallelAnimationGroup):
    def __init__(self, animations: Iterator):
        super().__init__()
        for animation in animations:
            self.addAnimation(animation)


class OptSeqAniamtionGroup(QSequentialAnimationGroup):
    def __init__(self, animations: Iterator):
        super().__init__()
        for animation in animations:
            self.addAnimation(animation)


# 从某点开始展开（收紧）并放大（消失）的动画
class ZoomAnimation(OptAniamtion):
    def __init__(self,
                 start: QPoint,
                 end: QPoint,
                 toSize: QSize,
                 target: QObject,
                 duration: int = 1000,
                 loop: int = 1,
                 objectName: Optional[str] = None,
                 baseSize: QSize = QSize(50, 50)
                 ):
        super().__init__(
            _type='geometry',
            target=target,
            start=QRect(start, baseSize),
            end=QRect(end, toSize),
            duration=duration,
            loop=loop,
            objectName=objectName
        )


# 带有透明度变化的ZoomAnimation
class ZoomAnimationWithAlpha(QParallelAnimationGroup):
    def __init__(self,
                 start: QPoint,
                 end: QPoint,
                 toSize: QSize,
                 target: QObject,
                 target2: QObject,
                 duration: int = 1000,
                 duration2: int = 1000,
                 loop: int = 1,
                 initialAlpha: float = 1,
                 finalAlpha: float = 0,
                 objectName: Optional[str] = None,
                 baseSize: QSize = QSize(50, 50)
                 ):
        super().__init__()
        self.addAnimation(
            ZoomAnimation(
                start=start,
                end=end,
                toSize=toSize,
                target=target,
                duration=duration,
                baseSize=baseSize
            )
        )

        self.addAnimation(
            OptAniamtion(
                _type='windowOpacity',
                target=target2,
                start=initialAlpha,
                end=finalAlpha,
                duration=duration2,
            )
        )

        if objectName is not None:
            self.setObjectName(objectName)
        self.setLoopCount(loop)


# 从某点开始向周围展开的动画
class ExpandAnimation(OptAniamtion):
    def __init__(self,
                 initialPoint: QPoint,
                 expand_quarter: list[int, int],
                 target: QObject,
                 duration: int = 1000,
                 loop: int = 1,
                 objectName: Optional[str] = None
                 ):
        """
        :param initialPoint: 起点
        :param expand_quarter: 一个二元列表，分别表示上下扩散半径和左右扩散半径
        :param target: ...
        :param duration: ...
        :param loop: ...
        :param objectName: ...
        """
        super().__init__(
            _type='geometry',
            target=target,
            start=QRect(initialPoint, QSize(0, 0)),
            end=QRect(initialPoint - QPoint(expand_quarter[1], expand_quarter[0]),
                      QSize(2 * expand_quarter[1], 2 * expand_quarter[0])),
            duration=duration,
            loop=loop,
            objectName=objectName
        )


# 从某点开始向周围展开的动画并带有透明度渐变
class ExpandAnimationWithAlpha(QParallelAnimationGroup):
    def __init__(self,
                 initialPoint: QPoint,
                 expand_quarter: list[int, int],
                 target: QObject,
                 target2: QObject,
                 duration: int = 1000,
                 duration2: int = 1000,
                 loop: int = 1,
                 objectName: Optional[str] = None,
                 initialAlpha: float = 1,
                 finalAlpha: float = 0,
                 ):
        super().__init__()
        self.addAnimation(
            ExpandAnimation(
                initialPoint=initialPoint,
                expand_quarter=expand_quarter,
                duration=duration,
                target=target,
            )
        )

        self.addAnimation(
            OptAniamtion(
                _type='windowOpacity',
                target=target2,
                start=initialAlpha,
                end=finalAlpha,
                duration=duration2,
            )
        )

        if objectName is not None:
            self.setObjectName(objectName)
        self.setLoopCount(loop)


# 创建完成后整体弹射出来的动画
class FlyAnimation(OptAniamtion):
    def __init__(self,
                 start: QPoint,
                 end: QPoint,
                 target: QObject,
                 duration: int = 1000,
                 loop: int = 1,
                 objectName: Optional[str] = None
                 ):
        super().__init__(
            _type='point',
            start=start,
            end=end,
            target=target,
            duration=duration,
            loop=loop,
            objectName=objectName
        )


if __name__ == '__main__':
    app = QApplication([])
    ui = QWidget()
    ui.setGeometry(QRect(400, 300, 800, 600))
    btn = QPushButton(ui)
    btn.setStyleSheet('background-color : black')
    btn.setGeometry(QRect(200, 150, 1, 1))
    # ani = ZoomAnimationWithAlpha(
    #     start=QPoint(10, 10),
    #     end=QPoint(400, 200),
    #     toSize=QSize(400, 400),
    #     initialAlpha=1,
    #     finalAlpha=.5,
    #     target=ui,
    #     duration=600
    # )

    # ani = ExpandAnimation(
    #     initialPoint=QPoint(200, 150),
    #     expand_quarter=[50, 60],
    #     target=btn,
    #     duration=2000,
    # )

    ani = ExpandAnimationWithAlpha(
        initialPoint=QPoint(200, 150),
        expand_quarter=[50, 60],
        target=btn,
        duration=2000,
        duration2=5000,
        initialAlpha=1,
        finalAlpha=.1,
        target2=ui
    )
    ani.start()
    ui.show()
    app.exec()
