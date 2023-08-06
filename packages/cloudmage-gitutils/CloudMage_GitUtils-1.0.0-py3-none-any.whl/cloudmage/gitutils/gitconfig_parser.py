##############################################################################
# CloudMage : Git Config Parser Class
#  ===========================================================================
# CloudMage Git Config Object Utility/Library
#   - Search a provided directory path location for a .git/config directory.
#   - If config found, extract the repository URL, and git provider and return
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 2/12/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Base Python Modules
from datetime import datetime
import inspect
import sys
import os


#####################
# Class Definition: #
#####################
class GitConfigParser(object):
    """ CloudMage Git Config Parser Class

    This class is designed to search a provided file path location for a
    .git/config directory/file. If found, the config file will be parsed,
    and an attempt to extract the repository URL, and the git provider will
    be made. If those properties are properly extracted, then the respective
    class properties are set, and the object is returned.
    """

    def __init__(self, path, verbose=False, log=None):
        """ GitConfigParser Class Constructor

        Parameters:
            path    (str):  required
            verbose (bool): optional [default=False]
            log     (obj):  optional [default=None]

        Attributes:
            _path        (str)  : private
            _verbose     (bool) : private
            _log         (obj)  : private
            _log_context (str)  : private
            _url         (str)  : private
            _provider    (str)  : private
            _user        (str)  : private

        Properties:
            verbose      (bool) : public
            url          (str)  : public
            provider     (str)  : public
            user:        (str)  : public

        Methods:
            _exception_handler
            log
        """

        # Class Private Attributes
        # Check to ensure that the provided path is valid
        if path and isinstance(path, str) and os.path.exists(path):
            self._path = path
        else:
            self._path = os.getcwd()

        # Check the passed verbose value to verify expected type.
        if verbose is not None and isinstance(verbose, bool):
            self._verbose = verbose
        else:
            self._verbose = False

        # Check to ensure that the passed log object is in fact an object,
        # and has the proper attributes, if not don't assign.
        if (
            log is not None and isinstance(log, object) and
            hasattr(log, 'debug') and hasattr(log, 'info') and
            hasattr(log, 'warning') and hasattr(log, 'error')
        ):
            self._log = log
        else:
            self._log = None
        self._log_context = "CLS->GitConfigParser"

        # Set initial values for class properties
        self._url = None
        self._provider = None
        self._user = None

        # Class Public Attributes
        self.url = self._path
        self.provider = None

        if self._url and self._url is not None:
            self.provider = self._url

    ############################################
    # Class Exception Handler:                 #
    ############################################
    def _exception_handler(self, caller_function, exception_object):
        """ Class Exception Handler

        Handle any exceptions that arise in a universal format
        for easy debuging purposes.

        Parameters:
            caller_function  (str):  required
            exception_object (obj):  required

        Returns:
            Publish properly formatted exceptions
            to log object or stdout, stderr
        """
        this_exception_msg = (
            "EXCEPTION occurred in: "
            f"{self._log_context}.{caller_function}, on line "
            f"{sys.exc_info()[2].tb_lineno}: -> {str(exception_object)}"
        )
        self.log(this_exception_msg, 'error', caller_function)

    ############################################
    # Class Logger:                            #
    ############################################
    def log(self, log_msg, log_type, log_id):
        """ Class Log Handler

        Provides the logging for this class. If the class caller instantiates
        the object with the verbose setting set to true, then the class will
        log to stdout/stderr or to a provided log object if one was passed
        during object instantiation.

        Parameters:
            log_msg  (str):  required
            log_type (str):  required
            log_id   (str):  required

        Returns:
            Log Stream
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        try:
            # Internal method variable assignments:
            this_log_msg_caller = f"{self._log_context}.{log_id}"

            # Set the log message offset based on the message type:
            # [debug=3, info=4, warning=1, error=3]
            this_log_msg_offset = 3
            if log_type.lower() == 'info':
                this_log_msg_offset = 4
            elif log_type.lower() == 'warning':
                this_log_msg_offset = 1

            # If a valid log object was passed into the class constructor,
            # publish the log to the log object:
            if self._log is not None:
                # Set the log message prefix
                this_log_message = f"{this_log_msg_caller}: -> {log_msg}"
                if log_type.lower() == 'error':
                    self._log.error(this_log_message)
                elif log_type.lower() == 'warning':
                    self._log.warning(this_log_message)
                elif log_type.lower() == 'info':
                    self._log.info(this_log_message)
                else:
                    self._log.debug(this_log_message)
            # If no valid log object was passed into the class constructor,
            # write the message to stdout, stderr:
            else:
                this_log_message = "{}    {}{}{}: -> {}".format(
                    datetime.now(),
                    log_type.upper(),
                    " " * this_log_msg_offset,
                    this_log_msg_caller,
                    log_msg
                )
                if log_type.lower() == 'error':
                    print(this_log_message, file=sys.stderr)
                else:
                    if self._verbose:
                        print(this_log_message, file=sys.stdout)
        except Exception as e:
            self._exception_handler(__id, e)

    ################################################
    # Verbose Setter / Getter Methods:             #
    ################################################
    @property
    def verbose(self):
        """ Verbose Property Getter

        Getter method for the verbose property.
        This method will return the verbose setting.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """ Verbose Property Setter

        Setter method for the verbose property.
        This method will set the verbose setting if a valid
        bool value is provided.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # Check the value of verbose, and set accordingly
        if verbose is not None and isinstance(verbose, bool):
            self._verbose = verbose
            self.log(
                f"Updated {__id} property with value: {self._verbose}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type bool "
                f"but received type: {type(verbose)}",
                'error',
                __id
            )

    ################################################
    # Search Directory Path and Search for Git URL #
    ################################################
    @property
    def url(self):
        """ URL Property Getter Method

        This property will return the repository URL if a value was set by
        the property setter method.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)

        if self._url is not None:
            self.log(f"Return: {self._url}", 'debug', __id)
            return self._url
        else:
            self.log(
                f"Return: {__id} has no value assigned!",
                'warning',
                __id
            )
            return f"{__id} property has no value assigned!"

    @url.setter
    def url(self, config_path):
        """ URL Property Setter Method

        This property setter method will search the provided path and attempt
        to locate and extact the git repository URL if a .git/config file is
        found in the path location.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # Ensure that a valid config_path value was passed.
        if config_path is not None and isinstance(config_path, str):
            # Search for a .git directory in the provided search path, and if
            # found parse to get the repository URL.
            git_config_path = os.path.join(config_path, '.git/config')
            self.log(
                f"Searching for git config in path: {git_config_path}",
                'debug',
                __id
            )

            # If the provided path exists, then attempt to extract the url
            # from the .git/config file.
            if os.path.exists(git_config_path) and os.access(
                git_config_path,
                os.R_OK
            ):
                self.log(
                    ".git/config found! Searching for repository url...",
                    'debug',
                    __id
                )

                with open(git_config_path) as f:
                    for count, file_line in enumerate(f):
                        # For each line in the config, if url is found in the
                        # line, then attempt to parse it.
                        line = file_line.strip()
                        if line and 'url' in line:
                            self.log(
                                f"URL string match found in .git/config -> "
                                f"line: {line}",
                                'debug',
                                __id
                            )
                            k, v = line.partition("=")[::2]
                            git_config_url = v.strip()
                            self.log(
                                f"Parsing URL string match: {git_config_url}",
                                'debug',
                                __id
                            )
                            # If the found URL string starts and ends with
                            # proper criteria, assign the value and break.
                            if git_config_url.startswith((
                                'http',
                                'https',
                                'git',
                                'ssh')
                            ) and git_config_url.endswith('.git'):
                                self._url = git_config_url
                                self.log(
                                    "URL string match verified... "
                                    "Updating url property with value: "
                                    f"{self._url}",
                                    'info',
                                    __id
                                )
                                break
                            else:
                                self.log(
                                    "URL match failed format verification on "
                                    "matched string: {git_config_url}",
                                    'warning',
                                    __id
                                )
                                continue
                        else:
                            self.log(
                                f"URL' match not found in line: {line}",
                                'debug',
                                __id
                            )
            else:
                self.log(
                    "Provided directory path doesn't exist. Aborting update!",
                    'error',
                    __id
                )
        else:
            self.log(
                f"{__id} path argument expected string but received "
                f"type: {type(config_path)}",
                'error',
                __id
            )

    ################################################
    # Search URL String for Git Provider:          #
    ################################################
    @property
    def provider(self):
        """ Provider Property Getter method.

        This property method will return the repository platform provider
        provided that a proper value can be determined and/or was set by
        properly by the property setter method.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)

        if self._provider is not None:
            self.log(f"Return: {self._provider}", 'debug', __id)
            return self._provider
        else:
            self.log(
                f"Return: {__id} property has no value assigned!",
                'warning',
                __id
            )
            return f"{__id} property has no value assigned!"

    @provider.setter
    def provider(self, repository_url):
        """ Provider Property Setter method.

        Setter method for the object provider property. This property will
        search the provided URL and attempt to extact the a git repository
        provider, such as github, gitlab, or bitbucket.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        if repository_url is not None and isinstance(repository_url, str):
            self.log(
                f"Searching for git provider in URL: {repository_url}",
                'debug',
                __id
            )
            # Parse the provided repository url and attempt to
            # extract the provider.
            if repository_url.startswith((
                'http',
                'https',
                'git',
                'ssh'
            )) and repository_url.endswith('.git'):
                provider_git_url = repository_url.strip().split("/")
                self.log(
                    "URL format validated, splitting into search list: "
                    f"{provider_git_url}",
                    'debug',
                    __id
                )
                if len(provider_git_url) == 2:
                    provider_string = provider_git_url[-2].split(
                        ":"
                    )[0].split("@")[1]
                elif len(provider_git_url) > 3:
                    provider_string = provider_git_url[-3]
                else:
                    provider_string = None

                # Validate the provider string is an expected value if parsed.
                if provider_string is not None and (
                    'github' in provider_string or
                    'gitlab' in provider_string or
                    'bitbucket' in provider_string
                ):
                    # If a user@provider.tld is set, then parse the user
                    # designation and set the class user attribute.
                    if '@' in provider_string:
                        self._user = provider_string.split('@')[0]
                        self.log(
                            "User detected in provider string, "
                            f"updating user attribute: {self._user}",
                            'debug',
                            __id
                        )
                        provider_string = provider_string.split('@')[1]
                    else:
                        self.log(
                            f"No User detected in provider string",
                            'debug',
                            __id
                        )
                    # Now the provider string should be the target provider,
                    # set the internal class attribute.
                    self._provider = provider_string
                    self.log(
                        f"Provider match {self._provider} found!",
                        'debug',
                        __id
                    )
                else:
                    self.log(
                        f"Parsed provider value: {provider_string} not found "
                        "or invalid. Aborting provider search!",
                        'error',
                        __id
                    )
            else:
                self.log(
                    f"URL {repository_url} not properly formatted, "
                    "aborting provider search...",
                    'error',
                    __id
                )
        else:
            self.log(
                f"{__id} repository url argument expected string but "
                "received type: {type(repository_url)}",
                'error',
                __id
            )

    ################################################
    # Search URL String for User:                  #
    ################################################
    @property
    def user(self):
        """ Git URL User Property Getter method.

        This property method will return the repository url user
        provided within the git provider URL if present.
        This value is set within the provider setter.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)

        if self._user is not None:
            self.log(f"Return: {self._user}", 'debug', __id)
            return self._user
        else:
            self.log(
                f"Return: {__id} has no value assigned!",
                'warning',
                __id
            )
            return f"{__id} property has no value assigned!"
