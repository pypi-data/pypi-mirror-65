# coding: utf-8


from __future__ import print_function

import argparse
import atexit
import logging
import os
import sched
import signal
import sys
import time
import traceback
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from typing import Union

import six
from crontab import CronTab


def reset_log_to(log_file: str, log_level: int = logging.DEBUG, logger_name: str = None) -> None:
    global logger
    logger = logging.getLogger(logger_name)
    logger.handlers = []
    logger.setLevel(logging.DEBUG)

    if log_file is None:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(levelname)s]%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s]%(message)s")
        handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=15)
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        error_formatter = logging.Formatter(
            "[%(asctime)s][%(levelname)s][%(funcName)s][%(pathname)s:%(lineno)d]%(message)s")
        error_handler = TimedRotatingFileHandler(log_file + '.wf', when='midnight', backupCount=15)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(error_formatter)
        logger.addHandler(error_handler)


def goodbye(pidfile: str) -> None:
    os.remove(pidfile)
    logger.info('exit, {} removed'.format(pidfile))


def daemonlize(pidfile: str, stdin: str = '/dev/null', stdout: str = '/dev/null', stderr: str = '/dev/null') -> None:
    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError("fork 1 failed: {}".format(e))

    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError("fork 2 failed: {}".format(e))

    sys.stdout.flush()
    sys.stderr.flush()

    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)

    atexit.register(goodbye, pidfile)

    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


def print_schedule(epoch: float) -> None:
    s = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(round(epoch)))
    logging.info("will run at {}".format(s))


def scheduledTask(PIDFILE: str, LOGFILE: str, log_level, interval: Union[float, str], logger_name: str = None,
                  buildin_args: bool = False):
    cron = None
    if isinstance(interval, six.string_types):
        cron = CronTab(interval)

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parser = argparse.ArgumentParser()
            parser.add_argument('action')

            _, unknown = parser.parse_known_args()  # this is an 'internal' method
            # which returns 'parsed', the same as what parse_args() would return
            # and 'unknown', the remainder of that
            # the difference to parse_args() is that it does not exit when it finds redundant arguments

            for arg in unknown:
                if arg.startswith(("-", "--")):
                    # you can pass any arguments to add_argument
                    parser.add_argument(arg)

            xargs = parser.parse_args()
            action = xargs.action
            args_dict = vars(xargs)
            del args_dict['action']
            if action == 'start':
                try:
                    daemonlize(PIDFILE, stdout=LOGFILE, stderr=LOGFILE)
                except RuntimeError as e:
                    print(e, file=sys.stderr)
                    raise SystemExit(1)

                reset_log_to(LOGFILE, log_level, logger_name)

                s = sched.scheduler(time.time, time.sleep)
                t = time.time()

                def do_something(time_to_run, sc):
                    try:
                        if buildin_args:
                            kwargs["_time"] = time_to_run
                            kwargs["_action"] = "start"
                        kwargs.update(args_dict)
                        func(**kwargs)
                    except Exception as e:
                        logger.error(e)
                        traceback.print_exc(file=sys.stderr)

                    if cron:
                        time_to_run = time.time() + cron.next(default_utc=False)
                        print_schedule(time_to_run)

                    else:
                        assert interval > 0
                        while time_to_run < time.time():
                            time_to_run += interval

                    s.enterabs(time_to_run, 1, do_something, (time_to_run, sc,))

                if cron:
                    time_to_run = time.time() + cron.next(default_utc=False)
                    print_schedule(time_to_run)
                    s.enterabs(time_to_run, 1, do_something, (time_to_run, s,))
                else:
                    s.enter(0, 1, do_something, (t, s,))
                s.run()

            elif action == 'stop':
                if os.path.exists(PIDFILE):
                    with open(PIDFILE) as f:
                        os.kill(int(f.read()), signal.SIGTERM)
                else:
                    print('not running', file=sys.stderr)
                    raise SystemExit(0)
            elif action == 'status':
                if os.path.exists(PIDFILE):
                    print('running')
                else:
                    print('not running')
            elif action == 'run':
                reset_log_to(None, logger_name=logger_name)
                kwargs.update(args_dict)
                if buildin_args:
                    kwargs["_action"] = "run"
                func(**kwargs)
            else:
                print('unknown action {}'.format(xargs.action), file=sys.stderr)
                raise SystemExit(1)

        return wrapper

    return decorate
