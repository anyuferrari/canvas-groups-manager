from Controllers.canvas_controller import Canvas
from queries import Queries


class CategoriesCreator:
    def __init__(self, courses: list):
        self.i = 0
        self.canvas = Canvas()
        self.courses = courses
        for course in courses:
            print(f"*     Controlando categorías para {course}")
            self.check_categories(course)

    def check_categories(self, course: str):
        query = Queries.categories_query
        variables = {"courseId": course}
        categories = self.canvas.graph_ql(query=query, variables=variables)
        names = [category['name'] for category in categories['data']['course']['groupSetsConnection']['nodes']]
        if f'Grupos: {course}' in names:
            return True
        else:
            posted = self.canvas.post_category(course)
            self.canvas.post_annulled_students(posted)
            self.i += 1
            return posted
