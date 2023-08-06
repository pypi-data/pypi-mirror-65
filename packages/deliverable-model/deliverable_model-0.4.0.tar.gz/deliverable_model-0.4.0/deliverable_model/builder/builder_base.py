from pathlib import Path


class BuilderBase:
    def serialize(self, assert_dir: Path) -> dict:
        """
        Save assert to assert_dir and return dict as metadata

        """
        raise NotImplementedError

    def get_dependency(self) -> list:
        """
        Return python package dependency for builder
        """
        raise NotImplementedError
