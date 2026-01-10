from django.db import connection


class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        for query in connection.queries:
            print(query)
            print("")

        print(f"SQL Queries executed: {len(connection.queries)}")
        return response
