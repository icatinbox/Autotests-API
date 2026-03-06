from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DirectoryTest(BaseModel):
    testId: int = Field(ge = 0)
    name: str
    isCustom: bool

    model_config = ConfigDict(extra='forbid')

class DirectoryGrade(BaseModel):
    gradeId: int = Field(ge = 0)
    name: str
    order: int

    model_config = ConfigDict(extra='forbid')

class File(BaseModel):
    fileId: int = Field(ge = 0)
    fileName: str

class TestAssignment(BaseModel):
    model_config = ConfigDict(extra='forbid')

    testAssignmentId: int = Field(ge = 0)
    testHistoryId: int = Field(ge = 0)
    jobId: int = Field(ge = 0)
    testName: str
    gradeName: str | None = None
    assignedAt: datetime
    gradeAt: datetime | None = None
    comment: str | None = None
    isEditable: bool
    files: List[File]