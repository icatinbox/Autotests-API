from src.sql.tables import ALLOWED_TABLES


def sql_delete_by_id(cursor, table, entity_id):
    id_column = ALLOWED_TABLES[table]
    query = f"DELETE FROM {table} WHERE {id_column} = ?"
    cursor.execute(query, entity_id)

def sql_clean_full_history_by_job_id(cursor, job_id: int):
    cursor.execute('SELECT TestAssignmentId FROM CandidateTestAssignments WHERE JobId = ?', job_id)
    ids = cursor.fetchall()
    print("job:", ids)
    for test_id in ids:
        cursor.execute('DELETE FROM Files WHERE ObjectId = ?', f'assignment_{test_id[0]}')
    cursor.execute('DELETE FROM ActiveCandidateStatus WHERE JobId = ?', job_id)
    cursor.execute('DELETE FROM CandidateTestAssignments WHERE JobId = ?', job_id)
    cursor.execute('DELETE FROM CandidateHistories WHERE JobId = ?', job_id)
    cursor.execute('DELETE FROM JobHistories WHERE Job_JobId = ?', job_id)
    cursor.execute('DELETE FROM Jobs WHERE JobId = ?', job_id)

def sql_clean_full_history_by_candidate_id(cursor, candidate_id: int):
    cursor.execute('SELECT TestAssignmentId FROM CandidateTestAssignments WHERE CandidateId = ?', candidate_id)
    ids = cursor.fetchall()
    print("candi:", ids)
    for test_id in ids:
        cursor.execute('DELETE FROM Files WHERE ObjectId = ?', f'assignment_{test_id[0]}')
    cursor.execute('DELETE FROM ActiveCandidateStatus WHERE CandidateId = ?', candidate_id)
    cursor.execute('DELETE FROM CandidateTestAssignments WHERE CandidateId = ?', candidate_id)
    cursor.execute('DELETE FROM CandidateHistories WHERE CandidateId = ?', candidate_id)
    cursor.execute('DELETE FROM Candidates WHERE CandidateId = ?', candidate_id)