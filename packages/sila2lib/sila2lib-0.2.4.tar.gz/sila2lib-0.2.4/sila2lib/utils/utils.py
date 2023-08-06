"""_____________________________________________________________________

:PROJECT: SiLA2_python

*SiLA2 sila2_python installer skript*

:details: SiLA2 sila2_python installer.
          Installing core SiLA2 python library
          and optional tools interactivly.

          !! IMPORTANT SiLA 2 python requires python >= 3.6 !!!

:authors: mark doerr (mark@uni-greifswald.de)
          Florian Meinicke (florian.meinicke@cetoni.de)
          Timm Severin (timm.severin@tum.de)
          Robert Giessmann (robert.giessmann@tu-berlin.de)

:date: (creation)          20180610
:date: (last modification) 2019-08-29
________________________________________________________________________
"""

import sys
import os
import logging
from pathlib import Path

import subprocess

from distutils.util import strtobool

def query_yes_no(question, default_answer="yes", help=""):
    """Ask user at stdin a yes or no question

    :param question: question text to user
    :param default_answer: should be "yes" or "no"
    :param help: help text string
    :return:  :type: bool
    """
    if default_answer == "yes":
        prompt_txt = "{question} [Y/n] ".format(question=question)
    elif default_answer == "no":  # explicit no
        prompt_txt = "{question} [y/N] ".format(question=question)
    else:
        raise ValueError("default_answer must be 'yes' or 'no'!")

    while True:
        try:
            answer = input(prompt_txt)
            if answer:
                if answer == "?":
                    print(help)
                    continue
                else:
                    return strtobool(answer)
            else:
                return strtobool(default_answer)
        except ValueError:
            sys.stderr.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
        except KeyboardInterrupt:
            sys.stderr.write("Query interrupted by user, exiting now ...")
            exit(0)

def query(question, default_answer="", help=""):
    """Ask user a question

    :param question: question text to user
    :param default_answer: any default answering text string
    :param help:  help text string
    :return: stripped answer string
    """
    prompt_txt = "{question} [{default_answer}] ".format(question=question, default_answer=default_answer)

    while True:
        answer = input(prompt_txt).strip()

        if answer:
            if answer == "?":
                print(help)
                continue
            else:
                return answer
        else:
            return default_answer


def call(command=""):
    ''' Convenient command call: it splits the command string into tokens (default separator: space)

    :param command: the command to be executed by the system
    '''
    try:
        cmd_lst = command.split()

        print("cmd lst {}".format(cmd_lst))

        subprocess.run(cmd_lst, check=True)
    except subprocess.CalledProcessError as err:
        sys.stderr.write('CalledProcessERROR:{}'.format(err))

def safe_write(output_filename: str = "",
               output_str: str = ""):
    '''
      check, if file exists, before writing to file ...
      otherwise ask to overwrite ...
    '''
    if os.path.isfile(output_filename):
        question = f"File {output_filename} exists - shall I overwrite this file ?"
        if query_yes_no(question, default_answer="no", help="Type y/yes to overwrite the file...") :
            logging.info(f"overwriting {output_filename}")
            with open(output_filename, 'w') as output_file:
                output_file.write(output_str)
    else :
        with open(output_filename, 'w') as output_file:
            output_file.write(output_str)

def run(command="", parameters=[]):
    '''This version is closer to the subprocess version

    :param command: the command to be executed by the system
    :param parameters: parameters of the this command
    '''
    try:
        subprocess.run([command] + parameters, check=True, shell=True)
    except subprocess.CalledProcessError as err:
        sys.stderr.write('ERROR:', err)

def run_with_return(command="", parameters=[]):
    '''This version is closer to the subprocess version

    :param command: the command to be executed by the system
    :param parameters: parameters of the this command
    :return : result of the executed command
    '''
    try:
        # check=True, shell=True,
        return subprocess.run([command] + parameters,
                        stdout=subprocess.PIPE).stdout.decode('utf-8')
    except subprocess.CalledProcessError as err:
        sys.stderr.write('ERROR:', err)

def runSetup(src_dir="", lib_dir=""):
    """running a setup.py file within a pyhton script
       it requires a lot of things set...
       :param src_dir: directory containing the setup.py file
       :param lib_dir: directory containing the target lib directory
    """
    # all path settings seem to be required by run_setup and setup.py
    os.environ["PYTHONPATH"] = os.path.join(lib_dir, 'lib', 'python3.5', 'site-packages')
    sys.path.append(lib_dir)
    os.chdir(src_dir)
    setup_file = os.path.join(src_dir, 'setup.py')
    # this no longer works:
    #~ run_setup(setup_file,  script_args=['install', '--prefix', lib_dir ])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '.'])

def installAndImport(package):
    """ This imports a package and
        if not available, installs it first

        :return: The sucessfully imported package
    """
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        #~ pip.main(['install', package])
        print(f"Module {package} not installed! I'm going to install it now...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    finally:
        globals()[package] = importlib.import_module(package)
        return globals()[package]



if __name__ == '__main__':
    """Main: """
