# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from os.path import dirname, join
import time
from atelier.test import TestCase
import docker
import getlino

client = docker.from_env()


class DockerTestMixin:
    docker_tag = None

    def setUp(self):
        if self.docker_tag is None:
            return
        self.container = client.containers.run(
            self.docker_tag, command="/bin/bash", user='lino', tty=True, detach=True)

    def tearDown(self):
        if self.docker_tag is None:
            return
        self.container.stop()

    def run_docker_command(self, command):
        #exit_code, output = container.exec_run(command, user='lino')
        print("===== run in {} : {} =====".format(self.container, command))
        assert not "'" in command
        exit_code, output = self.container.exec_run(
            """bash -c '{}'""".format(command), user='lino')
        output = output.decode('utf-8')
        if exit_code != 0:
            msg = "%s  returned %d:\n-----\n%s\n-----" % (
                command, exit_code, output)
            self.fail(msg)
        else:
            return output

    def test_production_server(self):
        """

        Test the instrucations written on
        https://www.lino-framework.org/admin/install.html

        """
        # load bash aliases
        # res = self.run_docker_command(
        #    container, 'source /etc/getlino/lino_bash_aliases')

        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        # create and activate a virtualenv
        self.run_docker_command(
            'sudo mkdir -p /usr/local/lino/shared/env')
        self.run_docker_command(
            'cd /usr/local/lino/shared/env && sudo chown root:www-data .  && sudo chmod g+ws . && virtualenv -p python3 master')
        res = self.run_docker_command(
            'source /usr/local/lino/shared/env/master/bin/activate && sudo  pip3 install -e .')
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        # print(self.run_docker_command(container, "sudo cat /etc/getlino/lino_bash_aliases"))
        res = self.run_docker_command(
            '. /usr/local/lino/shared/env/master/bin/activate &&  sudo getlino configure --batch --db-engine postgresql --monit')
        self.assertIn('getlino configure completed', res)
        res = self.run_docker_command(
            '. /usr/local/lino/shared/env/master/bin/activate && sudo getlino startsite noi noi1 --batch --dev-repos "lino xl noi"')
        self.assertIn('The new site noi1 has been created.', res)
        res = self.run_docker_command(
            '. /usr/local/lino/shared/env/master/bin/activate && sudo getlino startsite cosi cosi1 --batch --dev-repos "lino xl cosi"')
        self.assertIn('The new site cosi1 has been created.', res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go cosi1 && . env/bin/activate &&  ls -l')
        print(res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go cosi1 && source  /etc/getlino/lino_bash_aliases && . env/bin/activate  &&  pull.sh')
        print(res)
        res = self.run_docker_command(
            '. /etc/getlino/lino_bash_aliases && go cosi1 && ./make_snapshot.sh')
        print(res)
        # Need to wait 10 sec until the supervisor finish restarting
        time.sleep(10)
        res = self.run_docker_command(
            '/usr/local/bin/healthcheck.sh')
        self.assertNotIn('Error', res)

    def test_developer_env(self):
        """

        Test the instrucations written on
        https://www.lino-framework.org/dev/install/index.html

        """
        self.run_docker_command(
            'mkdir ~/lino && virtualenv -p python3 ~/lino/env')
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && pip3 install -e . ')
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino configure --batch --db-engine postgresql')
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite noi mynoi1 --batch --dev-repos "lino xl noi"')
        self.assertIn('The new site mynoi1 has been created.', res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite cosi mycosi1 --batch --dev-repos "lino xl cosi"')
        self.assertIn('The new site mycosi1 has been created.', res)
        res = self.run_docker_command(
            '. ~/.lino_bash_aliases && go mycosi1 && . env/bin/activate && ls -l')
        print(res)
        res = self.run_docker_command(
            '. ~/.lino_bash_aliases && go mycosi1 && . env/bin/activate && pull.sh')
        print(res)

    def test_contributor_env(self):
        """

        Test the instrucations written on
        https://www.lino-framework.org/team/index.html

        """

        self.run_docker_command(
            'mkdir ~/lino && virtualenv -p python3 ~/lino/env')
        res = self.run_docker_command(
            'ls -l')
        self.assertIn('setup.py', res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && pip3 install -e . ')
        self.assertIn("Installing collected packages:", res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino configure --clone --devtools --redis --batch ')
        self.assertIn('getlino configure completed', res)
        # print(self.run_docker_command(container, "cat ~/.lino_bash_aliases"))
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite noi mynoi1 --batch')
        self.assertIn('The new site mynoi1 has been created.', res)
        res = self.run_docker_command(
            '. ~/lino/env/bin/activate && getlino startsite cosi mycosi1 --batch')
        self.assertIn('The new site mycosi1 has been created.', res)
        res = self.run_docker_command(
            '. ~/.lino_bash_aliases && go mycosi1 && . env/bin/activate && ls -l')
        print(res)
        res = self.run_docker_command(
            '. ~/.lino_bash_aliases && go mycosi1 && . env/bin/activate && pull.sh')
        print(res)


class UbuntuDockerTest(DockerTestMixin, TestCase):
    docker_tag = "getlino_debian"

class DebianDockerTest(DockerTestMixin, TestCase):
    docker_tag = "getlino_ubuntu"
