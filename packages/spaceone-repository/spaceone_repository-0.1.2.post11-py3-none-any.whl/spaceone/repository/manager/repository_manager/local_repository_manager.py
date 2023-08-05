from spaceone.repository.manager.repository_manager import RepositoryManager
from spaceone.repository.model.repository_model import Repository


class LocalRepositoryManager(RepositoryManager):

    def register_repository(self, params):
        """
        Args:
            params:
                - name
                - repository_type: local
        """
        # Assume there is only one local repository

        return self.repo_model.create(params)
