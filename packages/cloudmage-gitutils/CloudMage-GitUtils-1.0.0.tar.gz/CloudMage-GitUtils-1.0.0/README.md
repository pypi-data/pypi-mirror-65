# CloudMage GitUtils Python3 Utility and Reporting Package

<br/>

![CloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/banners/cloudmage-nebula-glow.png)

<br/>

![PyTests](https://github.com/CloudMages/PyPkgs-GitUtils/workflows/PyTests/badge.svg)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Coverage](https://github.com/CloudMages/PyPkgs-GitUtils/workflows/Coverage/badge.svg)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![codecov](https://codecov.io/gh/CloudMages/PyPkgs-GitUtils/branch/master/graph/badge.svg)](https://codecov.io/gh/CloudMages/PyPkgs-GitUtils)

<br/><br/>

## Table of Contents

* [Description](#description)
* [Road Map](#road-map)
* [Python Version Support](#python-version-support)
* [Package Installation](#package-installation)
* [Package Dependencies](#package-dependencies)
* [GitConfigParser Class](#gitconfigparser-class)
  * [GitConfigParser Constructor Arguments](#gitconfigparser-constructor-arguments)
  * [GitConfigParser Attributes and Properties](#gitconfigparser-attributes-and-properties)
  * [GitConfigParser Available Methods](#gitconfigparser-available-methods)
  * [GitConfigParser Class Usage](#gitconfigparser-class-usage)
* [GithubReports Class](#githubreports-class)
  * [GithubReports Constructor Arguments](#githubreports-constructor-arguments)
  * [GithubReports Attributes and Properties](#githubreports-attributes-and-properties)
  * [GithubReports Available Methods](#githubreports-available-methods)
  * [GithubReports Class Usage](#githubreports-class-usage)
* [ChangeLog](#changelog)
* [Contacts and Contributions](#contacts-and-contributions)

<br/><br/>

## Description

In part, the purpose of this library is to be able to either automatically detect a projects configured Git repository by searching for and parsing a .git/config file in a given file path, or to take an input consisting simply of the repositories URL (HTTP | Git formatted). The object has the repository url, provider, and any users configured within the git URL string. The Second part of this utility package is to provide a few pre-packaged reports that can be retrieved from Github such as an Open Pull Request report, showing all pull requests opened within a given repository user or organization namespace.

<br/><br/>

## Road Map

Currently this library gathers data from the Githubs API, however, future development will include Gitlab and Bitbucket repository API reporting as well.

<br/><br/>

## Python Version Support

This library is compatible with Python 3.6 and higher. It may work with earlier versions of Python3 but was not tested against anything earlier then 3.6. As Python 2.x is soon to be end of life, backward compatibility was not taken into consideration.

<br/><br/>

## Package Installation

This library has been published to [PyPi](https://pypi.org/project/cloudmage-gitutils/) and can be installed via normal python package manager conventions such as [pip](https://pip.pypa.io/en/stable/) or [poetry](https://pypi.org/project/poetry/).

<br/>

```python
pip3 install cloudmage-gitutils
```

<br/><br/>

## Package Dependencies

This package installs and imports the following python modules during installation:

* pyGithub
* progress
* cloudmage.jinjautils

<br/>

Additionally the package takes advantage of the following built in python modules:

* os
* sys
* json
* inspect
* datetime

<br/><br/>

## GitConfigParser Class

This class takes a directory path argument, which it uses as a target directory to search for a .git/config file. If a file is found, then the class will parse the URL from the config, and determines the git platform provider from the parsed URL path. This data is then used to return back an object instance with properties set to the parsed values.

<br/>

### GitConfigParser Constructor Arguments

-----

The following arguments can be used to instantiate a new object instance:

<br/>

| __[path]('')__ |  *A valid directory path where a `.git/config` file can be found. <br/> Must be valid directory path, checked with `os.path.exists()`* |
|:---------------|:-------------------------------------------------------|
| *required*     | [true]('')                                             |
| *type*         | [str](https://docs.python.org/3/library/stdtypes.html) |

<br/>

| __[verbose]('')__ |  *Enables verbose mode. &nbsp; [[true]('')=enable &nbsp; [false]('')=disable]* |
|:------------------|:--------------------------------------------------------|
| *required*        | [false]('')                                             |
| *type*            | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *default*         | [false]('') *(disabled)*                                |

<br/>

| __[log]('')__ |  *Redirects object standard log messaging to provided log object.* |
|:--------------|:-----------------------------------------------------------|
| *required*    | [false]('')                                                |
| *type*        | [obj](https://docs.python.org/3/library/stdtypes.html)     |
| *default*     | [None]('') *(log to stdout, stderr if verbose=[true](''))* |

<br/><br/>

### GitConfigParser Attributes and Properties

-----

The following attributes/properties are available to an instantiated object instance. Any of the attributes or properties can be accessed with standard object dot notation as in the example: `verbose_mode = GitConfigParserObj.verbose`

<br/>

| __[verbose]('')__ |  *Verbose setting that controls logging level within the object. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:--------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*  |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *instantiated value* | [false](false)                                          |

<br/>

| __[url]('')__ |  *Verbose setting that controls logging level within the object. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:---------------------------------------------------------------------------------------------|
| *returns*            | *url string* [->](->) `https://github.com/namespace/repository`                              |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                                       |
| *instantiated value* | *URL string parsed from .git/config in directory path specified during object instantiation* |

<br/>

| __[provider]('')__   |  *The parsed provider (*github.com*, *gitlab.com*, or *bitbucket.org*) from a given URL string* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Provider string [->](->) `github.com`                                          |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Provider string parsed from object url property during object instantiation*  |

<br/>

| __[user]('')__       |  *If a user was used in the config url, then the value of the user will be assigned to this property* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | User string [->](->) `username`                                                |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *User string parsed from object url property during object instantiation*      |

<br/>

| __[log]('')__        |  *The class logger. Will either write directly to stdout, stderr, or to a lob object if passed into the object constructor during object instantiation* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Log Event Stream                                                               |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Logs written to stdout, stderr*                                               |

<br/><br/>

### GitConfigParser Available Methods

-----

The following methods are available to an instantiated object instance. Some of the methods are simply setter methods that run the logic required to discover and then set one of the above instance properties.

<br/>

__[verbose]('')__

Setter method for `verbose` property that enables or disables verbose mode

<br/>

| parameter   | type       | required     | arg info                                                   |
|:-----------:|:----------:|:------------:|:-----------------------------------------------------------|
| verbose | [bool]('')  | [true](true) | *[True]('') enables verbose logging, [False]('') disables it* |

<br/>

__Examples:__

```python
# Getter method
verbose_setting = GitConfigParserObj.verbose

# Setter method
GitConfigParserObj.verbose = True
```

<br/><br/>

__[log]('')__

Method to enable logging throughout the class. Log messages are sent to the log method providing the log message, the message type being one of `[debug, info, warning, error]`, and finally the function or method id that is automatically derived within the function or method using the python inspect module. If a log object such as a logger or an already instantiated log object instance was passed to the class constructor during the objects instantiation, then all logs will be written to the provided log object. If no log object was provided during instantiation then all `debug`, `info`, and `warning` logs will be written to stdout, while any encountered `error` log entries will be written to stderr. Note that debug or verbose mode needs to be enabled to receive the event log stream.

<br/>

| arg      | type       | required     | arg info                                          |
|:--------:|:----------:|:------------:|:--------------------------------------------------|
| log_msg  | [str]('')  | [true](true) | *The actual message being sent to the log method* |
| log_type | [str]('')  | [true](true) | *The type of message that is being sent to the log method, one of `[debug, info, warning, error]`*    |
| log_id   | [str]('')  | [true](true) | *A string value identifying the sender method or function, consisting of the method or function name* |

<br/>

__Examples:__

```python
def my_function():
  __function_id = inspect.stack()[0][3]
  GitConfigParserObj.log(
    f"{__function_id} called.",
    'info',
    __function_id
  )
```

<br/><br/>

__[url]('')__

Setter method for `url` property that will search the object instances set directory path and look for a .git/config directory in that path. If found, then the setter method will parse the .git/config file and look for a URL line to parse and extract the URL. It will then update the object property with the parsed value. If this method is called post instantiation, then a valid directory path must be provided as an argument.

<br/>

| parameter   | type       | required     | arg info                                          |
|:-----------:|:----------:|:------------:|:--------------------------------------------------|
| config_path | [str]('')  | [true](true) | *Must be a valid directory path. This value is checked by `os.path.exists()` and will write an error to the log if the provided argument directory path does not exist* |

<br/>

__Examples:__

```python
GitConfigParserObj.url = /home/projects/my_project_directory
```

<br/><br/>

__[provider]('')__

Setter method for `provider` property that will search the object instances updated url property for a valid git provider string. Currently the provider setter will look specifically for a value that matches one of `[github.com, gitlab.com, bitbucket.org]`. If this method is called post instantiation, then a valid git repository url must be provided as an argument. The provider property setter will parse either an http, https, git or ssh formatted URL string. During the parse operation, if a user is identified in the provider string such as user@bitbucket.org, then the username will also be parsed and used to update the `user` object property.

<br/>

| parameter      | type       | required     | arg info                                          |
|:--------------:|:----------:|:------------:|:--------------------------------------------------|
| repository_url | [str]('')  | [true](true) | *Must be a properly formatted URL string starting with one of `[http, https, git, ssh]` and must end in `.git`* |

<br/>

__Examples:__

```python
GitConfigParserObj.provider = "git@github.com:namespace/repository.git"
```

<br/><br/>

### GitConfigParser Class Usage

-----

<br/>

#### GitConfigParser Default Instantiation

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None
```

<br/><br/>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br/> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br/><br/>

#### GitConfigParser Verbose Instantiation

```python
from cloudmage-gitutils import GitConfigParser

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br/><br/>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br/> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels [`log.debug()`, `log.info()`, `log.warning()`, `log.error()`] and printed to the passed respective logger object method.

<br/><br/>

#### GitConfigParser Log Instantiation

```python
from cloudmage-gitutils import GitConfigParser

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

ProjectPath = '/Projects/MyCoolProject'
# Contains .git/config with
# url = https://github.com/GithubNamespace/MyCoolProject-Repo.git

Repo = GitConfigParser(ProjectPath, verbose=True, log=GitLog)

repo_url = Repo.url
print(repo_url) # https://github.com/GithubNamespace/MyCoolProject-Repo

repo_provider = Repo.provider
print(repo_provider) # github.com

repo_user = Repo.user
print(repo_user) # None

for items in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br/><br/>

## GithubReports Class

This class will take an auth_token, and user/organization namespace name and run a query against the namespace for all open pull requests in any repositories living within that user/org namespace. Once the pull request data is returned, it can be then be used to generate the included HTML template report that will list the repository, pull request title, submitter, reviewers, creation date and days open count for each found repository.

<br/>

### GithubReports Constructor Arguments

-----

The following arguments can be used to instantiate a new object instance:

<br/>

| __[verbose]('')__ |  *Enables verbose mode. &nbsp; [[true]('')=enable &nbsp; [false]('')=disable]* |
|:------------------|:--------------------------------------------------------|
| *required*        | [false]('')                                             |
| *type*            | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *default*         | [false]('') *(disabled)*                                |

<br/>

| __[auth_token]('')__ |  *A valid Github personal access token used to search issues within the user/organization namespace account.* |
|:---------------|:-------------------------------------------------------|
| *required*     | [true]('')                                             |
| *type*         | [str](https://docs.python.org/3/library/stdtypes.html) |

<br\>

| __[log]('')__ |  *Redirects object standard log messaging to provided log object.* |
|:--------------|:-----------------------------------------------------------|
| *required*    | [false]('')                                                |
| *type*        | [obj](https://docs.python.org/3/library/stdtypes.html)     |
| *default*     | [None]('') *(log to stdout, stderr if verbose=[true](''))* |

<br/><br/>

### GithubReports Attributes and Properties

-----

The following attributes/properties are available to an instantiated object instance. Any of the attributes or properties can be accessed with standard object dot notation as in the example: `verbose_mode = GithubReportsObj.verbose`

<br/>

| __[verbose]('')__ |  *Verbose setting that controls logging level within the object. &nbsp; [[true]('')=enabled, [false]('')=disabled]* |
|:---------------------|:--------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(enabled or disabled)*  |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html) |
| *instantiated value* | [false](false)                                          |

<br/>

| __[auth_token]('')__ |  *Property to set/re-set the Github Authentication Token required to make calls against Github APIs.* |
|:---------------------|:------------------------------------------------------------------------------------------------------|
| *returns*            | *string* [->](->) `0123456789109876543210`                                                            |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                                                |
| *instantiated value* | *Provided Token, If token not provided during object construction, use Obj.auth_token = "<Token>"*    |

<br/>

| __[repo_namespace]('')__ |  *The user / organization namespace that will be used as the search target*       |
|:-------------------------|:----------------------------------------------------------------------------------|
| *returns*                | string [->](->) `CloudMages`                                                      |
| *type*                   | [str](https://docs.python.org/3/library/stdtypes.html)                            |
| *instantiated value*     | *None, set with Obj.repo_namespace = "<CloudMages>"*                              |

<br/>

| __[is_organization]('')__  |  *Flag to indicate if the provided namespace is an organization namespace (affects API calls).  &nbsp; [[true]('')=organization, [false]('')=user]* |
|:---------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|
| *returns*                  | [true](true) or [false](false) *(organization or user) namespace*                                                                                   |
| *type*                     | [bool](https://docs.python.org/3/library/stdtypes.html)                                                                                             |
| *instantiated value*       | [false](false)                                                                                                                                      |

<br/>

| __[notify]('')__     |  *Flag to specify if, when running reports, a comment should be left on a repository that has exceeded the open days threshold. &nbsp; [[true]('')=leave_comment, [false]('')=do_not_comment]* |
|:---------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *returns*            | [true](true) or [false](false) *(leave comments or do not leave comments)                                                                                                                      |
| *type*               | [bool](https://docs.python.org/3/library/stdtypes.html)                                                                                                                                        |
| *instantiated value* | [false](false)                                                                                                                                                                                 |

<br/>

| __[open_pr_threshold]('')__   |  *Number value indicating a days threshold used for reports such as open pull requests. This value will be used to determine if a PR has exceeded desired days open.* |
|:------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *returns*                     | int [->](->) 5                                                                                                                                                         |
| *type*                        | [int](https://docs.python.org/3/library/stdtypes.html)                                                                                                                 |
| *instantiated value*          | [5](5) days                                                                                                                                                            |

<br/>

| __[template_path]('')__       |  *String value of the path where reporting templates are stored.* |
|:------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *returns*                     | str [->](->) /Path/to/template/files                                                                                                                                   |
| *type*                        | [str](https://docs.python.org/3/library/stdtypes.html)                                                                                                                 |
| *instantiated value*          | /{installation/path}/templates                                                                                                                                         |

<br/>

| __[log]('')__        |  *The class logger. Will either write directly to stdout, stderr, or to a lob object if passed into the object constructor during object instantiation* |
|:---------------------|:-------------------------------------------------------------------------------|
| *returns*            | Log Event Stream                                                               |
| *type*               | [str](https://docs.python.org/3/library/stdtypes.html)                         |
| *instantiated value* | *Logs written to stdout, stderr*                                               |

<br/><br/>

### GithubReports Available Methods

-----

The following methods are available to an instantiated object instance. Some of the methods are simply setter methods that run the logic required to discover and then set one of the above instance properties.

<br/>

__[verbose]('')__

Setter method for `verbose` property that enables or disables verbose mode

<br/>

| parameter   | type       | required     | arg info                                                   |
|:-----------:|:----------:|:------------:|:-----------------------------------------------------------|
| verbose     | [bool]('') | [true](true) | *[True]('') enables verbose logging, [False]('') disables it* |

<br/>

__Examples:__

```python
# Getter method
verbose_setting = GitHubReportObj.verbose

# Setter method
GitHubReportObj.verbose = True
```

<br/><br/>

__[log]('')__

Method to enable logging throughout the class. Log messages are sent to the log method providing the log message, the message type being one of `[debug, info, warning, error]`, and finally the function or method id that is automatically derived within the function or method using the python inspect module. If a log object such as a logger or an already instantiated log object instance was passed to the class constructor during the objects instantiation, then all logs will be written to the provided log object. If no log object was provided during instantiation then all `debug`, `info`, and `warning` logs will be written to stdout, while any encountered `error` log entries will be written to stderr. Note that debug or verbose mode needs to be enabled to receive the event log stream.

<br/>

| arg      | type       | required     | arg info                                          |
|:--------:|:----------:|:------------:|:--------------------------------------------------|
| log_msg  | [str]('')  | [true](true) | *The actual message being sent to the log method* |
| log_type | [str]('')  | [true](true) | *The type of message that is being sent to the log method, one of `[debug, info, warning, error]`*    |
| log_id   | [str]('')  | [true](true) | *A string value identifying the sender method or function, consisting of the method or function name* |

<br/>

__Examples:__

```python
def my_function():
  __function_id = inspect.stack()[0][3]
  GitConfigParserObj.log(
    f"{__function_id} called.",
    'info',
    __function_id
  )
```

<br/><br/>

__[auth_token]('')__

Setter method for `auth_token` property that will be used to make calls to Githubs API for authentication. The provided auth_token must be valid, and have access to read repositories and issues. An auth_token can be set during instance instantiation, using the property setter, or passed directly into a reporting method. This allows the versatility of using different tokens if necessary.

<br/>

| parameter   | type       | required     | arg info                                          |
|:-----------:|:----------:|:------------:|:--------------------------------------------------|
| auth_token  | [str]('')  | [true](true) | *Must be a valid Github auth token. The search methods will throw a BadCredentials exception if an invalid token is provided.* |

<br/>

__Examples:__

```python
# Getter method
set_auth_token = GitHubReportObj.auth_token


# Setter method
GitHubReportObj = GitHubReports(auth_token="0123456789109876543210")

# Set using property setter
GitHubReportObj.auth_token = "0123456789109876543210"

export TOKEN="0123456789109876543210"
GitHubReportObj.search_open_pulls(auth_token=$TOKEN)
```

<br/><br/>

__[repo_namespace]('')__

Setter method for `repo_namespace` property that will be used to specify what repository namespace will be targeted for reporting. The repository namespace must be a string value, and a valid Github user or organization namespace. The `repo_namespace` can be set by the property setter method, or by being passed directly into the search method as a method argument.

<br/>

| parameter        | type       | required     | arg info                                          |
|:----------------:|:----------:|:------------:|:--------------------------------------------------|
| repo_namespace   | [str]('')  | [true](true) | *Must be a valid Github user or organization namespace or reporting and/or any form of desired data collection will fail.* |

<br/>

__Examples:__

```python
# Getter method
namespace = GitHubReportObj.repo_namespace


# Setter method
GitHubReportObj = GitHubReports(auth_token="0123456789109876543210")

# Set using property setter
GitHubReportObj.repo_namespace = "CloudMages"

# Set within the reporting method call
export TOKEN="0123456789109876543210"
GitHubReportObj.search_open_pulls(
  auth_token=$TOKEN
  repo_namespace="CloudMages"
)
```

<br/><br/>

__[is_organization]('')__

Setter method for `is_organization` property that will be used as a flag to determine if the provided repo_namespace is a user namespace or organization namespace. This information is relevant as the APIs that will be called to fetch data for or about the specified repository as such with repository or issues searchs will be affected by this flag. If an organization namespace is passed, but not signaled that the namespace is an organization, reports or other calls to the API could fail.

> Default value of this flag is set to [false](false).

<br/>

| parameter        | type       | required       | arg info                                                             |
|:----------------:|:----------:|:--------------:|:---------------------------------------------------------------------|
| is_organization  | [bool]('') | [false](false) | *[True]('') signals organization, [False]('') signals user namepace* |

<br/>

__Examples:__

```python
# Getter method
OrgFlag = GitHubReportObj.is_organization


# Setter method
GitHubReportObj.repo_namespace = "CloudMages"
GitHubReportObj.is_organization = True
SearchIssues = GitHubReportObj.search_open_pulls()
```

<br/>

__[notify]('')__

Setter method for `notify` property that will be used as a flag to publish a @mentioned comment on any open pull requests or issues that were found within the searched namespace if the open pull request or issue has been opened for a period of time exceeding the value set in `open_pr_threshold`. If an open pull request or issue is discovered, and Obj.notify is set to [True](''), then a message that specifically @mentions the issue submitter and all listed issue reviewers will be constructed and written on any offending issue as a comment indicating that the issue has been open in access of the threshold and should be reviewed and closed immediately. If the value is set to [True](''), then messages will be sent to the log, but will not be published or commented on the repository issue itself.

> By Default this value is set to [False](False)

<br/>

| parameter        | type       | required       | arg info                                                             |
|:----------------:|:----------:|:--------------:|:---------------------------------------------------------------------|
| notify           | [bool]('') | [false](false) | *[True]('') signals notify, [False]('') signals write log only*      |

<br/>

__Examples:__

```python
# Getter method
PublishComment = GitHubReportObj.notify

# Setter method
GitHubReportObj.notify = True
SearchIssues = GitHubReportObj.search_open_pulls()
```

<br/>

__[open_pr_threshold]('')__

Setter method for `open_pr_threshold` property that is used as the threshold metric for any open pull requests or issues discovered during namespace search. If a issue or pull request is open and the created date is greater then the value that is set for this flag in days old, then the issue or pull request will be added to reporting, and can be commented on by the search method to indicate that the pull request or issue has been open for an extended amount of time and should be reviewed and / or merged / closed immediately.

> By Default this value is set to [5](5) days

<br/>

| parameter        | type       | required       | arg info                                                             |
|:----------------:|:----------:|:--------------:|:---------------------------------------------------------------------|
| days             | [int]('')  | [false](false) | *Number of days threshold for pull requests / Github Issues.*        |

<br/>

__[template_path]('')__

Getter only method for `template_path` property that is used to simply get the file location of where the modules HTML report templates are stored. This value can not, nor does not need to have its value altered as the included model templates will always be packaged in the /templates direcotry, held within the project root.

> By Default this value is {/path/to/this/module}/templates/

<br/>

| parameter        | type       | required       | arg info                                                             |
|:----------------:|:----------:|:--------------:|:---------------------------------------------------------------------|
| None             | [N/A]('')  | [N/A]('')      | *No Parameter Value, this is a Getter method only.*                  |

<br/>

__Examples:__

```python
# Getter method
TemplatePath = GitHubReportObj.template_path
```

<br/>

__[search_open_pulls]('')__

The `search_open_pulls` reporting method will search a provided namespace for all open pull requests. For each open pull request item, the pull request Name, HTML URL, Title, Body, Submitter, Reviewers, Merge Data, Creation Data, Age, and Review States will be collected and returned back as a list of dictionaries. This data can then be used with the provided module template to render into an HTML report. The report will indicate by a green background any pull requests that have been approved and are awaiting either additional approvers or the submitter. The report will also indicate with a red background in the PR Days Open field if the pull request has been open longer then the configured `open_pr_threshold` number of days.

<br/>

| parameter        | type       | required       | arg info                                                             |
|:----------------:|:----------:|:--------------:|:---------------------------------------------------------------------|
| auth_token       | [str]('')  | [true](true)   | *Must be a valid Github auth token. The search methods will throw a BadCredentials exception if an invalid token is provided.* |
| repo_namespace   | [str]('')  | [true](true)   | *Must be a valid Github user or organization namespace or reporting and/or any form of desired data collection will fail.*     |

<br/>

__Examples:__

```python
Open_PRs = GitHubReportObj.search_open_pulls(
  auth_token=$TOKEN
  repo_namespace="CloudMages"
)
```

<br/><br/>

__Execution Example:__

```json
Constructing search query for CloudMages repository namespace...
    Open Pull Request Threshold:          5 days
    Notifications Enabled:                False
    Repository Namespace is Organization: True
    Verbose Mode Enabled:                 True

Instantiated Github API Connector Object
Search Results: 1 open PullRequests were returned!

Open PR Search returned 1 results
Validating Search Results...

https://github.com/DaCloudMage/UnitTest-GitUtils/pull/1 Within the Open Days Limit.

Printing Collected Open Pull Request DataSet:

[{
  "id": 123456789,
  "repository": "UnitTest-GitUtils",
  "repository_url": "https://github.com/DaCloudMage/UnitTest-GitUtils",
  "number": 1,
  "submitter": "user_1",
  "reviewers": [],
  "link": "https://github.com/DaCloudMage/UnitTest-GitUtils/pull/1",
  "title": "Open pr",
  "body": "Test Open PR Report",
  "created": datetime.datetime(2020, 4, 9, 0, 29, 56),
  "age": datetime.timedelta(days=-1, seconds=66866, microseconds=735729),
  "age_days": 1,
  "state": "open",
  "is_merged": False,
  "merged": None,
  "mergable": True,
  "merge_state": "clean",
  "merged_by": None,
  "review_count": 0,
  "days_open_threshold": 5
}]

1 / 1 of the returned search results were verified as open pull requests.
```

<br/><br/>

### GithubReports Class Usage

-----

#### GithubReports Default Instantiation

```python
from cloudmage-gitutils import GitHubReports
import os

# Fetch exported Token
AUTH_TOKEN = os.environ['GITHUB_TOKEN']

# Instantiate the object
OpenPRs = GitHubReports(auth_token=AUTH_TOKEN)
OpenPRs.repo_namespace = "CloudMages"
OpenPrs.is_organization = True
SearchOpenPRs = OpenPrs.search_open_pulls()

print(len(SearchOpenPRs))
```

<br/><br/>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Verbose Class Constructor Argument:__](Note) <br/> When instantiating the class an optional `verbose` argument can be provided. The argument expects a bool value of either `True` or `False`. By default verbose is set to False. If `verbose=True` is passed during object instantiation, then debug mode is turned on allowing the class to output DEBUG, INFO, and WARNING messages to stdout, and ERROR messages to stderr.

<br/><br/>

#### GithubReports Verbose Instantiation

```python
from cloudmage-gitutils import GitHubReports
import os

# Fetch exported Token
AUTH_TOKEN = os.environ['GITHUB_TOKEN']

# Instantiate the object
OpenPRs = GitHubReports(auth_token=AUTH_TOKEN, verbose=True)
OpenPRs.repo_namespace = "CloudMages"
OpenPrs.is_organization = True
SearchOpenPRs = OpenPrs.search_open_pulls()

print(len(SearchOpenPRs))

# Class DEBUG, INFO, and WARNING messages will be printed to stdout, and ERROR messages will be printed to stderr
```

<br/><br/>

> ![CloudMage](https://github.com/TheCloudMage/Common-Images/raw/master/icons/note.png) &nbsp;&nbsp; [__Optional Log Object:__](Note) <br/> When instantiating the class an optional `log` argument can also be provided. The argument expects an Logger object to be passed as an input. If passed then all DEBUG, INFO, WARNING, and ERROR messages will be printed to the standard log levels [`log.debug()`, `log.info()`, `log.warning()`, `log.error()`] and printed to the passed respective logger object method.

<br/><br/>

#### GithubReports Log Instantiation

```python
from cloudmage-gitutils import GitHubReports
import os

# Define test log class
# This is an example log object that simply appends any DEBUG, INFO and ERROR received class messages
# to the respective log level list. Normally this would be a logger or custom log object.
class Log(object):
        """Test Log Object"""

        def __init__(self):
            """Class Constructor"""
            self.debug_logs = []
            self.info_logs = []
            self.error_logs = []

        def debug(self, message):
            """Log Debug Messages"""
            self.debug_logs.append(message)

        def info(self, message):
            """Log Debug Messages"""
            self.info_logs.append(message)

        def error(self, message):
            """Log Debug Messages"""
            self.error_logs.append(message)

# Instantiate test log class
GitLog = Log()

# Fetch exported Token
AUTH_TOKEN = os.environ['GITHUB_TOKEN']

# Instantiate the object
OpenPRs = GitHubReports(auth_token=AUTH_TOKEN, verbose=True, log=GitLog)
OpenPRs.repo_namespace = "CloudMages"
OpenPrs.is_organization = True
SearchOpenPRs = OpenPrs.search_open_pulls()

for item in GitLog.debug_logs:
    print(item) # Prints stored debug logs
```

<br/><br/>

## Changelog

To view the project changelog see: [ChangeLog:](CHANGELOG.md)

<br/><br/>

## ![TheCloudMage](https://cloudmage-images-public.s3.us-east-2.amazonaws.com/icons/cloudmage/32/logo.png) &nbsp;&nbsp;Contacts and Contributions

This project is owned and maintained by: [@TheCloudMage](https://github.com/TheCloudMage)

<br/>

To contribute, please:

* Fork the project
* Create a local branch
* Submit Changes
* Create A Pull Request
