import shutil
import subprocess
import virtualenv
import os
import pytest

skip = 'DISCO_LIVE_TESTS' not in os.environ
reason = ('Please pass an environment variable DISCO_LIVE_TESTS if you want'
          ' to run the integration tests on a live environment. Don\'t forget'
          ' to set environment variables for connecting to Dis.co servers')
test_file_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.skipif(skip, reason=reason)
class TestJobsDiscoMP(object):
    def test_pool(self):
        venv_temp_dir = self._create_and_activate_venv()
        venv_pip_path = os.path.join(venv_temp_dir, "bin", "pip")
        venv_python_path = os.path.join(venv_temp_dir, "bin", "python")
        subprocess.call([venv_pip_path, 'install', 'dill'])
        install_return_code = subprocess.call([venv_pip_path, "install", '.'])
        assert install_return_code == 0
        out = subprocess.Popen([venv_python_path, os.path.join(test_file_path, 'test_files/pool_helper.py')],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        assert stdout == b'[0, 1000, 8000, 27000, 64000, 125000, 216000, 343000, 512000, 729000]\n'

    def test_process(self):
        venv_temp_dir = self._create_and_activate_venv()
        venv_pip_path = os.path.join(venv_temp_dir, "bin", "pip")
        venv_python_path = os.path.join(venv_temp_dir, "bin", "python")
        subprocess.call([venv_pip_path, 'install', 'dill'])
        install_return_code = subprocess.call([venv_pip_path, "install", '.'])
        assert install_return_code == 0

        out = subprocess.Popen([venv_python_path, os.path.join(test_file_path, 'test_files/process_helper.py')],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        print("stdout is: ", stdout, " stderr is ", stderr)
        assert stdout == b'JobStatus.done\n'

    @classmethod
    def _create_and_activate_venv(cls):
        venv_temp_dir = cls._venv_temp_dir()

        cls._delete_venv()

        virtualenv.create_environment(venv_temp_dir)
        path = os.path.join(venv_temp_dir, "bin", "activate_this.py")
        exec(open(path).read(), {'__file__': path})

        return venv_temp_dir

    @staticmethod
    def _venv_temp_dir():
        return os.path.join(os.path.expanduser("~"), ".venv-test-temp")

    @classmethod
    def _delete_venv(cls):
        try:
            shutil.rmtree(cls._venv_temp_dir())
        except OSError:
            return
