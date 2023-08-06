def _get_schema(buffer):
    """
    Extract the schema code embedded in the buffer

    :param buffer: The raw buffer of the FlatBuffers message.
    :return: The schema identifier
    """
    return buffer[4:8].decode("utf-8")


def check_schema_identifier(buffer, expected_identifer):
    """
    Check the schema code embedded in the buffer matches an expected identifier

    :param buffer: The raw buffer of the FlatBuffers message
    :param expected_identifer: The expected flatbuffer identifier
    """
    if _get_schema(buffer) != expected_identifer.decode():
        raise RuntimeError(
            "Incorrect schema: expected {} but got {}".format(
                expected_identifer, _get_schema(buffer)
            )
        )
