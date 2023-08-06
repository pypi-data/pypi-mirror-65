#! Python3
'''Utilities Max has re-written from his VBA utilities
Put this in the user site folder to enable easy import without bothering to package it
From a terminal window use the command "python -m site --user-site" to find the right folder
Note that imported files do not see global variables.  You can't set logName in the module
that imports myUtilities
'''
# Great tutorial on logging is here https://www.datadoghq.com/blog/python-logging-best-practices/
# For basic logging, put these lines at the start of each module
from pathlib import Path
import logging
import sys
from pathlib import Path

logDir = Path.home().joinpath('Documents/Logs')
logName = Path(__name__).stem + '.log'
logFile = str(logDir.joinpath(logName))
print(logFile)
# Create the output directory if necessary
if not Path(logDir).exists():
    Path(logDir).mkdir()
# Configure a basic logger
# logging.basicConfig(filename=logFile,level=logging.DEBUG, format='{asctime} {filename} {levelname} {message}',
#     style='{', datefmt='%H:%M:%S')      # Can't find how to use '{' format in datefmt parameter
# logging.basicConfig(filename=logFile,level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
'''
NOTE WELL: 'logging.basicConfig' does NOTHING if a handler has been set up already.
Thus we have to delete handlers to change logging file on the fly
https://stackoverflow.com/questions/13839554/how-to-change-filehandle-with-python-logging-on-the-fly-with-different-classes-a

To set up a module level logger, you have to create one outside a function so that it
and the filehandler and console handler are available to other functions.
So, create one defaulting to overwrite any existing log file, and rely on the programmer
to change to a new one for appending if the programmer desires that.

By defining logging at the module level, we can do setLevel in one function and have it be effective everywhere

Setting up logging the long way
'''
# Create a filehandler and set it to log DEBUG and above
filehandler = logging.FileHandler(logFile, 'w', encoding = "UTF-8")  # Overwrite any existing logfile
# filehandler = logging.FileHandler(logName, 'a', encoding = "UTF-8")     # Append to any existing logfile
filehandler.setLevel(logging.DEBUG)

# Create a console handler with a higher log level
consolehandler = logging.StreamHandler()
consolehandler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers. Use {} style.
formatter = logging.Formatter('{asctime} {filename} {levelname} {message}', style='{', datefmt='%H:%M:%S')
# Create a bare formatter, one with only the message
bare = logging.Formatter('{message}', style='{')
filehandler.setFormatter(formatter)
consolehandler.setFormatter(formatter)

# Get the root logger
logger = logging.getLogger()
for hdlr in logger.handlers[:]:
    if isinstance(hdlr, logging.FileHandler):
        logger.removeHandler(hdlr)
# add the handlers to the logger
logger.addHandler(filehandler)
logger.addHandler(consolehandler)


# To change the loglevel on the fly use:
# logger.setLevel(logging.DEBUG)

# To change the output file is difficult
# We have to delete handlers to change the logging output file on the fly
# IF you know the filehandler you want to redirect, you can do:
# filehandler.close()
# filehandler.baseFilename = os.path.abspath('/home/max/Documents/NEWNAME.LOG')
# logger.debug('new message to new file?')

# If you don't know the name of the active filehandler, you have to delete them all:
# Create new filehandler for append with name = logName, a full file spec
# filehandler = logging.FileHandler(logName, 'a')    # use 'w' for overwrite
# Define and set formatter, then add new handler
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     filehandler.setFormatter(formatter)
#     logger = logging.getLogger()  # root logger
#     for hdlr in logger.handlers[:]:  # remove all old handlers
#         if isinstance(hdlr, logging.FileHandler):
#             logger.removeHandler(hdlr)
#     logger.addHandler(filehandler)  # set the new handler
# You cannot do the above in a function, because the logger is local to the function.
# When the function is complete, then the new logger is destroyed along with everything else in the function's scope.


# def logging_examples():
#     import logging
#     # Enabling logging with a format
#     logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#     logging.debug('Logging is enabled.')
#     # Turn logging on or off
#     logging.disable(logging.CRITICAL)  # This disables all logging
#     logging.debug('Logging should be disabled.')
#     logging.disable(logging.NOTSET)  # and this re-enables it.
#     logging.debug('Logging should be re-enabled.')
#
#
# def logger_example():
#     import logging
#     logger = logging.getLogger()  # this gets the root logger
#     logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
#     logging.debug('Logging is enabled.')
#     print('The logger.disabled value is ' + str(logger.disabled))
#     logger.disabled = True
#     logger.debug('Logging is disabled.')
#     print('The logger.disabled value is ' + str(logger.disabled))
#     logger.disabled = False
#     logger.debug('Logging is re-enabled.')


def log(*objects, sep=" ", end="", file=sys.stdout, flush=False, lvl=logging.DEBUG):
    # Using same arguments as the print statement to make it work if I convert a print statement to a log statement
    # Note that echoing to the console is goverened by the console handler, above
    try:
        msg = sep.join(str(obj) for obj in objects)
        # old_lvl = logger.getEffectiveLevel()
        # logger.setLevel(lvl)
        if lvl==logging.DEBUG:
            logger.debug(msg)
            print(msg, sep, end)
        elif lvl==logging.INFO:
            logger.info(msg)
            # print(msg, sep, end)
        elif lvl==logging.WARNING:
            logger.warning(msg)
            # print(msg, sep, end)
        elif lvl==logging.ERROR:
            logger.error(msg)
            # print(msg, sep, end)
        else:
            logger.critical(msg)
            print(msg, sep, end)
        # logger.setLevel(old_lvl)
    except UnicodeEncodeError as err:
        logger.warning('Log entry contained unicode characters that cannot be written to ASCII file.  Skipping entry.')
    except:
        logger.warning('Unhandled error in log function.')


def writelog(*objects, logName='log.txt', logDir=Path.home().joinpath('Documents/Logs'), overwrite=False,
             sep=" ", end="\n", file=sys.stdout, flush=False, lvl = logging.DEBUG):
    '''Appends entry by default to log.txt in /home/max/Documents/Logs,
    Mimics print function paramenters.  Ignores logging level.
    :param msg:
    :type msg:
    :param logName: The name of the log file, without path
    :type logName: str
    :param logDir: The path to the folder containing the log file, without the file name
    :type logDir: str
    :param overwrite: If true, start a new log
    :type overwrite: bool
    :return:
    :rtype:
    '''
    # Using *objects just like the print command
    msg = sep.join(str(obj) for obj in objects)
    if not Path(logDir).exists():
        Path(logDir).makedir()
    logfile = Path(logDir).joinpath(logName)
    if overwrite:
        log = open(logfile, 'w')
    else:
        log = open(logfile, 'a')
    log.write(msg + '\n')
    print(msg, sep=sep, end=end, file=file, flush=flush)
    log.close()


'''def select(case):  # How to emulate a VBA Select Case statement in Python
    caseOne = ('a', 'b', 'c')
    caseTwo = (1, 2, 3)
    if False:
        pass  # You must have code here, and if you do, PyCharm will mark it as unreachable.
        # pass is a noop (no operation, do nothing)
    elif case in caseOne:
        print('Case a executed')
    elif case in caseTwo:
        print('Case 1 executed')
    else:
        print('Case else executed')
'''


def delim(str) -> str:
    if str is not None:
        return '"' + str + '"'


def select_a_file(root='.', msg='Browse to the desired file.') -> str:
    import PySimpleGUI as sg

    layout = [[sg.Text(msg)],
              [sg.InputText(size=(65,2)), sg.FileBrowse(initial_folder=root)],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('File Browser', layout)
    # (event, (source_filename,)) = window.Read()
    (event, values) = window.Read()
    source_filename = values['Browse']      # Found by debug inspecting the return values dictionary

    print(event, source_filename)
    if event=='Cancel':
        window.Close()
        return
    else:
        window.Close()
        return source_filename


def select_a_folder(root='.') -> str:
    import PySimpleGUI as sg

    layout = [[sg.Text('Browse to the desired folder.')],
              [sg.InputText(), sg.FolderBrowse(initial_folder=root)],
              [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Folder Browser', layout)
    (event, values) = window.Read()
    source_filename = values[0]
    print(event, source_filename)
    if event=='Cancel':
        window.Close()
        return
    else:
        window.Close()
        return source_filename


# def all_in_one():
#     import PySimpleGUI as sg
#
#     layout = [[sg.Text('All graphic widgets in one window!', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
#               [sg.Text('Here is some text.... and a place to enter text')],
#               [sg.InputText()],
#               [sg.Checkbox('My first checkbox!'), sg.Checkbox('My second checkbox!', default=True)],
#               [sg.Radio('My first Radio!     ', "RADIO1", default=True), sg.Radio('My second Radio!', "RADIO1")],
#               [sg.Multiline(default_text='This is the default Text should you decide not to type anything', )],
#               [sg.InputCombo(['Combobox 1', 'Combobox 2'], size=(20, 3)),
#                sg.Slider(range=(1, 100), orientation='h', size=(35, 20), default_value=85)],
#               [sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(30, 6)),
#                sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=25),
#                sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=75),
#                sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=10)],
#               [sg.Text('_' * 100, size=(70, 1))],
#               [sg.Text('Choose Source and Destination Folders', size=(35, 1))],
#               [sg.Text('Source Folder', size=(15, 1), auto_size_text=False, justification='right'),
#                sg.InputText('Source'),
#                sg.FolderBrowse()],
#               [sg.Text('Destination Folder', size=(15, 1), auto_size_text=False, justification='right'),
#                sg.InputText('Dest'),
#                sg.FolderBrowse()],
#               [sg.Submit(), sg.Cancel(), sg.Button('Customized', button_color=('white', 'green'))]]
#
#     event, values = sg.Window('Everything bagel', layout, auto_size_text=True, default_element_size=(40, 1)).Read()

#
# def pathlibExamples():
#     from pathlib import Path
#
#     filename = Path("source_data/text_files/raw_data.txt")
#
#     print(filename.name)
#     # prints "raw_data.txt"
#
#     print(filename.suffix)
#     # prints "txt"
#
#     print(filename.stem)
#     # prints "raw_data"
#
#     if not filename.exists():
#         print("Oops, file doesn't exist!")
#     else:
#         print("Yay, the file exists!")


def fileExt(filename: str) -> str:
    '''
    Return just the file extension, without the separator, in lower case
    :param filename:
    :type filename: str
    :return: ext
    :rtype: str
    '''
    from pathlib import Path
    return Path(filename).suffix[1:].lower()  # removing the separator


def bareFilename(filename: str) -> str:
    '''
    Returns the filename without the extension
    :param filename:
    :type filename: str
    :return: just the filename without the exention
    :rtype: str
    '''
    from pathlib import Path
    return Path(filename).stem


# def walklevelOLD(some_dir, level=1):
#     # restricts os.walk to a single level
#     import os.path
#     from pathlib import Path
#     some_dir = some_dir.rstrip(os.path.sep)
#     assert os.path.isdir(some_dir)
#     num_sep = some_dir.count(os.path.sep)
#     for root, dirs, files in os.walk(some_dir):
#         yield root, dirs, files
#         num_sep_this = root.count(os.path.sep)
#         if num_sep + level <= num_sep_this:
#             del dirs[:]

def walklevel(some_dir, level=1):
    # restricts os.walk to a single level.   Updated to use pathlib instead of os.path
    import os
    from pathlib import Path
    some_dir = some_dir.rstrip(os.sep)
    assert Path(some_dir).is_dir
    num_sep = some_dir.count(os.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def reverse(s: str):
    return s[::-1]  # equivalent to s[-1:-(len(s):1]


def o(numb):
    '''
    Returns the ordinal version of number, e.g. "33rd"
    :param numb:
    :return: ordinal version of number, e.g. "33rd"
    From https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    user was   https://stackoverflow.com/users/2756187/houngan
    '''
    if numb < 20:  # determining suffix for < 20
        if numb==1:
            suffix = 'st'
        elif numb==2:
            suffix = 'nd'
        elif numb==3:
            suffix = 'rd'
        else:
            suffix = 'th'
    else:  # determining suffix for > 20
        tens = str(numb)
        tens = tens[-2]
        unit = str(numb)
        unit = unit[-1]
        if tens=="1":
            suffix = "th"
        else:
            if unit=="1":
                suffix = 'st'
            elif unit=="2":
                suffix = 'nd'
            elif unit=="3":
                suffix = 'rd'
            else:
                suffix = 'th'
    return str(numb) + suffix


def main():
    print(sys.getdefaultencoding())     # On QuietPC this is UTF-8
    pass
    # # logging_examples()
    # # logger_example()
    # logging.info('an informational log entry')
    # logging.debug('a debug log entry')


if __name__=="__main__":
    main()
    # pass
