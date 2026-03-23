from data_structures import ACCOUNT_ID
from tests.utils.utils import content_to_sql_binary

SQL_INSERT_CANDIDATE = """
    DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
    INSERT INTO dbo.Candidates (
        AccountId,
        ClientId,
        CandidateStatusId,
        CVId,
        Salary,
        Employment,
        Schedule,
        Place,
        Sex,
        VKCity,
        BusinessTrip,
        BirthDate,
        DateCreated,
        LastUpdate,
        Experience,
        FirstName,
        LastName,
        AddWay,
        Currency
    )
    OUTPUT INSERTED.CandidateId
    VALUES (
        0,
        1000002,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        @Now,
        @Now,
        0,
        N'Имя_',
        N'Фамилия_' + REPLACE(CONVERT(nvarchar(36), NEWID()), '-', ''),
        N'Отклик',
        0
    );
"""

def sql_insert_vacancy(cursor):
    query = """
        DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
        INSERT INTO dbo.Jobs (
            Status,
            AccountId,
            Name,
            CustomerId,
            ResponsibleId,
            FromDate,
            PositionCount,
            IsConfidential,
            TravelWorkType
        )
        OUTPUT INSERTED.JobId
        VALUES (
            1,
            ?,
            N'Тестовая вакансия ' + REPLACE(CONVERT(nvarchar(36), NEWID()), '-', ''),
            0,
            ?,
            @Now,
            1,
            0,
            0
        );
    """
    cursor.execute(query, ACCOUNT_ID, ACCOUNT_ID)
    return cursor.fetchone()[0]
def sql_insert_candidate_history(cursor, status, job_id, candidate_id, reason_id):
    query = """
        DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
        INSERT INTO dbo.CandidateHistories (
            CandidateStatusId,
            JobId,
            CandidateId,
            DateCreated,
            EventType,
            Description,
            FromDate,
            AccountId,
            IsAllDay,
            ResponsibleId,
            ReasonId
        )
        OUTPUT INSERTED.CandidateHistoryId
        VALUES (?, ?, ?, @Now, 0, N'',
            @Now, ?, 0, ?, ?);
    """
    cursor.execute(query, status, job_id, candidate_id, ACCOUNT_ID, ACCOUNT_ID, reason_id)
    return cursor.fetchone()[0]
def sql_insert_active_candidate_status(cursor, status, job_id, candidate_id, history_id):
    query = """
        DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
        INSERT INTO dbo.ActiveCandidateStatus(
            CandidateStatusId,
            JobId,
            CandidateId,
            DateCreated,
            CandidateHistoryId,
            ClosedAt
        )
        OUTPUT INSERTED.ActiveCandidateStatusId
        VALUES (?, ?, ?, @Now, ?, NULL);
    """
    cursor.execute(query, status, job_id, candidate_id, history_id)
    return cursor.fetchone()[0]
def sql_insert_test(cursor, candidate_id, job_id, test_id, ch_id):
    query = """
        DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
        INSERT INTO CandidateTestAssignments(
            CandidateId,
            JobId,
            TestId,
            GroupParentHistoryId,
            AssignedAt,
            CreatedAt,
            UpdatedAt,
            IsDeleted,
            Comment
        )
        OUTPUT INSERTED.TestAssignmentId
        VALUES (?, ?, ?, ?,
            @Now , @Now , @Now , 0,
            N'Я в своем познании настолько преисполнился, что уверен в прохождении теста');
    """
    cursor.execute(query, candidate_id, job_id, test_id, ch_id)
    return cursor.fetchone()[0]
def sql_insert_test_file(cursor, test_assignment_id):
    object_id = f'assignment_{test_assignment_id}'
    content = content_to_sql_binary('Этот тест самый тестовый в мире!')
    query = """
        DECLARE @Now datetime2(0) = CAST(GETDATE() AS datetime2(0));
        INSERT INTO dbo.Files (
            Name,
            Content,
            ObjectId,
            CreationTime,
            ModificationTime,
            IsConfidential
        )
        OUTPUT INSERTED.Id
        VALUES (N'Тестовый файл.pdf', ?, ?, @Now, @Now, 0);
    """
    cursor.execute(query, content, object_id)
    return cursor.fetchone()[0]