def test_console_named_logger():
  from rainbow import RainbowLogger
  logger = RainbowLogger("rainbow")
  logger.info("my info")
  logger.warning("my warn")
  logger.error("my error")
  logger.debug("my debug")
  logger.critical("my critical")


def test_file_named_logger():
  from rainbow import RainbowLogger
  logger = RainbowLogger("rainbow", filepath="rainbow.named.log")
  logger.info("my info")
  logger.warning("my warn")
  logger.error("my error")
  logger.debug("my debug")
  logger.critical("my critical")


def test_console_root_logger():
  from rainbow import RainbowLogger
  logger = RainbowLogger()
  logger.info("root info")
  logger.warning("root warn")
  logger.error("root error")
  logger.debug("root debug")
  logger.critical("root critical")


def test_file_root_logger():
  from rainbow import RainbowLogger
  logger = RainbowLogger(filepath="rainbow.root.log")
  logger.info("root info")
  logger.warning("root warn")
  logger.error("root error")
  logger.debug("root debug")
  logger.critical("root critical")


if __name__ == "__main__":
  test_console_named_logger()
  test_file_named_logger()

  test_console_root_logger()
  test_file_root_logger()
