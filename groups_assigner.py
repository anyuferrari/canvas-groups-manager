import pandas as pd
import yaml

from Controllers.canvas_controller import Canvas
from queries import Queries

with open('credentials.yml', 'r') as file:
    credentials = yaml.safe_load(file)


class GroupsAssigner:
    def __init__(self, courses: list, ):
        self.m = 0
        self.canvas = Canvas()
        self.courses = courses
        self.run()

    def get_sections(self, course: str):
        query = Queries.sections_query
        variables = {'courseId': course}
        sections = self.canvas.graph_ql(query, variables)['data']['course']['sectionsConnection']['nodes']
        return [section for section in sections if section['sisId'] is not None]

    def get_all_students(self, course: str):
        canvas_course_id = self.canvas.get_course_id(course)
        query = Queries.all_users_query
        variables = {'courseId': canvas_course_id}
        request = self.canvas.graph_ql(query, variables)['data']['course']['enrollmentsConnection']['nodes']
        return [{"user": it['user']['_id'], "username": it['user']['loginId'],
                 "section": it['section']['name']} for it in
                request if it['sisRole'] == "student"]

    def run(self):
        m = 0
        for course in self.courses:
            print(f"*     Curso {course}")
            students = pd.DataFrame(self.get_all_students(course))
            sections = self.canvas.get_sections(course)
            k = 0
            for section in sections:
                section_students = students[students.section == section['full_name']]
                if len(section_students) > 50:
                    print("          SECCIÓN CON MÁS DE 50 ALUMNOS, REVISAR")
                    print(f"          {section['name']}")
                k += 1
                print(f"*          Sección {k} de {len(sections)}")
                groups = self.canvas.get_section_groups(course, section)
                data = []
                for section_group in groups:
                    for student in section_group['membersConnection']['nodes']:
                        data.append(student['user']['_id'])
                ungrouped = section_students[~section_students.user.isin(data)]
                groups_request = []
                for group in groups:
                    if len(ungrouped) != 0:
                        members = [member['user']['_id'] for member in group['membersConnection']['nodes']]
                        if len(members) > 5:
                            print("          GRUPO CON MÁS DE 5 ALUMNOS")
                            print(f"          {group['name']}")
                        elif len(members) < 5:
                            to_group = []
                            for j in range(5 - len(members)):
                                to_group.append(ungrouped.iloc[0]['user'])
                                ungrouped = ungrouped.iloc[1:]
                                if len(ungrouped) == 0:
                                    break
                            members += to_group
                            m += len(to_group)
                            if len(to_group) != 0:
                                groups_request.append({"group_id": group['_id'], "members": members})
                    else:
                        continue
                if len(groups_request) != 0:
                    self.canvas.assign_group(groups_request)
            print(f'          Se han asignado {m} alumnos a sus grupos')
