test_survey = {
    "title": "Survey for Care Partners",
    "prompt": "What are you doing now?",
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

survey_dict = {}
survey_dict['test_survey'] = test_survey