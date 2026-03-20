from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class SynchronizationOnPublicationSiteResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: int
    messages: Optional[Any] = None


class CandidateStatusSla(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    candidateStatusId: int
    jobId: Optional[int] = None
    slaTime: int


class CandidateHistory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidateHistoryId: int
    statusId: Optional[int] = None
    jobId: Optional[int] = None
    jobName: Optional[str] = None
    organizationUnit: Optional[Any] = None
    candidateId: int
    dateCreated: datetime
    eventType: int
    rating: Optional[Any] = None
    description: str

    fromDate: Optional[datetime] = None
    toDate: Optional[datetime] = None

    workdaysBetween: int
    isClosed: int
    accountId: int
    isAllDay: int

    fields: str | None = None

    responsibleId: int
    notificationSettings: Optional[Any] = None
    invited: Optional[Any] = None
    alternativeAuthor: Optional[Any] = None

    isStatusSynchronizationOnPublicationSiteEnabled: bool
    synchronizationOnPublicationSiteResult: SynchronizationOnPublicationSiteResult | None = None

    assignedTests: Optional[Any] = None
    testAssignments: list[Any]

    isClosingVacancy: bool
    candidateStatusSla: Optional[CandidateStatusSla] = None

    isAvailableJob: bool

    sodPackagePriority: Optional[Any] = None
    sodVsp: Optional[Any] = None
    sodBoxNumber: Optional[Any] = None
    sodCorrectionListNumber: Optional[Any] = None
    offerPlannedDate: Optional[datetime] = None
    sodFiles: Optional[Any] = None
    approvalTrigger: Optional[Any] = None

    hireTermId: Optional[int] = None
    reasonId: Optional[int] = None
    youthProgramParticipation: Optional[Any] = None
    isYouthProgramEvent: bool
    youthProgramId: Optional[int] = None
    jobType: Optional[int] = None
    employmentConditionId: Optional[int] = None


class ActiveCandidateHistoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidateHistory: CandidateHistory
    activeCandidateStatusId: int
    candidateStatusId: int
    jobId: int
    candidateId: int
    dateCreated: datetime
    candidateHistoryId: int
    closedAt: int | None = None

    # новое поле из ответа
    jobType: Optional[int] = None


class FeedResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activeCandidateHistories: list[ActiveCandidateHistoryItem]
    candidateHistories: list[CandidateHistory]

    applications: list[Any]
    emails: list[Any]
    shortMessages: list[Any]
    telegramMessages: list[Any]

    isProcessedByConfidentialJob: bool