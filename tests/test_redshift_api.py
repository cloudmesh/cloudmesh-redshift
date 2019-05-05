###############################################################
# pytest -v --capture=no tests/test_redshift_openapi.py
# pytest -v  tests/test_redshift_openapi.py
# pytest -v --capture=no -v --nocapture tests/test_redshift_openapi.py:Test_RedShift_openapi.<METHODNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.run.subprocess import run
import cloudmesh.redshift.command.run



import pytest


@pytest.mark.incremental
class Test_RedShift_openapi:

    def setup(self):
        self.clusterid = ""

    def test_list_clusters(self):
        result = run(['curl', 'http://localhost:8080/api/list_clusters'], shell=False)

        assert result is not None
        assert result[0] == "["

    def test_start_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/start?name=pytest-cluster&count=2'], shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = result[16:31]

    def test_list_steps(self):
        result = run(['curl', 'http://localhost:8080/api/list_steps?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_describe(self):
        result = run(['curl', 'http://localhost:8080/api/describe?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_copy(self):
        result = run(['curl','http://localhost:8080/api/copy?cluster=?{}&bucket=test&bucketname='
                             'test.py'.format(self.clusterid)], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_run(self):
        result = run(['curl','http://localhost:8080/api/run?cluster=?{}&bucket=test&bucketname='
                             'test.py'.format(self.clusterid)], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_list_instances(self):
        result = run(['curl', 'http://localhost:8080/api/list_instances?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_stop_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/stop?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""

