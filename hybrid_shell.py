from os import getcwd as pwd
from os import chdir as cd
import os, shutil

def posix_path(string):
    '''Makes path passed to function compatible with 'nix systems
    as well as the interpreter.'''
    import posixpath    
    return string.replace(os.path.sep, posixpath.sep)


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
    with open(fname, 'a'):
        os.utime(fname, times)


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


def hostUp(host, shell=False):
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



def WakeOnLan(mac_address, broadcast_address):
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


def stringX(execString, shell=False, wait=True, decode='utf-8', bufsize=1):
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
        try:
            for root, dirs, files in os.walk(searchpaths):
                for name in dirs:
                    if fnmatch(name, pattern):
                        results.append(os.path.join(root, name))
                        
                for name in files:
                    if fnmatch(name, pattern):
                        results.append(os.path.join(root, name))
        except:
            for i in searchpaths:
                if fnmatch(i, pattern):
                    results.append(i)
    else:
        List = os.listdir(searchpaths)
        for i in List:
            if fnmatch(i, pattern):
                results.append(os.path.join(searchpaths, i))            
        
    return results


def ls(path='.', ret=False, details=['type'], absPath=False, pattern='*'):
    '''Lists contents of a given directory with some bells and whistles.
    Requested detail types are defined in a list. Valid detail types are...    
    [mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime, type]'''
    from fnmatch import fnmatch
    from time import ctime
    from stat import S_ISREG
    from stat import S_ISDIR

    LIST = os.listdir(path)
    masterList = list()
    for i in LIST:
        try:
            fileList = list()
            if fnmatch(i, pattern):
                i = os.path.abspath(path + os.sep + i)
                fileList.append(i)
                detailsList = (str(os.stat(i).st_mode), str(os.stat(i).st_ino),
                            str(os.stat(i).st_dev), str(os.stat(i).st_nlink),
                            str(os.stat(i).st_uid), str(os.stat(i).st_gid),
                            "{:,}".format(int(round(os.stat(i).st_size / 1000))) + 'KB',
                            ctime(int(os.stat(i).st_atime)),
                            ctime(int(os.stat(i).st_mtime)),
                            ctime(int(os.stat(i).st_ctime)))
    
                if S_ISDIR(int(detailsList[0])):
                    detailsList = detailsList + ('dir',)
                elif S_ISREG(int(detailsList[0])):
                    detailsList = detailsList + ('file',)
    
                types = ['mode', 'ino', 'dev', 'nlink', 'uid', 'gid',
                         'size', 'atime', 'mtime', 'ctime', 'type']
    
                for j in details:
                    for k in range(len(types)):
                        if (j == types[k]):
                            fileList.append(detailsList[k])
    
            if (fileList != []):
                masterList.append(fileList)
        except:
            masterList.append([i, 'ERROR'])
        
    if not absPath:
        for i in range(len(masterList)):
            file = os.path.basename(masterList[i][0])
            masterList[i].remove(masterList[i][0])
            masterList[i].insert(0, file)


    if not (ret):
        try:
            from prettytable import PrettyTable
            headers = ['name'] + details
            printout = PrettyTable(headers)
            printout.align['name'] = 'l'
            for i in masterList:
                printout.add_row(i)
            print(printout)
            print()
        except:
            for i in masterList:
                print(i)            
    else:
        return masterList


if __name__ == "__main__":
    pass
