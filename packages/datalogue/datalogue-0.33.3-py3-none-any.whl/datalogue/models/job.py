from datetime import datetime
from uuid import UUID
from typing import Union, Optional

from dateutil.parser import parse

from datalogue.utils import SerializableStringEnum
from datalogue.errors import _enum_parse_error, DtlError


class JobStatus(SerializableStringEnum):
    Scheduled = "Scheduled"
    Defined = "Defined"
    Running = "Running"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Unknown = "Unknown"
    Cancelled = "Cancelled"

    @staticmethod
    def parse_error(s: str) -> str:
        return DtlError(_enum_parse_error("job status", s))

    @staticmethod
    def job_status_from_str(string: str) -> Union[DtlError, 'JobStatus']:
        return SerializableStringEnum.from_str(JobStatus)(string)


class Job:
    def __init__(self, stream_id: Optional[UUID], run_at: datetime, status: JobStatus,
                 stream_collection_id: Optional[UUID], id: UUID, remaining_time_millis: int, percentage_progress: int,
                 created_by: UUID, errors: Optional[str], ended_at: Optional[datetime], started_at: Optional[datetime]):
        self.stream_id = stream_id
        self.stream_collection_id = stream_collection_id
        self.status = status
        self.run_at = run_at
        self.id = id
        self.remaining_time_millis = remaining_time_millis
        self.percentage_progress = percentage_progress
        self.created_by = created_by
        self.errors = errors
        self.ended_at = ended_at
        self.started_at = started_at

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'id: {self.id!r}, '
                f'stream_id: {self.stream_id!r}, '
                f'stream_collection_id: {self.stream_collection_id!r}, '
                f'status: {self.status!r}, '
                f'run_at: {self.run_at!r}, '
                f'created_by: {self.created_by!r}, '
                f'remaining_time_millis: {self.remaining_time_millis!r}, '
                f'percent_progress: {self.percentage_progress!r}, '
                f'errors: {self.errors!r}, '
                f'ended_at: {self.ended_at!r}, '
                f'started_at: {self.started_at!r})')


def _job_from_payload(json: dict) -> Union[DtlError, Job]:
    stream_id = json.get('streamId')
    if stream_id is not None:
        try:
            stream_id = UUID(stream_id)
        except ValueError:
            return DtlError("'streamId' field was not a proper uuid")

    run_at = json.get("runDate")
    if run_at is None:
        return DtlError("Job object should have a 'runDate' property")
    else:
        try:
            run_at = parse(run_at)
        except ValueError:
            return DtlError("The 'runDate' could not be parsed as a valid date")

    status = json.get("status")
    if status is None:
        return DtlError("Job object should have a 'status' property")
    else:
        status = JobStatus.job_status_from_str(status)
        if isinstance(status, DtlError):
            return status

    stream_collection_id = json.get("streamCollectionId")
    if stream_collection_id is not None:
        try:
            stream_collection_id = UUID(stream_collection_id)
        except ValueError:
            return DtlError("'streamCollectionId' field was not a proper uuid")

    job_id = json.get('jobId')
    if job_id is None:
        return DtlError("Job object should have a 'jobId' property")
    else:
        try:
            job_id = UUID(job_id)
        except ValueError:
            return DtlError("'jobId' field was not a proper uuid")

    remaining_time_millis = json.get('remainingTimeInMillis')
    if remaining_time_millis is None:
        return DtlError("Job object should have a 'remainingTimeInMillis' property")
    else:
        try:
            remaining_time_millis = int(remaining_time_millis)
        except ValueError:
            return DtlError("'remainingTimeInMillis' was not a proper int")

    percentage_progress = json.get('percentage')
    if percentage_progress is None:
        return DtlError("Job object should have a 'percentProgress' property")
    else:
        try:
            percentage_progress = int(percentage_progress)
        except ValueError:
            return DtlError("'percentProgress' was not a proper int")

    created_by = json.get('createdBy')
    if created_by is None:
        return DtlError("Job object should have a 'createdBy' property")
    else:
        try:
            created_by = UUID(created_by)
        except ValueError:
            return DtlError("'createdBy' was not a proper uuid")

    # details is optional
    errors = json.get('details')

    # ended_at is optional
    ended_at = json.get("endDate")
    if ended_at is not None:
        try:
            ended_at = parse(ended_at)
        except ValueError:
            return DtlError("The 'endDate' could not be parsed as a valid date")

    # started_at is optional
    started_at = json.get("startDate")
    if started_at is not None:
        try:
            started_at = parse(started_at)
        except ValueError:
            return DtlError("The 'startDate' could not be parsed as a valid date")

    return Job(stream_id, run_at, status, stream_collection_id, job_id,
               remaining_time_millis, percentage_progress, created_by, errors, ended_at, started_at)
