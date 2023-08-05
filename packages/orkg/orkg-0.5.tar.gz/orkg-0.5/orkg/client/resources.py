from orkg.utils import NamespacedClient, query_params, dict_to_url_params
from orkg.out import OrkgResponse


class ResourcesClient(NamespacedClient):

    def by_id(self, id):
        """
        Lookup a resource by id
        :param id: the id of the resource to lookup
        :return: an OrkgResponse object containing the resource
        """
        self.client.backend._append_slash = True
        response = self.client.backend.resources(id).GET()
        return OrkgResponse(response)

    @query_params("q", "exact", "page", "items", "sortBy", "exclude", "desc")
    def get(self, params=None):
        """
        Fetch a list of resources, with the possibility to paginate the results and filter them out based on label
        :param q: search term of the label of the resource (optional)
        :param exact: whether to check for the exact search term or not (optional) -> bool
        :param page: the page number (optional)
        :param items: number of items per page (optional)
        :param sortBy: key to sort on (optional)
        :param desc: true/false to sort desc (optional)
        :param exclude: classes to be excluded in search (optional)
        :return: an OrkgResponse object contains the list of resources
        """
        if len(params) > 0:
            self.client.backend._append_slash = False
            response = self.client.backend.resources.GET(dict_to_url_params(params))
        else:
            self.client.backend._append_slash = True
            response = self.client.backend.resources.GET()
        return OrkgResponse(response)

    @query_params("id", "label", "classes")
    def add(self, params=None):
        """
        Create a new resource in the ORKG instance
        :param id: the specific id to add (optional)
        :param label: the label of the new resource (optional)
        :param classes: list of classes to assign the resource to (optional)
        :return: an OrkgResponse object containing the newly created resource
        """
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            self.client.backend._append_slash = True
            response = self.client.backend.resources.POST(json=params, headers=self.auth)
        return OrkgResponse(response)

    @query_params("id", "label", "classes")
    def find_or_add(self, params=None):
        """
        find or create a new resource in the ORKG instance
        :param id: the specific id to add (optional)
        :param label: the label of the new resource (optional)
        :param classes: list of classes to assign the resource to (optional)
        :return: an OrkgResponse object containing the found or newly created resource
        """
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            if "id" in params:
                # check if a resource with this id is there
                found = self.by_id(params['id'])
                if found.succeeded:
                    return found
            # check if a resource with this label is there
            found = self.get(q=params['label'], exact=True, items=1)
            if found.succeeded:
                if isinstance(found.content, list) and len(found.content) > 0:
                    found.content = found.content[0]
                return found
            # None found, what the hell! let's create a new one
            self.client.backend._append_slash = True
            response = self.client.backend.resources.POST(json=params, headers=self.auth)
        return OrkgResponse(response)

    @query_params("label", "classes")
    def update(self, id, params=None):
        """
        Update a resource with a specific id
        :param id: the id of the resource to update
        :param label: the new label (optional)
        :param classes: the updated list of classes (optional)
        :return: an OrkgResponse object contains the newly updated resource
        """
        if len(params) == 0:
            raise ValueError("at least label should be provided")
        else:
            if not self.exists(id):
                raise ValueError("the provided id is not in the graph")
            self.client.backend._append_slash = True
            response = self.client.backend.resources(id).PUT(json=params, headers=self.auth)
        return OrkgResponse(response)

    def exists(self, id):
        """
        Check if a resource exists in the graph
        :param id: the id of the resource to check
        :return: true if found, otherwise false
        """
        return self.by_id(id).succeeded

