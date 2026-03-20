from src.sql.tables import ALLOWED_TABLES


def sql_delete_by_id(cursor, table, entity_id):
    id_column = ALLOWED_TABLES[table]
    query = f"DELETE FROM {table} WHERE {id_column} = ?"
    cursor.execute(query, entity_id)

def sql_clean_full_history_by_job_id(cursor, job_id: int):
    cursor.execute(f'DELETE FROM ActiveCandidateStatus WHERE JobId = ?', job_id)
    cursor.execute(f'DELETE FROM CandidateTestAssignments WHERE JobId = ?', job_id)
    cursor.execute(f'DELETE FROM CandidateHistories WHERE JobId = ?', job_id)
    cursor.execute(f'DELETE FROM JobHistories WHERE Job_JobId = ?', job_id)
    cursor.execute(f'DELETE FROM Jobs WHERE JobId = ?', job_id)

def sql_clean_full_history_by_candidate_id(cursor, candidate_id: int):
    cursor.execute(f'DELETE FROM ActiveCandidateStatus WHERE CandidateId = ?', candidate_id)
    cursor.execute(f'DELETE FROM CandidateTestAssignments WHERE CandidateId = ?', candidate_id)
    cursor.execute(f'DELETE FROM CandidateHistories WHERE CandidateId = ?', candidate_id)
    cursor.execute(f'DELETE FROM Candidates WHERE CandidateId = ?', candidate_id)