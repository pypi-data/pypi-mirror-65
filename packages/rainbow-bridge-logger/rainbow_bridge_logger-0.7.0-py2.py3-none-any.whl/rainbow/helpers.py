import os


def _get_color(color=None):
  """Get color name from pre-defined color list"""
  if color == False or os.environ.get("RAINBOW_LOGGER_NO_COLOR") or color == "":
    return ""

  if color is None and not color:
    raise ValueError("Must have color code")

  colors = {
    "PURPLE":"\033[96m",
    "MAGENTA":"\033[95m",
    "BLUE":"\033[94m",
    "GREEN":"\033[92m",
    "YELLOW":"\033[93m",
    "RED":"\033[91m",
    "DARKGRAY":"\033[90m",
    "GREY":"\033[0m",
    "WHITE":"\033[1m"
  }

  if color not in colors:
    raise KeyError("Use a proper color name: {}".format(list(colors.keys())))

  return colors[color]


def _get_message(no_time=False, no_color=False):
  """Get message parts"""
  time = "{}%(asctime)s{}".format(
    _get_color(not no_color and "DARKGRAY"),
    _get_color(not no_color and "GREY")
  )

  name = "{}%(name)-12s{}".format(
    _get_color(not no_color and "PURPLE"),
    _get_color(not no_color and "GREY")
  )

  level = "%(levelname)-8s"
  message = "%(message)s"

  if os.environ.get("RAINBOW_LOGGER_NO_TIME") == "true" or no_time:
    return "{} {}\t{}".format(name, level, message)

  return "{} {} {}\t{}".format(time, name, level, message)


def _set_level_format(level=None, color="", no_color=False, logging_module=None):
  """Set logging format based on level and color"""
  FORMAT = "{}{}{}"
  LEVEL_MAPPING = {
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
  }

  _logging_module = logging_module
  parsed_format = FORMAT.format(
    _get_color(not no_color and color),
    LEVEL_MAPPING[level],
    _get_color(not no_color and "GREY")
  )


  if level is not None:
    _logging_module.addLevelName(level, parsed_format)

  return True
