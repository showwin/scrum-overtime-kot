import datetime

from beautifultable import BeautifulTable

from configuration import SokotConfiguration
from requester import SokotRequester

DUMMY_RESP = [{
    "date": "2016-05-01",
    "dailyWorkings": [{
        "date": "2016-05-01",
        "employeeKey": "8b6ee646a9620b286499c3df6918c4888a97dd7bbc6a26a18743f4697a1de4b3",
        "currentDateEmployee": {
            "divisionCode": "1000",
            "divisionName": "本社",
            "gender": "male",
            "typeCode": "1",
            "typeName": "正社員",
            "code": "0003",
            "lastName": "勤怠",
            "firstName": "太郎",
            "lastNamePhonetics": "キンタイ",
            "firstNamePhonetics": "タロウ"
        },
        "isClosing": True,
        "overtime": 135,
    }]
}]


class SokotAggretator():
    def __init__(self):
        self._config = SokotConfiguration()
        self._sprints = self._culc_sprint()
        self._requester = SokotRequester()

    def _culc_sprint(self):
        sprints = []
        start_day = self._config.get_scrum_start_day()
        sprint_start = start_day
        while True:
            if sprint_start > datetime.date.today():
                break
            sprint_end = sprint_start + datetime.timedelta(days=14)
            sprint = (sprint_start, sprint_end)
            sprints.append(sprint)
            sprint_start = sprint_end
        return sprints

    def _aggregate_sprint(self, members, sprint_start, sprint_end):
        print('/daily-workings?start={}&end={}'.format(sprint_start, sprint_end))

        # resp = self._requester.get('/daily-workings?start={}&end={}'.format(sprint_start, sprint_end))
        resp = DUMMY_RESP
        sum_min = 0
        for daily_record in resp:
            for record in daily_record['dailyWorkings']:
                if record['currentDateEmployee']['code'] in members:
                    if record['isClosing']:
                        sum_min += record['overtime']
        return round(sum_min / 60, 2)

    def aggregate(self, agg_type):
        table = BeautifulTable()
        group_names = list(self._config.list_group().keys())
        table.column_headers = ["Sprint No."] + group_names

        sprint_no = 0
        for sprint in self._sprints:
            sprint_no += 1
            sprint_start, sprint_end = sprint[0], sprint[1]
            sprint_str = "Sprint #{} ({} - {})".format(sprint_no, sprint_start, sprint_end)
            group_result = []
            for _, members in self._config.list_group().items():
                result = self._aggregate_sprint(members, sprint_start, sprint_end)
                group_result.append(result)
            table.append_row([sprint_str] + group_result)
        return table
