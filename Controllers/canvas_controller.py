import asyncio

import aiohttp
import requests
import yaml
from aiolimiter import AsyncLimiter

from queries import Queries

with open('credentials.yml', 'r') as file:
    credentials = yaml.safe_load(file)


class Canvas:

    def __init__(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.base_url = credentials['Canvas'][0]['URL']
        self.token = credentials['Canvas'][0]['API_KEY']
        self.headers = {'authorization': 'Bearer {}'.format(self.token), 'content-type': 'application/json'}
        self.limiter = AsyncLimiter(max_rate=60, time_period=60)

    def post_category(self, course: str):
        url = f'{self.base_url}courses/sis_course_id:{course}/group_categories?name=Grupos:' \
              f' {course}&sis_group_category_id={course}'
        request = requests.post(url, headers=self.headers)
        response = request.json()
        try:
            answer = response['id']
        except KeyError:
            answer = None
        return answer

    def delete_category(self, categoty: str):
        url = f'{self.base_url}group_categories/{categoty}'
        request = requests.delete(url, headers=self.headers)
        return request.ok

    def post_annulled_students(self, category):
        url = f'{self.base_url}group_categories/{category}/groups?name=ALUMNOS ANULADOS'
        request = requests.post(url, headers=self.headers)
        return request.ok

    def get_section_groups(self, course: str, section: dict):
        query = Queries.groups_query
        variables = {'courseId': course}
        groups = self.graph_ql(query, variables)['data']['course']['groupsConnection']['nodes']
        return [group for group in groups if section['sisId'] in group['name']]

    def get_course_id(self, sis_id: str):
        url = f'{self.base_url}/courses/sis_course_id:{sis_id}'
        request = requests.get(url, headers=self.headers)
        response = request.json()
        return response['id']

    def get_sections(self, course: str):
        query = Queries.sections_query
        variables = {"courseId": course}
        sections = self.graph_ql(query, variables)
        return [{'name': section['name'][section['name'].find('CATEDRA'):section['name'].find('- CO -')],
                 'sisId': section['sisId'], 'full_name': section['name']} for section in
                sections['data']['course']['sectionsConnection']['nodes'] if section['sisId'] is not None]

    def assign_group(self, groups_request: list):
        async def put_group(session: aiohttp.ClientSession, group_id: str, students: list):
            url = f'{self.base_url}groups/{group_id}?members[]={students[0]}'
            for student in students[1:]:
                url += f'&members[]={student}'
            async with session.put(url) as response:
                response = await response.json()

        async def fetch_groups(groups: list):
            async with aiohttp.ClientSession(headers=self.headers) as session, self.limiter:
                tasks = [put_group(session, group['group_id'], group['members']) for group in groups]
                return await asyncio.gather(*tasks)

        return asyncio.run(fetch_groups(groups_request))

    def graph_ql(self, query: object, variables: object) -> object:
        url = 'https://siglo21.beta.instructure.com/api/graphql'
        request = requests.post(url, json={'query': query, 'variables': variables}, headers=self.headers)
        return request.json()
