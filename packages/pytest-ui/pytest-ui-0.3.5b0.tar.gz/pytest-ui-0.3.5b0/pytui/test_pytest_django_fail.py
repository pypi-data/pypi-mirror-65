from __future__ import absolute_import
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()

import logging
import pytest
import multiprocessing
from .plugin import PytestPlugin

from .logging_tools import get_logger, LogWriter

log_name = 'runner'
logger = get_logger(log_name)
pipe_logger = get_logger(log_name, 'pipe')
stdout_logger = get_logger(log_name, 'stdout')
stdout_logger_writer = LogWriter(stdout_logger)
stderr_logger = get_logger(log_name, 'stderr')
stderr_logger_writer = LogWriter(stderr_logger)

def process_run_tests():
    """ Class method as separate process entrypoint """

    # sys.stdout = stdout_logger_writer
    # sys.stderr = stderr_logger_writer

    # runner = cls(path, write_pipe=write_pipe, pipe_size=pipe_size,
    #              pipe_semaphore=pipe_semaphore)
    # exitcode, description = runner.run_tests(failed_only, filter_value)
    import mock
    runner = mock.Mock()
    exitcode = pytest.main(
        # ['ocm/cm']
        [
            # '-p', 'no:terminal',
            'crm/selfservice/tests/test_acc_useraccount_messages.py',
        ],
        plugins=[PytestPlugin(runner=runner, filter_value='')]
    )
    print(exitcode)
    # logger.info('Test run finished')
    # runner.pipe_send('run_finished')


def main():
    runner_process = multiprocessing.Process(
        target=process_run_tests,
        name='pytui-runner',
        args=()
    )
    runner_process.start()


if __name__ == '__main__':
    main()