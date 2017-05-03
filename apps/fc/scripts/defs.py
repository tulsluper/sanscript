import os
import json
import logging
import time
from paramiko import SSHClient, AutoAddPolicy


def load_data(filepath, default=None):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return default


def dump_data(filepath, data):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False


def run_with_locker(lockfile):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if not os.path.isfile(lockfile):
                open(lockfile, 'w').close()
                try:
                    function(*args, **kwargs)
                except Exception as e:
                    logging.warning('Exception: %s' %e)
                    logging.warning('EXIT')
                    pass
                os.remove(lockfile)
        return wrapper
    return real_decorator


def get_logger(logfile, loggername=''):
    open(logfile, 'w').close()
    os.environ['TZ'] = 'Europe/Kiev'
    time.tzset()
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(logfile)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    return logger


def ssh_run(args):
    system, address, username, password, commands = args
    address, port = address.split(':') if ':' in address else address, 22
    outs, errs, exception = {}, {}, None
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(address, port=port, username=username, password=password)
        for commandname, command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            out = stdout.read()
            err = stderr.read()
            if type(out) == bytes:
                out = out.decode("utf-8")
            if type(err) == bytes:
                err = err.decode("utf-8")
            outs[commandname] = out
            errs[commandname] = err
    except Exception as e:
        exception = e
    finally:
        client.close()
    return system, outs, errs, exception


