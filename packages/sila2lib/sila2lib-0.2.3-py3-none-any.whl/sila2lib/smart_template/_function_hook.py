"""
Module for the FunctionHook storage object that is used to store references to functions
"""

# import meta packages
from typing import List, Callable


class FunctionHook:
    """Helper function to store function hooks of the template"""
    name: str = ""
    func: Callable = None
    args: List[Callable] = None

    def __init__(self, name: str, func: Callable, args: List[Callable] = None):
        """
        Class initialiser to allow construct the storage in one line
            This class' main use is to store function hooks and their corresponding function reference as well as the
            conversion operations used for the function arguments.

            :cvar name: The name of this function hook, as it is used to be replaced
            :cvar func: A reference to the function that is used when this hook is found
            :cvar args: A list of function references that are used to convert the arguments from string (as found in
                        the template string) to the type required when processing. If None, no argument conversion is
                        done and arguments get passed as string.
        """
        self.name = name
        self.func = func
        self.args = args
