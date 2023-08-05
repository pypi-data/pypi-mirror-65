from abc import ABCMeta
from typing import Type


def make_qt_abc_meta(cls: Type):
    """
    Factory method for creating common meta classes for abstract classes
    which are derived from qt classes.
    This is a workaround for solving meta class conflicts when creating
    Abstract Meta Classes based on Qt Classes.

    Args:
        cls: Qt Type which should be used to create the Meta Class.

    Examples:

    class MyClass(ABC,
                  Qt.QWidgets,
                  metaclass=make_qt_abc_meta(cls=QtWidgets.QWidget)):
        pass

    where make_qt_abc_meta() creates a class looking like:

    class QtAbcMeta(type(QtWidgets.QWidget), ABCMeta):
        pass

    which is equivalent to:

    class MyClass(ABC, Qt.QWidgets, metaclass=QtAbcMeta)
        pass
    """
    class QtAbcMeta(type(cls), ABCMeta):  # type: ignore
        pass
    return QtAbcMeta
