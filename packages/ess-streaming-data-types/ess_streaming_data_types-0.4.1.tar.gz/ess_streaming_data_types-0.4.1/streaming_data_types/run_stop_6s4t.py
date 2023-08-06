import flatbuffers
from streaming_data_types.fbschemas.run_stop_6s4t import RunStop
from streaming_data_types.utils import check_schema_identifier
from collections import namedtuple

FILE_IDENTIFIER = b"6s4t"


def serialise_6s4t(job_id, run_name="test_run", service_id="", stop_time=None):
    builder = flatbuffers.Builder(136)

    if service_id is None:
        service_id = ""
    if stop_time is None:
        stop_time = 0

    service_id_offset = builder.CreateString(service_id)
    job_id_offset = builder.CreateString(job_id)
    run_name_offset = builder.CreateString(run_name)

    # Build the actual buffer
    RunStop.RunStopStart(builder)
    RunStop.RunStopAddServiceId(builder, service_id_offset)
    RunStop.RunStopAddJobId(builder, job_id_offset)
    RunStop.RunStopAddRunName(builder, run_name_offset)
    RunStop.RunStopAddStopTime(builder, stop_time)

    run_stop_message = RunStop.RunStopEnd(builder)
    builder.Finish(run_stop_message)

    # Generate the output and replace the file_identifier
    buffer = builder.Output()
    buffer[4:8] = FILE_IDENTIFIER
    return bytes(buffer)


def deserialise_6s4t(buffer):
    check_schema_identifier(buffer, FILE_IDENTIFIER)

    run_stop = RunStop.RunStop.GetRootAsRunStop(buffer, 0)
    service_id = run_stop.ServiceId() if run_stop.ServiceId() else b""
    job_id = run_stop.JobId() if run_stop.JobId() else b""
    run_name = run_stop.RunName() if run_stop.RunName() else b""
    stop_time = run_stop.StopTime()

    RunStopInfo = namedtuple("RunStopInfo", "stop_time run_name job_id service_id")
    return RunStopInfo(
        stop_time, run_name.decode(), job_id.decode(), service_id.decode()
    )
