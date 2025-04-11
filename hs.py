from shutil import copy as cp
from shutil import move as mv
from os import getcwd as pwd
from os import chdir as cd
from time import localtime
from pathlib import Path
from math import ceil
import os
import sys
import base64


class ANSI():
    COLOR = {}
    class FG:
        codes = {'black':30,'red':31,'green':32,
                 'yellow':33,'blue':34,'purple':35,
                 'cyan':36,'Bblack':90,'Bred':91,
                 'Bgreen':92,'Byellow':93,'Bblue':94,
                 'Bpurple':95,'Bcyan':96}

    class BG:
        codes = {'black':40,'red':41,'green':42,
                 'yellow':43,'blue':44,'purple':45,
                 'cyan':46,'Bblack':100,'Bred':101,
                 'Bgreen':102,'Byellow':103,'Bblue':104,
                 'Bpurple':105,'Bcyan':106} 
                 
    class ST:
        codes = {'reset':'0;0','bold':1,'dim':2,
                 'italic':3, 'underline':4}
 
    def init():
        for i in ANSI.FG.codes.keys():
            ANSI.COLOR['FG_{}'.format(i)] = '\33[{}m'.format(ANSI.FG.codes[i])
        for i in ANSI.BG.codes.keys():
            ANSI.COLOR['BG_{}'.format(i)] = '\33[{}m'.format(ANSI.BG.codes[i])
        for i in ANSI.ST.codes.keys():
            ANSI.COLOR['ST_{}'.format(i)] = '\33[{}m'.format(ANSI.ST.codes[i])

    def format(phrase):
        array = phrase.split('{')
        tmp_array = []
        for i in array:
            if '}' in i:
                array2 = i.split('}')
                for j in array2:
                    tmp_array.append(j)
            else:
                tmp_array.append(i)

        array = tmp_array
        for i in range(len(array)):
            if array[i] in ANSI.COLOR.keys():
                array[i] = ANSI.COLOR[array[i]]
                
        return(''.join(array))    

ANSI.init()
cformat = ANSI.format


class console:
    '''
    '''
    sym = {}
    sym['cmd'] = cformat('{FG_green}${FG_purple}>{ST_reset}')
    sym['+'] = cformat('{FG_blue}[{FG_green}+{FG_blue}]{ST_reset}')
    sym['*'] = cformat('{FG_blue}[{FG_purple}*{FG_blue}]{ST_reset}')
    sym['!'] = cformat('{FG_blue}[{FG_red}!{FG_blue}]{ST_reset}')
    sym['.'] = '   '

    def out(msg, mode='*'):
        print('{} {}'.format(console.sym[mode], msg))

        
class threadz(object):
    '''wrapper for multithreading:
    ARGS:
       1. function
       2. function args as tuple
       3. number of threads as int

    output of threadz stored in (threadz object).result

    Ex.
       t = threadz()
       t.run(function,
             args,
             number of threads)'''

    result = dict()

    def __init__(self):
        pass

    def wrapper(obj, func, key, args):
        obj.result[key] = func(args)

    def run(self, function, targs, runs=1, wait=False):
        _threads_ = []

        for i in range(runs):
            pargs = (self, function, str(i),)
            all_args = pargs + ((targs),)
            _threads_.append(threading.Thread(target=threadz.wrapper, args=all_args))

        for thread in _threads_:
            thread.start()

        if wait:
            for thread in _threads_:
                thread.join()


def touch(fname, times=None):
    '''Updates the modified time of a file without changing the
    contents of it much like the touch command in 'nix systems.'''
    if os.path.exists(fname):
        os.utime(fname, times)
    else:
        with open(fname, 'w+') as openfile:
            openfile.write('')


def cat(File, numbered=False, less=True, ret=False):
    '''
        Displays contents of a file to interpreter much like the
        cat command in 'nix systems.
    '''
    if less:
        term_rows = os.get_terminal_size()[1]

    ret_list = list()
    with open(File) as i:

        num_indx  = 1
        less_indx = 0

        for j in i.readlines():
            output = j.strip('\n')
            if numbered:
                output = '{}{}{} {}'.format(ANSI.COLOR['FG_green'],num_indx,ANSI.COLOR['ST_reset'],output)

            if ret:
                ret_list.append(output)
                continue

            print(output)

            if less:
                if (less_indx == (term_rows - 3)):
                    print('{}press [enter] to continue...{}'.format(ANSI.COLOR['FG_green'],ANSI.COLOR['ST_reset']), end='')
                    input()
                    less_indx = 0

            num_indx += 1
            less_indx += 1

    if ret:
        return ret_list


# def proj_path():
#     if getattr(sys, 'frozen', False):
#         progDir = os.path.dirname(sys.executable)
#     else:
#         progDir = os.path.dirname(os.path.realpath(__file__))
#     return(progDir)
    

def time_stamp(sdate=False, stime=True, fs_mode=True):
    '''
        WORK HERE!
    '''
    tmp = localtime()
    timestamp = ''
    if sdate:
        timestamp = '{}{}{}'.format(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)

    if sdate and stime:
        if fs_mode:
            timestamp = timestamp + '_'
        else:
            timestamp = timestamp + '@'            

    if stime:
        if fs_mode:
            time_sep = '-'
        else:
            time_sep = ':'

        timestamp = timestamp + '{}{}{}{}{}'.format(
                str(tmp.tm_hour).zfill(2), time_sep,
                str(tmp.tm_min).zfill(2), time_sep,
                str(tmp.tm_sec).zfill(2))

    return(timestamp)


def stringx(execString, verbose=False, shell=None, wait=True, decode='ascii'):
    '''wrapper for subprocess.Popen'''
    if (shell == None):
        if (sys.platform == 'Windows'):
            shell=True
        elif (sys.platform == 'Linux'):
            shell=False

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
              shell=shell)

    try:
        # Tries to return output of system call.
        # *Will be unsuccessful if 'wait' is False.
        for line in iter(p.stdout.readline, b''):
            formatted = line.strip().decode(decode)
            if verbose:
                print(formatted)
            Return[0].append(formatted)
    except:
        pass

    Return.append(p.pid)
    return(Return)
    p.communicate()


def genx(execString, shell=None, decode='ascii'):
    '''wrapper for subprocess.Popen'''
    if (shell == None):
        if (sys.platform == 'Windows'):
            shell=True
        elif (sys.platform == 'Linux'):
            shell=False

    from shlex import split as shlexSplit
    import subprocess as sp

    IOdevice = sp.PIPE
    p = sp.Popen(shlexSplit(execString),
              stdout=IOdevice,
              stderr=IOdevice,
              stdin=sp.DEVNULL,
              shell=shell)

    try:
        # Tries to return output of system call.
        # *Will be unsuccessful if 'wait' is False.
        for line in iter(p.stdout.readline, b''):
            formatted = line.strip().decode(decode)
            yield(formatted)
    except:
        pass

    p.communicate()


def which(exe):
    ret = []
    for i in os.environ['PATH'].split(';'):
        try:
            if (exe in os.listdir(r'{}'.format(i))):
                ret.append(i)
        except:
            pass

    if (len(ret) > 0):
        return(ret)


def find(pattern, searchpath, sensitive=False, recursive=True, verbose=False):
    '''Returns matching items of a query. "pattern" must match "item(s)"
    Capable of searching directories as well as lists implicitly.'''
    results = list()
    if not sensitive:
        pattern = pattern.lower()

    if recursive:
        for root, dirs, files in os.walk(searchpath):
            for name in dirs:
                if verbose:
                    print('looking in {}...'.format(os.path.join(root, name)))
                if not sensitive:
                    name = name.lower()
                if (pattern in name):
                    results.append(os.path.join(root, name))

            for name in files:
                if not sensitive:
                    name = name.lower()
                if (pattern in name):
                    results.append(os.path.join(root, name))

    else:
        List = os.listdir(searchpaths)
        for i in List:
            if verbose:
                print(i)
            if not sensitive:
                i = i.lower()
            if (pattern in i):
                results.append(os.path.join(searchpaths, i))

    return(results)


class ls_vars:
    '''
    define ls settings
        func:
        colors:
        atribs:
    '''
    func = print
    colors = [(ANSI.COLOR['FG_red'] + ANSI.COLOR['ST_bold']),
              (ANSI.COLOR['FG_Bblack']),
              (ANSI.COLOR['FG_Bblack'] + ANSI.COLOR['BG_Bred']),
              (ANSI.COLOR['ST_reset'])]

    atribs = []


def ls(_dir='.', atribs=None, tree=False, func=None, colors=None, end='\n'):
    '''
    args:
        _dir :
        atribs :
        tree :
        func :
        colors :
            colors[0] : files color
            colors[1] : directories color
            colors[2] : symlinks color
            colors[3] : color reset

        some settings can be defined in ls_vars for persistance
    '''
    if (func == None):
        func = ls_vars.func
    if (colors == None):
        colors = ls_vars.colors
    if (atribs == None):
        atribs = ls_vars.atribs

    items     = os.listdir(_dir)
    num_items = len(items)
    col_amt   = (ceil(num_items/3))
    digits    = len(str(num_items))

    try:
        col_size = os.get_terminal_size()[0]
    except:
        col_size = 40

    cwd = os.getcwd()
    new_cwd = []
    indx = 0
    for i in cwd.split(os.path.sep):
        if (indx % 2 == 0):
            color = colors[0]
        else:
            color = colors[1]
        new_cwd.append('{}{}{}'.format(color,i,ANSI.COLOR['ST_reset']))
        indx += 1
    print('/'.join(new_cwd))
    print()


    # build formated items list and find lengths
    #    add color
    #    add number
    # build list of [[display_item, length]]
    #===========================================
    long_num = 0
    for i in range(len(items)):
        item    = items[i]
        absitem = os.path.join(_dir, item)
        num     = str(i).zfill(digits)

        # h accounts for the zero in range()
        h = (i+1)
        if not (h > (col_amt * 2)):
            char_length = (len(item) + len(num) + 1)

            if (char_length > long_num):
                long_num = char_length

            if (h == col_amt):
                col1_buffer = (long_num + 3)
                long_num = 0
            elif (h == (col_amt * 2)):
                col2_buffer = (long_num + 3)

        color = colors[1]
        if (os.path.isfile(absitem)):
            color = colors[0]
        # elif (os.path.isdir(absitem)):
        #     color = colors[1]
        if Path(absitem).is_symlink():
            color = colors[2]

        items[i] = ['{}. {}{}{}'.format(num,color,item,colors[3]),
                    char_length]

    # split list into 3 columns
    #==========================
    base = 0
    rang = col_amt
    cols = {}
    for i in range(3):
        colname = 'col{}'.format(i)
        if (i == 2):
            cols[colname] = items[base:]
        else:
            cols[colname] = items[base:rang]
        base = rang
        rang += rang


    # print numbered, colored, and seperated (buffered) items
    #========================================================
    for i in range(len(cols['col0'])):
        try:
            # print first column or break
            func(cols['col0'][i][0], end=(' ' * (col1_buffer - cols['col0'][i][1])))
            # print second column or break
            func(cols['col1'][i][0], end=(' ' * (col2_buffer - cols['col1'][i][1])))
        except:
            print('{}'.format(end))
            break

        try:
            # print last column or try to cycle back
            func(cols['col2'][i][0])
        except:
            print()


if __name__ == "__main__":
    pass
