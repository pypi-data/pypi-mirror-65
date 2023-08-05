import os
import sys
from .helpers import _set_level_format
from .helpers import _get_message


class RainbowLogger:
  """A customized logger built on top of Python's logging"""
  def __new__(
    cls,
    name=None,
    no_time=False,
    no_color=False,
    new_logging=None,
    filepath=None,
    log_level=None,
    get_logging=False
  ):
    import logging


    if not log_level:
      log_level = logging.DEBUG

    _logging_module = logging
    if new_logging is not None:
      _logging_module = new_logging

    if filepath:
      no_color = True

    level_color_mapping = [
      {"level": _logging_module.DEBUG, "color": "BLUE"},
      {"level": _logging_module.INFO, "color": "GREEN"},
      {"level": _logging_module.WARN, "color": "YELLOW"},
      {"level": _logging_module.ERROR, "color": "RED"},
      {"level": _logging_module.CRITICAL, "color": "MAGENTA"}
    ]

    for l in level_color_mapping:
      _set_level_format(
        level=l['level'],
        color=l["color"],
        no_color=no_color,
        logging_module=_logging_module
      )

    logger = _logging_module.getLogger(name)
    logger.setLevel(log_level)

    log_level = log_level if log_level else _logging_module.DEBUG
    if 'RAINBOW_LEVEL' in os.environ:
      log_level = getattr(
        _logging_module,
        os.environ["RAINBOW_LEVEL"],
        "DEBUG"
      )

    final_message = ""

    # remove existing handlers
    [logger.removeHandler(h) for h in logger.handlers]

    if not filepath and name:
      handler = _logging_module.StreamHandler(sys.stdout)
      final_message = _get_message(no_time, no_color)
      formatter = _logging_module.Formatter(final_message)
      handler.setFormatter(formatter)
      handler.setLevel(log_level)
      logger.addHandler(handler)
    elif filepath and name:
      # console logs on critical
      handler = _logging_module.StreamHandler()
      final_message = _get_message(no_time, no_color)
      formatter = _logging_module.Formatter(final_message)
      handler.setFormatter(formatter)
      handler.setLevel(_logging_module.CRITICAL)
      logger.addHandler(handler)

      handler = _logging_module.FileHandler(filepath)
      final_message = _get_message(no_time, no_color)
      formatter = _logging_module.Formatter(final_message)
      handler.setFormatter(formatter)
      handler.setLevel(log_level)
      logger.addHandler(handler)

    if not name:
      final_message = _get_message(no_time, no_color)
      config = {
        "format": final_message,
        "level": log_level,
        "filemode": "a",
      }

      if filepath:
        config["filename"] = filepath

      _logging_module.basicConfig(**config)

    if get_logging:
      return _logging_module

    return logger
