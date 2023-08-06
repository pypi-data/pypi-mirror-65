from functools import reduce
import operator
import flatbuffers
import numpy
import streaming_data_types.fbschemas.histogram_hs00.ArrayDouble as ArrayDouble
import streaming_data_types.fbschemas.histogram_hs00.ArrayULong as ArrayULong
import streaming_data_types.fbschemas.histogram_hs00.DimensionMetaData as DimensionMetaData
import streaming_data_types.fbschemas.histogram_hs00.EventHistogram as EventHistogram
from streaming_data_types.fbschemas.histogram_hs00.Array import Array
from streaming_data_types.utils import check_schema_identifier


FILE_IDENTIFIER = b"hs00"


def deserialise_hs00(buffer):
    """
    Deserialise flatbuffer hs10 into a histogram.

    :param buffer:
    :return: dict of histogram information
    """
    check_schema_identifier(buffer, FILE_IDENTIFIER)
    event_hist = EventHistogram.EventHistogram.GetRootAsEventHistogram(buffer, 0)

    dims = []
    for i in range(event_hist.DimMetadataLength()):
        bins_fb = ArrayDouble.ArrayDouble()
        if (
            event_hist.DimMetadata(i).BinBoundariesType() == Array.ArrayUInt
            or event_hist.DimMetadata(i).BinBoundariesType() == Array.ArrayULong
        ):
            bins_fb = ArrayULong.ArrayULong()

        # Get bins
        bins_offset = event_hist.DimMetadata(i).BinBoundaries()
        bins_fb.Init(bins_offset.Bytes, bins_offset.Pos)
        bin_boundaries = bins_fb.ValueAsNumpy()

        hist_info = {
            "length": event_hist.DimMetadata(i).Length(),
            "bin_boundaries": bin_boundaries,
            "unit": event_hist.DimMetadata(i).Unit().decode("utf-8")
            if event_hist.DimMetadata(i).Unit()
            else "",
            "label": event_hist.DimMetadata(i).Label().decode("utf-8")
            if event_hist.DimMetadata(i).Label()
            else "",
        }
        dims.append(hist_info)

    metadata_timestamp = event_hist.LastMetadataTimestamp()

    data_fb = ArrayDouble.ArrayDouble()
    if (
        event_hist.DataType() == Array.ArrayUInt
        or event_hist.DataType() == Array.ArrayULong
    ):
        data_fb = ArrayULong.ArrayULong()

    data_offset = event_hist.Data()
    data_fb.Init(data_offset.Bytes, data_offset.Pos)
    shape = event_hist.CurrentShapeAsNumpy().tolist()
    data = data_fb.ValueAsNumpy().reshape(shape)

    # Get the errors
    errors_offset = event_hist.Errors()
    if errors_offset:
        errors_fb = ArrayDouble.ArrayDouble()
        if (
            event_hist.DataType() == Array.ArrayUInt
            or event_hist.DataType() == Array.ArrayULong
        ):
            errors_fb = ArrayULong.ArrayULong()
        errors_fb.Init(errors_offset.Bytes, errors_offset.Pos)
        errors = errors_fb.ValueAsNumpy().reshape(shape)
    else:
        errors = []

    hist = {
        "source": event_hist.Source().decode("utf-8") if event_hist.Source() else "",
        "timestamp": event_hist.Timestamp(),
        "current_shape": shape,
        "dim_metadata": dims,
        "data": data,
        "errors": errors,
        "last_metadata_timestamp": metadata_timestamp,
        "info": event_hist.Info().decode("utf-8") if event_hist.Info() else "",
    }
    return hist


def _serialise_metadata(builder, length, edges, unit, label):
    unit_offset = builder.CreateString(unit)
    label_offset = builder.CreateString(label)

    if isinstance(edges[0], int) or (
        isinstance(edges, numpy.ndarray) and numpy.issubdtype(edges[0], numpy.int64)
    ):
        bin_type = Array.ArrayULong
        ArrayULong.ArrayULongStartValueVector(builder, len(edges))
        # FlatBuffers builds arrays backwards
        for x in reversed(edges):
            builder.PrependUint64(x)
        bins_vector = builder.EndVector(len(edges))
        # Add the bins
        ArrayULong.ArrayULongStart(builder)
        ArrayULong.ArrayULongAddValue(builder, bins_vector)
        bins_offset = ArrayULong.ArrayULongEnd(builder)
    else:
        bin_type = Array.ArrayDouble
        ArrayDouble.ArrayDoubleStartValueVector(builder, len(edges))
        # FlatBuffers builds arrays backwards
        for x in reversed(edges):
            builder.PrependFloat64(x)
        bins_vector = builder.EndVector(len(edges))
        # Add the bins
        ArrayDouble.ArrayDoubleStart(builder)
        ArrayDouble.ArrayDoubleAddValue(builder, bins_vector)
        bins_offset = ArrayDouble.ArrayDoubleEnd(builder)

    DimensionMetaData.DimensionMetaDataStart(builder)
    DimensionMetaData.DimensionMetaDataAddLength(builder, length)
    DimensionMetaData.DimensionMetaDataAddBinBoundaries(builder, bins_offset)
    DimensionMetaData.DimensionMetaDataAddBinBoundariesType(builder, bin_type)
    DimensionMetaData.DimensionMetaDataAddLabel(builder, label_offset)
    DimensionMetaData.DimensionMetaDataAddUnit(builder, unit_offset)
    return DimensionMetaData.DimensionMetaDataEnd(builder)


def serialise_hs00(histogram):
    """
    Serialise a histogram as an hs00 FlatBuffers message.

    :param histogram: A dictionary containing the histogram to serialise.
    """
    source_offset = None
    info_offset = None

    builder = flatbuffers.Builder(1024)
    if "source" in histogram:
        source_offset = builder.CreateString(histogram["source"])
    if "info" in histogram:
        info_offset = builder.CreateString(histogram["info"])

    # Build shape array
    rank = len(histogram["current_shape"])
    EventHistogram.EventHistogramStartCurrentShapeVector(builder, rank)
    # FlatBuffers builds arrays backwards
    for s in reversed(histogram["current_shape"]):
        builder.PrependUint32(s)
    shape_offset = builder.EndVector(rank)

    # Build dimensions metadata
    metadata = []
    for meta in histogram["dim_metadata"]:
        unit = "" if "unit" not in meta else meta["unit"]
        label = "" if "label" not in meta else meta["label"]
        metadata.append(
            _serialise_metadata(
                builder, meta["length"], meta["bin_boundaries"], unit, label
            )
        )

    EventHistogram.EventHistogramStartDimMetadataVector(builder, rank)
    # FlatBuffers builds arrays backwards
    for m in reversed(metadata):
        builder.PrependUOffsetTRelative(m)
    metadata_vector = builder.EndVector(rank)

    # Build the data
    data_len = reduce(operator.mul, histogram["current_shape"], 1)
    flattened_data = numpy.asarray(histogram["data"]).flatten()

    if numpy.issubdtype(flattened_data[0], numpy.int64):
        data_type = Array.ArrayULong
        ArrayULong.ArrayULongStartValueVector(builder, data_len)
        # FlatBuffers builds arrays backwards
        for x in reversed(flattened_data):
            builder.PrependUint64(x)
        data_vector = builder.EndVector(data_len)
        ArrayULong.ArrayULongStart(builder)
        ArrayULong.ArrayULongAddValue(builder, data_vector)
        data_offset = ArrayULong.ArrayULongEnd(builder)
    else:
        data_type = Array.ArrayDouble
        ArrayDouble.ArrayDoubleStartValueVector(builder, data_len)
        # FlatBuffers builds arrays backwards
        for x in reversed(flattened_data):
            builder.PrependFloat64(x)
        data_vector = builder.EndVector(data_len)
        ArrayDouble.ArrayDoubleStart(builder)
        ArrayDouble.ArrayDoubleAddValue(builder, data_vector)
        data_offset = ArrayDouble.ArrayDoubleEnd(builder)

    errors_offset = None
    if "errors" in histogram:
        if isinstance(histogram["errors"], numpy.ndarray):
            flattened_data = histogram["errors"].flatten()
        else:
            flattened_data = numpy.asarray(histogram["errors"]).flatten()

        if numpy.issubdtype(flattened_data[0], numpy.int64):
            error_type = Array.ArrayULong
            ArrayULong.ArrayULongStartValueVector(builder, data_len)
            for x in reversed(flattened_data):
                builder.PrependUint64(x)
            errors = builder.EndVector(data_len)
            ArrayULong.ArrayULongStart(builder)
            ArrayULong.ArrayULongAddValue(builder, errors)
            errors_offset = ArrayULong.ArrayULongEnd(builder)
        else:
            error_type = Array.ArrayDouble
            ArrayDouble.ArrayDoubleStartValueVector(builder, data_len)
            for x in reversed(flattened_data):
                builder.PrependFloat64(x)
            errors = builder.EndVector(data_len)
            ArrayDouble.ArrayDoubleStart(builder)
            ArrayDouble.ArrayDoubleAddValue(builder, errors)
            errors_offset = ArrayDouble.ArrayDoubleEnd(builder)

    # Build the actual buffer
    EventHistogram.EventHistogramStart(builder)
    if info_offset:
        EventHistogram.EventHistogramAddInfo(builder, info_offset)
    EventHistogram.EventHistogramAddData(builder, data_offset)
    EventHistogram.EventHistogramAddCurrentShape(builder, shape_offset)
    EventHistogram.EventHistogramAddDimMetadata(builder, metadata_vector)
    EventHistogram.EventHistogramAddTimestamp(builder, histogram["timestamp"])
    if source_offset:
        EventHistogram.EventHistogramAddSource(builder, source_offset)
    EventHistogram.EventHistogramAddDataType(builder, data_type)
    if errors_offset:
        EventHistogram.EventHistogramAddErrors(builder, errors_offset)
        EventHistogram.EventHistogramAddErrorsType(builder, error_type)
    if "last_metadata_timestamp" in histogram:
        EventHistogram.EventHistogramAddLastMetadataTimestamp(
            builder, histogram["last_metadata_timestamp"]
        )
    hist_message = EventHistogram.EventHistogramEnd(builder)
    builder.Finish(hist_message)

    # Generate the output and replace the file_identifier
    buffer = builder.Output()
    buffer[4:8] = FILE_IDENTIFIER
    return bytes(buffer)
