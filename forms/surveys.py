test_survey = {
    "title": "Survey for Care Partners",
    "prompt": "What have you been up to?",
    "question": {
        "A": {
            "text": "travel",
            "options":
                {
                    "1": "travel_category_1",
                    "2": "travel_category_2",
                    "3": "travel_category_3"
                }
        },
        "B": {
            "text": "admin",
            "options":
                {
                    "4": "admin_category_1",
                    "5": "admin_category_2",
                    "6": "admin_category_3"
                }
        },
        "C": {
            "text": "clinical",
            "options":
                {
                    "7": "clinical_category_1",
                    "8": "clinical_category_2",
                    "9": "clinical_category_3",
                    "10": "clinical_category_4"
                }
        }
    }
}

test_survey_office = {
    "title": "Survey for ClinOps Office",
    "prompt": "What have you been up to?",
    "question": {
        "A": {
            "text": "desk work",
            "options":
                {
                    "1": "mostly emailing",
                    "2": "mostly working with documents",
                    "3": "can't remember"
                }
        },
        "B": {
            "text": "meetings",
            "options":
                {
                    "4": "meetings 1 on 1 ",
                    "5": "meetings in group",
                }
        },
        "C": {
            "text": "other",
            "options":
                {
                    "7": "lunch",
                    "8": "running errands",
                    "9": "something else",
                }
        }
    }
}

survey_questions = {
    "sent": {
        1: "Have you been doing ADMINISTRATIVE work in the last hour or so? (y/n)",
        2: "Have you been TRAVELING in the last hour or so? (y/n)"
    }
}

survey_admin ={
    "sent":{
        1: "Have you been doing ADMINISTRATIVE work in the last hour or so? (Y/N)"
    }
}

survey_admin_night = {
    "sent":{
        1:"Did you LOG CLINICAL INFORMATION after hours yesterday? (Y/N)"
    }
}

survey_dict = {}
survey_dict['test_survey'] = test_survey
survey_dict['test_survey_office'] = test_survey_office
survey_dict['survey_questions'] = survey_questions
survey_dict['survey_admin'] = survey_admin
survey_dict['survey_admin_night'] = survey_admin_night