from orkg.utils import NamespacedClient, query_params, dict_to_url_params
from orkg.out import OrkgResponse


class ClassesClient(NamespacedClient):

    def by_id(self, id):
        self.client.backend._append_slash = True
        response = self.client.backend.classes(id).GET()
        return OrkgResponse(response)

    @query_params("q", "exact")
    def get_all(self, params=None):
        if len(params) > 0:
            self.client.backend._append_slash = False
            response = self.client.backend.classes.GET(dict_to_url_params(params))
        else:
            self.client.backend._append_slash = True
            response = self.client.backend.classes.GET()
        return OrkgResponse(response)

    @query_params("page", "items", "sortBy", "desc")
    def get_resource_by_class(self, class_id, params=None):
        if len(params) > 0:
            self.client.backend._append_slash = False
            response = self.client.backend.classes(class_id).resources.GET(dict_to_url_params(params))
        else:
            self.client.backend._append_slash = True
            response = self.client.backend.classes(class_id).resources.GET()
        return OrkgResponse(response)

    @query_params("id", "label", "uri")
    def add(self, params=None):
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            self.client.backend._append_slash = True
            response = self.client.backend.classes.POST(json=params, headers=self.auth)
        return OrkgResponse(response)

    @query_params("id", "label", "uri")
    def find_or_add(self, params=None):
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            if "id" in params:
                # check if a class with this id is there
                found = self.by_id(params['id'])
                if found.succeeded:
                    return found
            # check if a class with this label is there
            found = self.get_all(q=params['label'], exact=True)
            if found.succeeded:
                if isinstance(found.content, list) and len(found.content) > 0:
                    found.content = found.content[0]
                return found
            # None found, what the hell! let's create a new one
            self.client.backend._append_slash = True
            response = self.client.backend.classes.POST(json=params, headers=self.auth)
        return OrkgResponse(response)

    @query_params("label", "uri")
    def update(self, id, params=None):
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            if not self.exists(id):
                raise ValueError("the provided id is not in the graph")
            self.client.backend._append_slash = True
            response = self.client.backend.classes(id).PUT(json=params, headers=self.auth)
        return OrkgResponse(response)

    def exists(self, id):
        return self.by_id(id).succeeded

