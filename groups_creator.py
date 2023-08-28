import asyncio

import aiohttp
import yaml
from aiolimiter import AsyncLimiter

from Controllers.canvas_controller import Canvas
from queries import Queries

with open('credentials.yml', 'r') as file:
    credentials = yaml.safe_load(file)


class GroupsCreator:
    def __init__(self, courses: list):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.limiter = AsyncLimiter(max_rate=60, time_period=60)
        self.i = 0
        self.canvas = Canvas()
        self.courses = courses
        self.fieldnames = ['_id', 'name', 'sisId']
        self.run()

    def get_section_groups(self, course: str, section_id: str):
        query = Queries.groups_query
        variables = {"courseId": course}
        groups = self.canvas.graph_ql(query, variables)
        return [
            {'id': group['_id'], 'membersCount': group['membersCount'], 'name': group['name'], 'sisId': group['sisId']}
            for group in groups['data']['course']['groupsConnection']['nodes'] if section_id in group['name']]

    def get_category_id(self, course: str):
        query = Queries.categories_query
        variables = {"courseId": course}
        categories = self.canvas.graph_ql(query, variables)['data']['course']['groupSetsConnection']['nodes']
        for category in categories:
            if 'Grupos:' in category['name']:
                return category['_id']

    def create_groups(self, course: str, sections: list):

        async def post_groups(session: aiohttp.ClientSession, section_name: str, section_id: str):
            prefix = f'{section_name} C/{section_id}-'
            groups = [prefix + str(i) for i in range(1, 11)]
            category = self.get_category_id(course)
            query = Queries.groups_mutation
            post_group = []
            variables = {"groupName1": groups[0],
                         "groupName2": groups[1],
                         "groupName3": groups[2],
                         "groupName4": groups[3],
                         "groupName5": groups[4],
                         "groupName6": groups[5],
                         "groupName7": groups[6],
                         "groupName8": groups[7],
                         "groupName9": groups[8],
                         "groupName10": groups[9],
                         "cateogryId": category}
            url = credentials['Canvas'][0]['GRAPHQL_URL']
            async with session.post(url, json={'query': query, 'variables': variables}) as response:
                response = await response.json()

        async def gatherer(section_list: list):
            async with aiohttp.ClientSession(headers=self.canvas.headers) as clientSession:
                tasks = [post_groups(clientSession, section['name'], section['sisId']) for section in section_list]
                return await asyncio.gather(*tasks)

        return asyncio.run(gatherer(sections))

    def run(self):
        for course in self.courses:
            print(f"*    Procesando el curso {course}")
            sections = self.canvas.get_sections(course)
            empty_sections = []
            for section in sections:
                groups = self.get_section_groups(course, section['sisId'])
                self.i += 1
                if len(groups) == 0:
                    print(f"          Sección sin grupos")
                    self.i += 10
                    empty_sections.append(section)
                elif 0 < len(groups) < 10:
                    print("          #############FALTAN GRUPOS################")
                elif len(groups) > 10:
                    print("          #############SOBRAN GRUPOS###############")
            self.create_groups(course, empty_sections)
        return self.i
