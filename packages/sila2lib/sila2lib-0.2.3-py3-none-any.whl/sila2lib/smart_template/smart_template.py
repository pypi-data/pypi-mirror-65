"""
Main module that implements the SmartTemplate class
"""

# import general packages for this class
import re as _re
from collections import ChainMap as _ChainMap
import warnings

# import from this package
from .exceptions import KeyExistsError, TypeWarning
from ._function_hook import FunctionHook

# meta packages
import logging
from logging import Logger
from typing import ChainMap
from typing import Match, Pattern
from typing import Callable, List, Any, Dict


class SmartTemplate:
    """
    Smart Template class
        This template class allows to substitute template variables marked by a $ character with code-defined strings.
        it furthermore allows to define hooks, which can perform modifications of the template variables.
        For details on the usage see the corresponding
        :download:`README.md <https://gitlab.com/tseverin/smart_template/blob/master/README.md>` file.

        :cvar pattern_str: The pattern string that is used to match template variables in the given template. It will
                           be compiled be :func:`re.compile`. Some elements will be replaced automatically by the
                           constructor of this class:

                            * **%(delimiter)s**   contains the delimiter used (see: delimiter)
                            * **%(id)s**          the pattern to find template variables (see pattern_id)
                            * **%(bid)s**         the pattern used inside braced template variables
                                                  (see pattern_braced_id)
                            * **%(fid)s**         the pattern to find hooks and their corresponding variable

        :cvar delimiter: The delimiter used in the template replacement. Defaults to ``$``.
        :cvar pattern_id: The pattern used to find inline, non-braced template variables.
        :cvar pattern_brace_id: The pattern used to find braced template variables, without the braces.
        :cvar pattern_function_id: The pattern used to find template variables with hooks. It further is re-used to
                                   extract the hook's name and its arguments.
        :cvar re_flags: The flags that are applied during compilation of all regular expressions used.
    """

    # Type hinting for variables which are not set on default
    template: str
    hooks: Dict[str, FunctionHook]
    mapping: ChainMap[str, Any]
    logger: Logger
    pattern: Pattern

    # pattern
    pattern_str = r"""
    %(delimiter)s(?:
      (?P<escaped>%(delimiter)s)            |   # Escape sequence of two delimiters
      (?P<named>%(id)s)                     |   # delimiter and a Python identifier
      {(?P<braced>%(bid)s)}                 |   # delimiter and a braced identifier
      {(?P<hooked>(?:%(fid)s:)+%(bid)s)}    |   # match function definitions
      (?P<invalid>)                             # Other ill-formed delimiter expressions
    )
    """

    # pattern replacement variables
    delimiter = '$'
    pattern_id = r'(?:[_a-z][_a-z0-9]*)'
    pattern_brace_id = None
    pattern_function_id = r"""
        (?P<hook>[_a-z][_a-z0-9]*)              # name of the function hook
        (?:\(                                   # start list of arguments
            (?P<arguments>[^\)]+)               # allow  anything that is not a closing bracket
        \))?                           
    """

    # regular expression compilation flags
    re_flags = _re.IGNORECASE | _re.ASCII

    def __init__(self, template: str, logging_level: int = logging.CRITICAL):
        """
        Class initialiser

            :param template: The template string in which the replacements are to be made
            :param logging_level: If a logger has been initialised, here a logging level for a module-internal logger
                                  can be set
        """

        # create a local logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

        # pre-compile the general search pattern
        self.pattern_str = self.pattern_str % {
            'delimiter':    _re.escape(self.delimiter),
            'id':           self.pattern_id,
            'bid':          self.pattern_brace_id or self.pattern_id,
            'fid':          self.pattern_function_id
        }
        self.pattern = _re.compile(self.pattern_str, self.re_flags | _re.VERBOSE)

        # pre-compile the search pattern for hooks
        self.hook_pattern = _re.compile(self.pattern_function_id, self.re_flags | _re.VERBOSE)

        self.mapping = _ChainMap({})
        self.hooks = {}

        self.template = template

    def _invalid(self, matched_element: Match):
        """
        Raises an error with information on the line/column when an invalid identifier has been found

            :param matched_element: An (invalid) match found by the regular expression which position is extracted

            :raises: ValueError: Always. That's why this function exists in the first place.
        """
        i = matched_element.start('invalid')
        lines = self.template[:i].splitlines(keepends=True)
        if not lines:
            column_number = 1
            line_number = 1
        else:
            column_number = i - len(''.join(lines[:-1]))
            line_number = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' %
                         (line_number, column_number))

    def add_function_hook(self, name: str, func: Callable, args: List[Callable] = None, overwrite: bool = False):
        """
        Add a hook to a function

            :param name: Name under which the hook is stored and accessed in the template file
            :param func: The function that is executed when the hooked is found in the template
            :param args: The type of arguments the function expects
            :param overwrite: Allow overwriting already existing hooks

            :raises KeyExistsError: If overwrite is set to `False` and the name of the hook has already been registered,
                                    this error will be raised.
        """

        # check if the key exists or if we allow to overwrite it
        if not overwrite and name in self.hooks:
            raise KeyExistsError

        #  add the hook to the local dictionary of hooks
        self.hooks[name] = FunctionHook(name=name, func=func, args=args)

    def remove_function_hook(self, name: str):
        """
        Remove a hook from the list of registered hooks

            :param name: name of the hook to delete
        """

        del self.hooks[name]

    def substitute(self, mapping: Dict[str, Any] = None, **kwargs) -> str:
        """
        Performs the actual substitution process
            This method substitutes all template variables in the template string defined at object creation with the
            data passed in the function call

            :param mapping: A dictionary whose keys are used as names of the template variables and the corresponding
                            item as replacement text. The item will automatically converted into a string
            :param kwargs: Any number of keyword/value pairs, where the keyword corresponds to the template variables
                           name. The value will automatically converted into a string and used as replacement.

            :returns: The substituted template text
        """
        if mapping is None:
            self.mapping = _ChainMap(kwargs)
        else:
            self.mapping = _ChainMap(kwargs, mapping)

        return self.pattern.sub(self._convert, self.template)

    def _convert(self, matched_element: Match) -> str:
        """
        This method actually performs the conversion of found named, braced or hooked groups.
            It is called by the pattern.sub method for each match found. The match is then evaluated and replaced with
            the corresponding element.

            :param matched_element: A regular expression match object that contains the current match.

            :returns: The replacement text for the match found.

            :raises ValueError: If some unrecognised named group is found. This can usually only happen, if the pattern
                                has been modified.
        """
        # extract direct variables matches
        named = matched_element.group('named') or matched_element.group('braced')
        if named is not None:
            return str(self.mapping[named])

        # function hooks require more complex evaluation
        if matched_element.group('hooked') is not None:
            (hooks, _, named) = matched_element.group('hooked').rpartition(':')
            self.logger.info('Found hook(s) "{hook}" for template variable {name}'.format(hook=hooks, name=named))
            return str(self._evaluate_hook(hooks, self.mapping[named]))

        # evaluate remaining.
        if matched_element.group('escaped') is not None:
            return self.delimiter
        if matched_element.group('invalid') is not None:
            self._invalid(matched_element)

        # we do not have to take car of the group 'hook' and 'arguments', those should have disappeared with 'hooked'
        #   so any remaining element must be some kind of weird error
        raise ValueError('Unrecognized named group in pattern', self.pattern)

    def _evaluate_hook(self, hooks: str, value: Any) -> str:
        """
        Evaluates the code when a hook is found
            This method takes care of recursively evaluating the hooks found with a template variable.

            :param hooks: The list of hooks found (as string). This can e.g. be 'indent:upper'
            :param value: The current value. Since this function works recursively, each recursion updates this values.

            :returns: The replacement text after all hooks have been applied.
        """

        # once we managed to run all hooks, just return the value
        if not hooks:
            return value

        # extract and remove the current hook
        current_hooks = hooks.split(':')
        current_hook = current_hooks.pop()

        # check if the hook contains function arguments
        matched_element = self.hook_pattern.search(current_hook)

        # this one must exist, it defines the function to call for the hook
        current_hook = matched_element.group('hook')

        # we *might* also have arguments, depending on this we want to generate the list of function arguments
        if matched_element.group('arguments') is not None:
            function_args_str = matched_element.group('arguments').split(',')

            # check if we have callables that allow to convert the function arguments
            if self.hooks[current_hook].args is None:
                function_args = function_args_str
            else:
                if len(function_args_str) > len(self.hooks[current_hook].args):
                    warnings.warn(
                        (
                            'Found more arguments in template than specified for hook "{hook}". '
                            'All additional arguments will be discarded.' '\n'
                            '\t' 'Allowed is: {hook}({hook_arguments_allowed})' '\n'
                            '\t' 'Found:      {hook}({hook_arguments_found})' '\n'
                        ).format(
                            hook=current_hook,
                            hook_arguments_allowed=', '.join([arg.__name__ for arg in self.hooks[current_hook].args]),
                            hook_arguments_found=', '.join(function_args_str)
                        ),
                        TypeWarning
                    )
                function_args = [func(arg) for (arg, func) in zip(function_args_str, self.hooks[current_hook].args)]
        else:
            function_args = []

        before_value = value
        value = self.hooks[current_hook].func(str(value), *function_args)
        self.logger.debug(
            (
                'Applying hook "{hook}" '
                'on the value "{old_value}" '
                'resulted in the new value "{new_value}"'
            ).format(
                hook=current_hook,
                old_value=before_value,
                new_value=value
            )
        )
        return self._evaluate_hook(':'.join(current_hooks), value)
