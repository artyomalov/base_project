from config import settings


class SubdivisionService:
    def __init__(
        self,
        repository,
    ):
        self.repository = repository
        self.link_generator = "LinkGenerator(url, model, e.t.c)"
        self.paginator = "Paginator(settings.PER_PAGE_ITEMS_COUNT)"

    def list_subdivisions(self):
        """
        get subdivisions list with pagination
        add link for every subdivision
        """
        pass

    def get_subdivision(self):
        """
        get subdivision data from db
        generate link to projects
        generate links for subdivision actions
        """
        pass

    def create_subdivision(self):
        """
        Creates subdivision and returns created result
        with all nessessary links
        """
        pass

    def update_subdivision(self):
        """
        Updates selected subdivision and
        returns updated result with all
        nesessary links
        """
        pass

    def delete_subdivision(self):
        """
        Deletes selected subdivision
        """


class ProjectService:
    def __init__(self, repository):
        self.repository = repository
        self.link_generator = "LinkGenerator(url, model, e.t.c)"
        self.paginator = "Paginator(settings.PER_PAGE_ITEMS_COUNT)"

    def list_projects(self):
        """
        Get projects list with pagination
        add link for every project
        """
        pass

    def get_project(self):
        """
        Get project data from db
        generate link to projects
        generate links for project actions
        """
        pass

    def create_project(self):
        """
        Creates project and returns created result
        with all nessessary links
        """
        pass

    def update_project(self):
        """
        Updates selected project and
        returns updated result with all
        nesessary links
        """
        pass

    def delete_project(self):
        """
        Deletes project by id
        """
        pass
