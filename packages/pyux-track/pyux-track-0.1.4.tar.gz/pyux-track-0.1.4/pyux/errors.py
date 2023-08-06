
class ColorValueError(ValueError):
    """Color is not available for ColourPen."""


class StyleValueError(ValueError):
    """Style is not available for ColourPen."""


class NoDurationsError(ValueError):
    """Durations were not yet computed in Chronos."""


class DelayTypeError(TypeError):
    """No delay was given to Timer."""


class TimeoutThreadError(TimeoutError):
    """Fail to start thread for timeout decorator"""
