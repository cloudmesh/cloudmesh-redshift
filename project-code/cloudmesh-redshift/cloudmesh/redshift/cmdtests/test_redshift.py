from cloudmesh.redshift.command.redshift import RedshiftCommand

import pytest

from cloudmesh.common.util import banner

from docopt import docopt


import sys
from contextlib import contextmanager
from io import StringIO


doc = RedshiftCommand.__doc__


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@pytest.mark.incremental
class TestRedshiftCommand(RedshiftCommand):
    def test_describe_all_clusters_with_no_existing(self):
        sys.stdout.write("Describe all clusters - no existing")
        r = RedshiftCommand()
        # args = docopt(doc, ["describe", "cl1"])
        with captured_output() as (out, err):
            sys.stdout.write(r.do_redshift('describe'))
            output = out.getvalue().strip()
            assert 'Cluster not found' in  output


    def test_describe_existing_cluster_existing_clusters(self):
        sys.stdout.write("Describe all clusters, existing")
        r = RedshiftCommand()
        with captured_output() as (out, err):
            sys.stdout.write(r.do_redshift('describe'))
            output = out.getvalue().strip()
            assert 'redshift-cluster-2' in  output

    # def test_describe_non_existent_cluster(self):
    #     print("Describe non existent")
    #     r = RedshiftCommand()
    #     # args = docopt(doc, ["describe", "cl1"])
    #     with captured_output() as (out, err):
    #         print(r.do_redshift('describe cl2'))
    #         output = out.getvalue().strip()
    #         assert 'Cluster not found' in  output
    #
    #
    # def test_describe_existing_cluster(self):
    #     print("Describe existing")
    #     r = RedshiftCommand()
    #     with captured_output() as (out, err):
    #         print(r.do_redshift('describe redshift-cluster-2'))
    #         output = out.getvalue().strip()
    #         assert 'redshift-cluster-2' in  output
