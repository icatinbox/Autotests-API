from datetime import datetime
from tests.utils.utils import date_to_iso

DEFAULT_STATUS_ID = 28913
STATUS_FREE_CANDIDATE = 28928
STATUS_BLACK_LIST = 28836
PAYLOAD_BLACK_LIST = {
    "candidateId": None,
    "description": "",
    "accountId": 22014,
    "statusId": STATUS_BLACK_LIST,
    "isAllDay": 0,
    "responsibleId": 22014,
    "fields": "",
    "notificationSettings": [],
    "invited": ""
}

PAYLOAD_TEST_MANAGE = {
    "id": 1733,
    "name": "Технический администратор",
    "description": "",
    "permissions": [
        {
            "permissionId": 1,
            "description": ""
        },
        {
            "permissionId": 2,
            "description": ""
        },
        {
            "permissionId": 3,
            "description": ""
        },
        {
            "permissionId": 4,
            "description": ""
        },
        {
            "permissionId": 5,
            "description": ""
        },
        {
            "permissionId": 6,
            "description": ""
        },
        {
            "permissionId": 7,
            "description": ""
        },
        {
            "permissionId": 8,
            "description": ""
        },
        {
            "permissionId": 9,
            "description": ""
        },
        {
            "permissionId": 10,
            "description": ""
        },
        {
            "permissionId": 11,
            "description": ""
        },
        {
            "permissionId": 12,
            "description": ""
        },
        {
            "permissionId": 13,
            "description": ""
        },
        {
            "permissionId": 14,
            "description": ""
        },
        {
            "permissionId": 15,
            "description": ""
        },
        {
            "permissionId": 16,
            "description": ""
        },
        {
            "permissionId": 17,
            "description": ""
        },
        {
            "permissionId": 18,
            "description": ""
        },
        {
            "permissionId": 19,
            "description": ""
        },
        {
            "permissionId": 20,
            "description": ""
        },
        {
            "permissionId": 21,
            "description": ""
        },
        {
            "permissionId": 22,
            "description": ""
        },
        {
            "permissionId": 23,
            "description": ""
        },
        {
            "permissionId": 74,
            "description": ""
        },
        {
            "permissionId": 24,
            "description": ""
        },
        {
            "permissionId": 25,
            "description": ""
        },
        {
            "permissionId": 26,
            "description": ""
        },
        {
            "permissionId": 27,
            "description": ""
        },
        {
            "permissionId": 28,
            "description": ""
        },
        {
            "permissionId": 29,
            "description": ""
        },
        {
            "permissionId": 30,
            "description": ""
        },
        {
            "permissionId": 31,
            "description": ""
        },
        {
            "permissionId": 33,
            "description": ""
        },
        {
            "permissionId": 34,
            "description": ""
        },
        {
            "permissionId": 35,
            "description": ""
        },
        {
            "permissionId": 36,
            "description": ""
        },
        {
            "permissionId": 37,
            "description": ""
        },
        {
            "permissionId": 38,
            "description": ""
        },
        {
            "permissionId": 39,
            "description": ""
        },
        {
            "permissionId": 40,
            "description": ""
        },
        {
            "permissionId": 41,
            "description": ""
        },
        {
            "permissionId": 42,
            "description": ""
        },
        {
            "permissionId": 43,
            "description": ""
        },
        {
            "permissionId": 44,
            "description": ""
        },
        {
            "permissionId": 45,
            "description": ""
        },
        {
            "permissionId": 46,
            "description": ""
        },
        {
            "permissionId": 47,
            "description": ""
        },
        {
            "permissionId": 48,
            "description": ""
        },
        {
            "permissionId": 49,
            "description": ""
        },
        {
            "permissionId": 50,
            "description": ""
        },
        {
            "permissionId": 51,
            "description": ""
        },
        {
            "permissionId": 52,
            "description": ""
        },
        {
            "permissionId": 53,
            "description": ""
        },
        {
            "permissionId": 54,
            "description": ""
        },
        {
            "permissionId": 55,
            "description": ""
        },
        {
            "permissionId": 56,
            "description": ""
        },
        {
            "permissionId": 57,
            "description": ""
        },
        {
            "permissionId": 58,
            "description": ""
        },
        {
            "permissionId": 59,
            "description": ""
        },
        {
            "permissionId": 60,
            "description": ""
        },
        {
            "permissionId": 61,
            "description": ""
        },
        {
            "permissionId": 62,
            "description": ""
        },
        {
            "permissionId": 63,
            "description": ""
        },
        {
            "permissionId": 64,
            "description": ""
        },
        {
            "permissionId": 65,
            "description": ""
        },
        {
            "permissionId": 66,
            "description": ""
        },
        {
            "permissionId": 67,
            "description": ""
        },
        {
            "permissionId": 69,
            "description": ""
        }
    ]
    }
PAYLOAD_TEST_GRADE = {
    "id": 1733,
    "name": "Технический администратор",
    "description": "",
    "permissions": [
        {
            "permissionId": 1,
            "description": ""
        },
        {
            "permissionId": 2,
            "description": ""
        },
        {
            "permissionId": 3,
            "description": ""
        },
        {
            "permissionId": 4,
            "description": ""
        },
        {
            "permissionId": 5,
            "description": ""
        },
        {
            "permissionId": 6,
            "description": ""
        },
        {
            "permissionId": 7,
            "description": ""
        },
        {
            "permissionId": 8,
            "description": ""
        },
        {
            "permissionId": 9,
            "description": ""
        },
        {
            "permissionId": 10,
            "description": ""
        },
        {
            "permissionId": 11,
            "description": ""
        },
        {
            "permissionId": 12,
            "description": ""
        },
        {
            "permissionId": 13,
            "description": ""
        },
        {
            "permissionId": 14,
            "description": ""
        },
        {
            "permissionId": 15,
            "description": ""
        },
        {
            "permissionId": 16,
            "description": ""
        },
        {
            "permissionId": 17,
            "description": ""
        },
        {
            "permissionId": 18,
            "description": ""
        },
        {
            "permissionId": 19,
            "description": ""
        },
        {
            "permissionId": 20,
            "description": ""
        },
        {
            "permissionId": 21,
            "description": ""
        },
        {
            "permissionId": 22,
            "description": ""
        },
        {
            "permissionId": 23,
            "description": ""
        },
        {
            "permissionId": 73,
            "description": ""
        },
        {
            "permissionId": 24,
            "description": ""
        },
        {
            "permissionId": 25,
            "description": ""
        },
        {
            "permissionId": 26,
            "description": ""
        },
        {
            "permissionId": 27,
            "description": ""
        },
        {
            "permissionId": 28,
            "description": ""
        },
        {
            "permissionId": 29,
            "description": ""
        },
        {
            "permissionId": 30,
            "description": ""
        },
        {
            "permissionId": 31,
            "description": ""
        },
        {
            "permissionId": 33,
            "description": ""
        },
        {
            "permissionId": 34,
            "description": ""
        },
        {
            "permissionId": 35,
            "description": ""
        },
        {
            "permissionId": 36,
            "description": ""
        },
        {
            "permissionId": 37,
            "description": ""
        },
        {
            "permissionId": 38,
            "description": ""
        },
        {
            "permissionId": 39,
            "description": ""
        },
        {
            "permissionId": 40,
            "description": ""
        },
        {
            "permissionId": 41,
            "description": ""
        },
        {
            "permissionId": 42,
            "description": ""
        },
        {
            "permissionId": 43,
            "description": ""
        },
        {
            "permissionId": 44,
            "description": ""
        },
        {
            "permissionId": 45,
            "description": ""
        },
        {
            "permissionId": 46,
            "description": ""
        },
        {
            "permissionId": 47,
            "description": ""
        },
        {
            "permissionId": 48,
            "description": ""
        },
        {
            "permissionId": 49,
            "description": ""
        },
        {
            "permissionId": 50,
            "description": ""
        },
        {
            "permissionId": 51,
            "description": ""
        },
        {
            "permissionId": 52,
            "description": ""
        },
        {
            "permissionId": 53,
            "description": ""
        },
        {
            "permissionId": 54,
            "description": ""
        },
        {
            "permissionId": 55,
            "description": ""
        },
        {
            "permissionId": 56,
            "description": ""
        },
        {
            "permissionId": 57,
            "description": ""
        },
        {
            "permissionId": 58,
            "description": ""
        },
        {
            "permissionId": 59,
            "description": ""
        },
        {
            "permissionId": 60,
            "description": ""
        },
        {
            "permissionId": 61,
            "description": ""
        },
        {
            "permissionId": 62,
            "description": ""
        },
        {
            "permissionId": 63,
            "description": ""
        },
        {
            "permissionId": 64,
            "description": ""
        },
        {
            "permissionId": 65,
            "description": ""
        },
        {
            "permissionId": 66,
            "description": ""
        },
        {
            "permissionId": 67,
            "description": ""
        },
        {
            "permissionId": 69,
            "description": ""
        }
    ]
    }
PAYLOAD_FULL_PERMISSIONS = {
    "id": 1733,
    "name": "Технический администратор",
    "description": "",
    "permissions": [
        {
            "permissionId": 1,
            "description": ""
        },
        {
            "permissionId": 2,
            "description": ""
        },
        {
            "permissionId": 3,
            "description": ""
        },
        {
            "permissionId": 4,
            "description": ""
        },
        {
            "permissionId": 5,
            "description": ""
        },
        {
            "permissionId": 6,
            "description": ""
        },
        {
            "permissionId": 7,
            "description": ""
        },
        {
            "permissionId": 8,
            "description": ""
        },
        {
            "permissionId": 9,
            "description": ""
        },
        {
            "permissionId": 10,
            "description": ""
        },
        {
            "permissionId": 11,
            "description": ""
        },
        {
            "permissionId": 12,
            "description": ""
        },
        {
            "permissionId": 13,
            "description": ""
        },
        {
            "permissionId": 14,
            "description": ""
        },
        {
            "permissionId": 15,
            "description": ""
        },
        {
            "permissionId": 16,
            "description": ""
        },
        {
            "permissionId": 17,
            "description": ""
        },
        {
            "permissionId": 18,
            "description": ""
        },
        {
            "permissionId": 19,
            "description": ""
        },
        {
            "permissionId": 20,
            "description": ""
        },
        {
            "permissionId": 21,
            "description": ""
        },
        {
            "permissionId": 22,
            "description": ""
        },
        {
            "permissionId": 23,
            "description": ""
        },
        {
            "permissionId": 73,
            "description": ""
        },
        {
            "permissionId": 74,
            "description": ""
        },
        {
            "permissionId": 24,
            "description": ""
        },
        {
            "permissionId": 25,
            "description": ""
        },
        {
            "permissionId": 26,
            "description": ""
        },
        {
            "permissionId": 27,
            "description": ""
        },
        {
            "permissionId": 28,
            "description": ""
        },
        {
            "permissionId": 29,
            "description": ""
        },
        {
            "permissionId": 30,
            "description": ""
        },
        {
            "permissionId": 31,
            "description": ""
        },
        {
            "permissionId": 33,
            "description": ""
        },
        {
            "permissionId": 34,
            "description": ""
        },
        {
            "permissionId": 35,
            "description": ""
        },
        {
            "permissionId": 36,
            "description": ""
        },
        {
            "permissionId": 37,
            "description": ""
        },
        {
            "permissionId": 38,
            "description": ""
        },
        {
            "permissionId": 39,
            "description": ""
        },
        {
            "permissionId": 40,
            "description": ""
        },
        {
            "permissionId": 41,
            "description": ""
        },
        {
            "permissionId": 42,
            "description": ""
        },
        {
            "permissionId": 43,
            "description": ""
        },
        {
            "permissionId": 44,
            "description": ""
        },
        {
            "permissionId": 45,
            "description": ""
        },
        {
            "permissionId": 46,
            "description": ""
        },
        {
            "permissionId": 47,
            "description": ""
        },
        {
            "permissionId": 48,
            "description": ""
        },
        {
            "permissionId": 49,
            "description": ""
        },
        {
            "permissionId": 50,
            "description": ""
        },
        {
            "permissionId": 51,
            "description": ""
        },
        {
            "permissionId": 52,
            "description": ""
        },
        {
            "permissionId": 53,
            "description": ""
        },
        {
            "permissionId": 54,
            "description": ""
        },
        {
            "permissionId": 55,
            "description": ""
        },
        {
            "permissionId": 56,
            "description": ""
        },
        {
            "permissionId": 57,
            "description": ""
        },
        {
            "permissionId": 58,
            "description": ""
        },
        {
            "permissionId": 59,
            "description": ""
        },
        {
            "permissionId": 60,
            "description": ""
        },
        {
            "permissionId": 61,
            "description": ""
        },
        {
            "permissionId": 62,
            "description": ""
        },
        {
            "permissionId": 63,
            "description": ""
        },
        {
            "permissionId": 64,
            "description": ""
        },
        {
            "permissionId": 65,
            "description": ""
        },
        {
            "permissionId": 66,
            "description": ""
        },
        {
            "permissionId": 67,
            "description": ""
        },
        {
            "permissionId": 69,
            "description": ""
        }
    ]
    }

BASE_PAYLOAD_CANDIDATE = {
    "photoId": 0,
    "communicationChannels": {
        "email": None,
        "phone": None,
        "fb": None,
        "gh": None,
        "gp": None,
        "li": None,
        "mk": None,
        "ok": None,
        "sk": None,
        "tg": None,
        "tw": None,
        "vk": None,
        "dc": None,
        "none": [
            ""
        ]
    },
    "driverLicense": "",
    "birthDate": None,
    "place": 0,
    "city": {},
    "phones": [],
    "salary": "",
    "schedule": 0,
    "currency": 0,
    "experience": [],
    "employment": 0,
    "relocations": [],
    "sourceUpdate": None,
    "addWay": "Отклик",
    "sourceName": "Центр занятости",
    "candidateId": None,
    "firstName": f"Тестовый {datetime.now().month}",
    "middleName": f"Кандидат {datetime.now().day}",
    "emails": [],
    "aboutMe": None,
    "position": None,
    "sex": 0,
    "sanbook": 0,
    "languages": [],
    "recommendations": [],
    "files": [],
    "education": [],
    "isReadyToRelocate": False,
    "maritalStatus": 0,
    "businessTrip": 0,
    "childs": 0,
    "filesHash": "7v3oR_QXcp1CMze-k9jYG",
    "skills": [],
    "citizenship": "",
    "courses": [],
    "cVText": "",
    "lastName": "Кандидатович"
}
BASE_PAYLOAD_VACANCY = {
    "accountId": 22014,
    "name": f"Тестовая {datetime.now().strftime('YY MM DD')} Новая вакансия",
    "regionId": None,
    "suspensePeriods": [],
    "customerId": 0,
    "responsibleId": 22014,
    "hiringManagerId": 0,
    "functionalManagerId": 0,
    "status": 1,
    "employeeIds": [],
    "positionCount": 1,
    "isConfidential": False,
    "jobTypeId": None,
    "filesHash": None,
    "recruitmentCenterId": None,
    "customFieldsValues": [
        {
            "systemName": "job_creation_reason",
            "fieldStamp": "Ka-dTJLQvuBl_ZmrpcHGI_EWoTwuP2lf",
            "value": 0
        },
        {
            "systemName": "job_registration_access_state_secrets",
            "fieldStamp": "gv17hEgKVuNr2PqcGCbMJ-XZ4-IR0-BQ",
            "value": 0
        },
        {
            "systemName": "job_expirience",
            "fieldStamp": "h4TX3FWjRnyuDjQUY38wtrokXndIATSZ",
            "value": 0
        },
        {
            "systemName": "job_education_level",
            "fieldStamp": "VXkWyU36dyqbTPe7rhIuOPsGeZSMFsbY",
            "value": 0
        },
        {
            "systemName": "job_additional_education",
            "fieldStamp": "aFtFGMw40kDhQqDPzL0PfVFp8pF_rPYs",
            "value": ""
        },
        {
            "systemName": "job_position_candidate_with_disability",
            "fieldStamp": "YrwOuY08MwzlgDCjGgAseQ2jUFN1d7DS",
            "value": 0
        },
        {
            "systemName": "job_internal_appointments_program",
            "fieldStamp": "_wwKi3LsI037EFVnmMPjwiGfaCwO_GMz",
            "value": 0
        },
        {
            "systemName": "job_key_tasks_test_period",
            "fieldStamp": "ar88A3dW9o0t6W2MBB0QDlAPIYECAoo7",
            "value": ""
        },
        {
            "systemName": "job_personal_qualities",
            "fieldStamp": "FeZffAppc9NQSi8E8Ka3TQkcSwZbBGQf",
            "value": ""
        },
        {
            "systemName": "job_more_preferred_companies",
            "fieldStamp": "yPT4mE2JeIBpAc0m2M8L2jZ4N17hZYck",
            "value": ""
        },
        {
            "systemName": "job_number_historical",
            "fieldStamp": "k8g9a1TzsAfO7lUyKZab9ZufujF1izzy",
            "value": ""
        },
        {
            "systemName": "job_employment_category",
            "fieldStamp": "g5ezXBLpjsyB70lrWgOo-36XMoDdXw_a",
            "value": 0
        },
        {
            "systemName": "job_priority",
            "fieldStamp": "4NQ8edEPlUn1HXHJAYmjNyXojxo8J0YH",
            "value": 0
        },
        {
            "systemName": "job_salary_min",
            "fieldStamp": "Wtc9nYEcvijm3GXZVyQEgAFKhxlLdHb4",
            "value": 0
        },
        {
            "systemName": "job_salary_max",
            "fieldStamp": "Al8LPpfc1CcPu_7RXIIJQIDFa38b4Pmp",
            "value": 0
        },
        {
            "systemName": "job_employment_type",
            "fieldStamp": "v64y65_c0x5hbwDDbP3Li3rQRCRuX8zG",
            "value": 0
        },
        {
            "systemName": "job_employment_schedule",
            "fieldStamp": "k1QnzK4M8OwOJatsCTB6OuPaNc5qmzwW",
            "value": 0
        },
        {
            "systemName": "job_grade",
            "fieldStamp": "lBHpWzI54Wca34A0bfnWH-xh7qpzk7q1",
            "value": 0
        },
        {
            "systemName": "job_contract_type",
            "fieldStamp": "IhinNPB5MMwuH-aHqT7pOfkdjQZ2u0aV",
            "value": 0
        }
    ],
    "organizationUnit": None,
    "regionalCoefficient": None,
    "northernAllowance": None,
    "bonusPHD": False,
    "bonusPHDValue": None,
    "bonusInvest": False,
    "bonusInvestValue": None,
    "annualReward": False,
    "annualRewardValue": None,
    "workFormatTypeId": None,
    "workScheduleTypeId": None,
    "probationPeriodTypeId": None,
    "clearanceLevelCompensationTypeId": None,
    "extraLeaveTypeId": None,
    "allowances": None,
    "compensationsAndBenefits": None,
    "travelWorkType": 0
}
BASE_PAYLOAD_CANDIDATE_HISTORIES = {
    "candidateId": None,
    "description": "",
    "jobId": None,
    "accountId": 22014,
    "statusId": None,
    "isAllDay": 0,
    "responsibleId": 22014,
    "fields": "",
    "sodPackagePriority": 5,
    "sodVsp": 0,
    "sodBoxNumber": "",
    "sodCorrectionListNumber": "",
    "offerPlannedDate": "",
    "sodFiles": [],
    "notificationSettings": [],
    "invited": ""
}
BASE_PAYLOAD_TEST = {
  "jobId": None,
  "candidateId": None,
  "testId": None,
  "AssignedAt": date_to_iso(datetime.now()),
  "testHistoryId": None,
  "comment": "Я в своем познании настолько преисполнился, что уверен в прохождении теста",
  "files": [{
    "fileName": "Тестовый файл.txt",
    "Content": "0K8g0LIg0YHQstC+0LXQvCDQv9C+0LfQvdCw0L3QuNC4INC90LDRgdGC0L7Qu9GM0LrQviDQv9GA0LXQ"
  }]
}

PAYLOAD_ROLE_ADMIN = {
    "accountId": 22014,
    "department": "",
    "isBlocked": 0,
    "firstName": "сотрудник",
    "lastName": "QPD",
    "middleName": "",
    "phone": None,
    "roleId": 0,
    "userName": "test@friendwork.ru",
    "customerId": 0,
    "isSodEnabled": False,
    "delegatedOrganizationUnitIds": []
}
PAYLOAD_BASE_ROLE = {
    "accountId": 22014,
    "department": "",
    "isBlocked": 0,
    "firstName": "сотрудник",
    "lastName": "QPD",
    "middleName": "",
    "phone": None,
    "roleId": 1733,
    "userName": "test@friendwork.ru",
    "customerId": 0,
    "isSodEnabled": False,
    "delegatedOrganizationUnitIds": []
}