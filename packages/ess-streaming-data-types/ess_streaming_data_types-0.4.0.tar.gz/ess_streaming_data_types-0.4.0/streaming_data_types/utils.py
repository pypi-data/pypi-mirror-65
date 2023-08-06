def _get_schema(buffer) -> str:
    """
    Extract the schema code embedded in the buffer

    :param buffer: The raw buffer of the FlatBuffers message.
    :return: The schema identifier
    """
    return buffer[4:8].decode("utf-8")


def check_schema_identifier(buffer, expected_identifer: bytes):
    """
    Check the schema code embedded in the buffer matches an expected identifier

    :param buffer: The raw buffer of the FlatBuffers message
    :param expected_identifer: The expected flatbuffer identifier
    """
    if _get_schema(buffer) != expected_identifer.decode():
        raise RuntimeError(
            f"Incorrect schema: expected {expected_identifer} but got {_get_schema(buffer)}"
        )
