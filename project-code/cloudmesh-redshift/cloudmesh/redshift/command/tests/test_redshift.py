from cloudmesh.redshift.command.redshift import RedshiftCommand

import pytest


@pytest.mark.incremental
class TestRedshiftCommand(RedshiftCommand):
    def test_do_redshift(self):
        pass


def test_normal():
    pass
