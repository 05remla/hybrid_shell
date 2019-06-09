from shutil import copy as cp
from shutil import move as mv
from os import getcwd as pwd
from os import chdir as cd
import threading
import os


class threadz(object):
    def __init__(self):
        self.result = dict()
      
    def wrapper(obj, func, key, *args, **kwargs):
        obj.result[key] = func(*args, **kwargs)

    def run(self, function, runs=1, *args, **kwargs):
        _threads_ = []

        for i in range(runs):
            wrapper_args = (self, function, str(i),)
            thread_args = wrapper_args + args              
            _threads_.append(threading.Thread(target=threadz.wrapper, args=thread_args, kwargs=kwargs))

        for thread in _threads_:
            thread.start()

        for thread in _threads_:
            thread.join()
            
            
def ps_aux():
    import psutil

    ret = []
    for proc in psutil.process_iter():
        try:
            ret.append([proc.name(), proc.pid])
        except:
            pass

    return ret


def touch(fname, times=None):
    '''Updates the modified time of a file without changing the
    contents of it much like the touch command in 'nix systems.'''
    try:
        with open(fname, 'a'):
            os.utime(fname, times)
    except:
        print('make the file')


def cat(File, numbered=False):
    '''Displays contents of a file to interpreter much like the
    cat command in 'nix systems.'''
    contents = list()
    with open(File) as i:
        List = i.readlines()
        for j in range(len(List)):
            if numbered:
                output = str(j + 1) + ' ' + List[j].strip('\n')
            else:
                output = List[j].strip('\n')
            contents.append(output)
    return contents


def alive(host, shell=False):
    from fnmatch import fnmatch
    from platform import system as OperSys
    operatingSystem = OperSys().lower()
    isHostUp = False

    if (operatingSystem == 'windows'):
        ping_str = "-n 1"
        shell = shell
    elif (operatingSystem == 'darwin'):
        ping_str = "-c 1"
        shell = shell

    args = "ping {} {}".format(ping_str, host)
    output = stringX(args, shell=shell)[0]

    for line in output:
        if fnmatch(line.lower(), '*ttl=*'):
            isHostUp = True

    return isHostUp


def wakeonlan(mac_address, broadcast_address):
    import struct, socket

    addr_byte = mac_address.split(':')
    hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
                                    int(addr_byte[1], 16),
                                    int(addr_byte[2], 16),
                                    int(addr_byte[3], 16),
                                    int(addr_byte[4], 16),
                                    int(addr_byte[5], 16))

    msg = b'\xff' * 6 + hw_addr * 16
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg, (broadcast_address, 9))
    s.close()


def stringx(execString, shell=False, wait=True, decode='ascii', bufsize=1):
    '''Runs a system command without forking from python.
    Able to return output of a given command to interpreter'''
    from shlex import split as shlexSplit
    import subprocess as sp
    Return = [[]]

    if (wait):
        IOdevice = sp.PIPE
    else:
        IOdevice = None

    p = sp.Popen(shlexSplit(execString),
              stdout=IOdevice,
              stderr=IOdevice,
              stdin=sp.DEVNULL,
              shell=shell,
              bufsize=bufsize)

    try:
        '''Tries to return output of system call.
        *Will be unsuccessful if 'wait' is False.'''
        for line in iter(p.stdout.readline, b''):
            Return[0].append(line.strip().decode(decode))
    except:
        pass

    Return.append(p.pid)
    return Return
    p.communicate()


def find(pattern, searchpaths, sensitive=False, recursive=True):
    '''Returns matching items of a query. "pattern" must match "item(s)"
    Capable of searching directories as well as lists implicitly.'''
    if sensitive: from fnmatch import fnmatchcase as fnmatch
    else: from fnmatch import fnmatch
    results = list()

    if recursive:
        for root, dirs, files in os.walk(searchpaths):
            for name in dirs:
                if fnmatch(name, pattern):
                    results.append(os.path.join(root, name))

            for name in files:
                if fnmatch(name, pattern):
                    results.append(os.path.join(root, name))

        for i in searchpaths:
            if fnmatch(i, pattern):
                results.append(i)
    else:
        List = os.listdir(searchpaths)
        for i in List:
            if fnmatch(i, pattern):
                results.append(os.path.join(searchpaths, i))

    return results


def ls(query='.', ret=False):
  items = sorted(os.listdir(query), key=str.lower)

  if ret:
    return items
  else:
    from pathlib import Path

    def dispatch_item(item, buffer, col):
      if (os.path.isfile(item)): color = '\033[92m'
      elif (os.path.isdir(item)): color = '\033[94m'
      if Path(item).is_symlink(): color = '\033[96m'
      item = os.path.split(item)[1]

      if (col == 1):
        print('{}{}{}'.format(
            color, item, (' ' * (buffer - len(item)))), end='')
      else:
        print('{}{}{}'.format(
            color, item, (' ' * (buffer - len(item)))))

    long = ((max(len(i) for i in items)) + 4)
    switch = int(round((len(items)+0.5)/2))

    for i in range(len(items)):
      dispatch_item(os.path.join(query,items[i]), long, 1)

      try:
        dispatch_item(os.path.join(query,items[i+switch]), long, 2)
      except:
        print('{}'.format('\033[0m'))
        break


if __name__ == "__main__":
    pass
