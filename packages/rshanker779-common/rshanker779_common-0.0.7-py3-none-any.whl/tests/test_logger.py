import rshanker779_common as utils


def test_clear_handler():
    logger = utils.get_logger(__name__)
    logger = utils.clear_handlers(logger)
    assert not logger.handlers
