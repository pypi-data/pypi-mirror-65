##############################################################################
# CloudMage : Github Open Pull Request Report Action
# ============================================================================
# CloudMage GithubReporting-OpenPR
#   - Search all Github pull requests and notify on PRs
#     that have been open beyond a specified threshold.
# Author: Richard Nason rnason@cloudmage.io
# Project Start: 4/4/2020
# License: GNU GPLv3
##############################################################################

###############
# Imports:    #
###############
# Import Pip Installed Modules:
# from cloudmage.jinjautils import JinjaUtils
from github import Github
from progress.bar import Bar

# Import Base Python Modules
from datetime import datetime
import inspect
import sys
import os


#####################
# Class Definition: #
#####################
class GithubReports(object):
    """ CloudMage Github Reporting Class

    This class is designed to pre package a few reports that can be ran
    against a Github account in order to produce a few common reports that
    can be automated, and produced on a scheduled interval.
    """

    def __init__(self, verbose=False, log=None, auth_token=None):
        """ GithubReports Class Constructor

        Parameters:
            _verbose    (bool): optional [default=False]
            _log        (obj) : optional [default=None]
            _auth_token (str) : optional [default=None]

        Self Attributes:
            self._verbose             (bool) : private
            self._log                 (obj)  : private
            self._log_context         (str)  : private
            self._auth_token          (str)  : private
            self._repo_namespace      (str)  : private
            self._is_organization     (bool) : private
            self._notify              (bool) : private
            self._open_pr_threshold   (int)  : private
            self._search_results      (obj)  : private
        Properties:
            self.verbose             (bool) : public
            self.auth_token          (str)  : public
            self.repo_namespace      (str)  : public
            self.is_organization     (bool) : public
            self.notify              (bool) : public
            self.open_pr_threshold   (int)  : public
            self.template_path       (str)  : public

        Methods:
            self._exception_handler()
            self.log()
            self.search_open_pulls()
        """
        # Class Public Properties and Attributes ######
        # Check the passed value to ensure its a bool before assignment.
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

        # Set the Auth Token that will be used to make the call to github
        if auth_token is not None and isinstance(auth_token, str):
            self._auth_token = auth_token
        else:
            self._auth_token = None

        self._log_context = "CLS->GitHubReports"

        # Class Private Properties and Attributes #
        self._now = datetime.now()         # NOW
        self._repo_namespace = None        # NAMESPACE
        self._is_organization = False      # IS_ORG
        self._notify = False               # NOTIFY
        self._open_pr_threshold = 5        # OPEN_THRESHOLD
        self._search_results = None        # Hold Search Results
        self._template_path = os.path.join(
            os.getcwd(),
            "templates"
        )

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
    # Template Path Getter Method:                 #
    ################################################
    @property
    def template_path(self):
        """ template_path Property Getter

        Getter method for the template_path property.
        This method will return the template_path setting.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._template_path

    ################################################
    # Auth_Token Setter / Getter Methods:          #
    ################################################
    @property
    def auth_token(self):
        """ Auth Token Property Getter

        Getter method for the auth_token property.
        This method will return the auth_token setting.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._auth_token

    @auth_token.setter
    def auth_token(self, token):
        """ auth_token Property Setter

        Setter method for the auth_token property.
        This method will set the auth_token setting if a valid
        str value is provided.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        if token is not None and isinstance(token, str):
            self._auth_token = token
            self.log(
                f"Updated {__id} property with value: {self._auth_token}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type str "
                f"but received type: {type(token)}",
                'error',
                __id
            )

    ############################################
    # GithubReports Getters and Setters:        #
    ############################################
    # self.namespace
    @property
    def repo_namespace(self):
        """ _repo_namespace Property Getter

        Getter method for GithubReports _repo_namespace property.
        This method returns the current repository _repo_namespace
        setting value.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._repo_namespace

    @repo_namespace.setter
    def repo_namespace(self, repo_namespace=None):
        """ _repo_namespace Property Setter

        Setter method for GithubReports _repo_namespace property.
        This method will take a string value, validate it
        is a string, and assign it to the _repo_namespace property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid str value then set the value.
        if (
            repo_namespace is not None and
            isinstance(repo_namespace, str)
        ):
            self._repo_namespace = repo_namespace
            self.log(
                f"Updated {__id} property with value: {self._repo_namespace}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type str "
                f"but received type: {type(repo_namespace)}",
                'error',
                __id
            )

    # self.is_organization
    @property
    def is_organization(self):
        """ is_organization Property Getter

        Getter method for GithubReports is_organization property.
        This method returns a bool value indicating if the
        current instance of the class targets a user or organization
        repository.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._is_organization

    @is_organization.setter
    def is_organization(self, is_organization=False):
        """ is_organization Property Setter

        Setter method for GithubReports is_organization property.
        This method will take a bool value, validate it
        is a bool value, and assign it to the is_organization property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid bool value then set the value.
        if (
            is_organization is not None and
            isinstance(is_organization, bool)
        ):
            self._is_organization = is_organization
            self.log(
                f"Updated {__id} property with value: {self._is_organization}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type bool "
                f"but received type: {type(is_organization)}",
                'error',
                __id
            )

    # self.notify
    @property
    def notify(self):
        """ notify Property Getter

        Getter method for GithubReports _notify property.
        This method returns a bool value indicating if the
        current instance of the class will perform notification
        actions such as commenting on a repository.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._notify

    @notify.setter
    def notify(self, notify=False):
        """ is_organization Property Setter

        Setter method for GithubReports _notify property.
        This method will take a bool value, validate it
        is a bool value, and assign it to the notify property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid bool value then set the value.
        if (
            notify is not None and
            isinstance(notify, bool)
        ):
            self._notify = notify
            self.log(
                f"Updated {__id} property with value: {self._notify}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type bool "
                f"but received type: {type(notify)}",
                'error',
                __id
            )

    # self.open_pr_threshold
    @property
    def open_pr_threshold(self):
        """ open_pr_threshold Property Getter

        Getter method for GithubReports _open_pr_threshold property.
        This method returns a bool value indicating the current
        threshold that pull requests can be open before notifications
        are sent to the pull request to resolve.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property requested.", 'info', __id)
        return self._open_pr_threshold

    @open_pr_threshold.setter
    def open_pr_threshold(self, open_pr_threshold=5):
        """ open_pr_threshold Property Setter

        Setter method for GithubReports _open_pr_threshold property.
        This method will take an int value, validate it
        is an int value, and assign it to the open_pr_threshold property.
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} property update requested.", 'info', __id)

        # if the passed value is a valid int value then set the value.
        if (
            open_pr_threshold is not None and
            isinstance(open_pr_threshold, int) and
            not isinstance(open_pr_threshold, bool)
        ):
            self._open_pr_threshold = open_pr_threshold
            self.log(
                f"Updated {__id} property with value: "
                f"{self._open_pr_threshold}",
                'info',
                __id
            )
        else:
            self.log(
                f"{__id} property argument expected type int "
                f"but received type: {type(open_pr_threshold)}",
                'error',
                __id
            )

    ############################################
    # Class Methods:                           #
    ############################################
    def search_open_pulls(self, auth_token=None, repo_namespace=None):
        """ GithubReports Open Pull Request Report Collector

        GithubReports method that will perform a search for all
        open pull requests and construct a return object that will
        contain a list of dictionaries with relevant pull request
        data

        Search filters can be found on githubs documentation page:
        https://help.github.com/en/github/
        searching-for-information-on-github/searching-issues-and-pull-requests
        """
        # Define this methods identity for functional logging:
        __id = inspect.stack()[0][3]
        self.log(f"{__id} method called.", 'info', __id)

        # Check the passed auth_token, if it has a value, then
        # set the auth_token property.
        if auth_token is not None and isinstance(auth_token, str):
            self._auth_token = auth_token

        # Check the passed repo_namespace, if it has a value, then
        # set the repo_namespace property.
        if repo_namespace is not None and isinstance(repo_namespace, str):
            self._repo_namespace = repo_namespace

        # Test to ensure required args have been provided
        if self._auth_token is None:
            self.log(
                "Github auth_token required to call this method! "
                "The auth_token can be set by passing the method argument "
                "search_open_pulls(auth_token=<token>) or by setting the "
                "token using the property setter method "
                "Obj.auth_token = <token> before calling the "
                "search_open_pulls() method.",
                'error',
                __id
            )
            return None
        elif self._repo_namespace is None:
            self.log(
                "Github repo_namespace required to call this method! "
                "The repo_namespace can be set by passing the method "
                "argument search_open_pulls(repo_namespace=<namespace>) "
                "or by setting the namespace using the property setter "
                "method Obj.repo_namespace = <namespace> before calling the "
                "search_open_pulls() method. If the repository is an "
                "organization repository, then Obj.is_organization = True "
                "must also be set or user repositories will be searched "
                "instead of organization repositories.",
                'error',
                __id
            )
            return None

        this_call_message = (
            f"Constructing search query for {self._repo_namespace} "
            "repository namespace...\n"
            "\tOpen Pull Request Threshold: "
            f"{' ' * 9}{self._open_pr_threshold} days\n"
            "\tNotifications Enabled: "
            f"{' ' * 15}{self._notify}\n"
            "\tRepository Namespace is Organization: "
            f"{self._is_organization}\n"
            "\tVerbose Mode Enabled: "
            f"{' ' * 16}{self._verbose}\n"
        )
        print(this_call_message)
        self.log(this_call_message, 'debug', __id)

        # Prep the search_results internal property to store the
        # expected result set
        self._search_results = []

        # Instantiate the Github Object and Search for Open Pull Requests
        try:
            # Instantiate a Github object using the Provided Github Token.
            ThisGithub = Github(self._auth_token, per_page=100)
            self.log(
                f"Instantiated Github API Connector Object",
                'debug',
                __id
            )
        except Exception as e:
            ThisGithubException = (
                "An un-expected error occurred when attempting to "
                "instantiate a new Github API Connector object."
            )
            print(f"{ThisGithubException}\n")
            self.log(ThisGithubException, 'error', __id)
            self._exception_handler(__id, e)
            return None

        # Construct the Github Issue Query
        try:
            if self._is_organization:
                ThisSearchResults = ThisGithub.search_issues(
                    'is:unmerged',
                    org=self._repo_namespace,
                    state='open',
                    type='pr'
                )
            else:
                ThisSearchResults = ThisGithub.search_issues(
                    'is:unmerged',
                    user=self._repo_namespace,
                    state='open',
                    type='pr'
                )
            self.log(
                f"Search Results: {ThisSearchResults.totalCount} "
                "open PullRequests were returned!",
                'debug',
                __id
            )

            print(
                "Open PR Search returned "
                f"{ThisSearchResults.totalCount} results"
            )
        except Exception as e:
            ThisSearchResultsException = (
                "An un-expected error occurred when attempting to "
                "perform a Github issue search for open PRs."
            )
            print(f"{ThisSearchResultsException}\n")
            self.log(ThisSearchResultsException, 'error', __id)
            self._exception_handler(__id, e)
            return None

        # If no results were returned then exit gracefully
        if ThisSearchResults.totalCount == 0:
            print("Search completed. Exiting search...")
            self.log(
                f"0 results returned, exiting search function...",
                'info',
                __id
            )
            return None
        else:
            print("Validating Search Results...\n")
            ThisSearchProgress = Bar(
                'Processing',
                max=ThisSearchResults.totalCount
            )

            this_open_exceeded_pr_comment = (
                f"has been open for {self._open_pr_threshold} days or "
                "longer. Please review the pull request, and merge or "
                "close at the earliest convenience. This reminder "
                "notification will be sent daily until this open pull "
                "request has been resolved. Thank you."
            )

            # For each returned issue, parse the desired data.
            try:
                for _issue_ in ThisSearchResults:
                    # Temp item data containers
                    this_pr_data = {}
                    this_pr_reviewers = []
                    this_pr_reviewer_mentions = (
                        f"@{_issue_.user.login} "
                    )

                    # Get pull request object
                    ThisPullRequest = (
                        _issue_.repository.get_pull(_issue_.number)
                    )

                    # If the flagged Pull Request is merged, ignore it
                    if (
                        ThisPullRequest.merged or
                        ThisPullRequest.merged_at is not None or
                        ThisPullRequest.merged_by is not None
                    ):
                        continue  # pragma: no cover

                    # Get designated pull request reviewers
                    ThisPullRequestedReviewers = (
                        ThisPullRequest.get_review_requests()
                    )
                    # Users
                    for _user_ in ThisPullRequestedReviewers[0]:
                        this_pr_reviewers.append(_user_.login)
                        this_pr_reviewer_mentions += (
                            f"@{_user_.login} "
                        )
                    # Teams
                    for _user_ in ThisPullRequestedReviewers[1]:
                        this_pr_reviewers.append(_user_.name)
                        this_pr_reviewer_mentions += (
                            f"@{_user_.name} "
                        )

                    # Get pull request reviews
                    ThisPullReviews = ThisPullRequest.get_reviews()
                    if ThisPullReviews.totalCount > 0:
                        for _review_ in ThisPullReviews:
                            this_pr_reviewer_status = (
                                f"{_review_.user.login}: {_review_.state}"
                            )
                            if (
                                _review_.user.login not in
                                this_pr_reviewer_mentions
                            ):
                                this_pr_reviewer_mentions += (
                                    f"@{_review_.user.login} "
                                )  # pragma: no cover
                            if _review_.user.login in this_pr_reviewers:
                                this_index = this_pr_reviewers.index(
                                    _review_.user.login
                                )
                                this_pr_reviewers[this_index] = (
                                    this_pr_reviewer_status
                                )
                            else:
                                this_pr_reviewers.append(
                                    this_pr_reviewer_status
                                )  # pragma: no cover

                    # Set the pull request age, and update
                    # the var_pr_dataset object
                    this_pr_age = (
                        self._now - ThisPullRequest.created_at
                    )

                    # Construct a PR message to get published if notify
                    this_pr_comment_msg = (
                        f"{this_pr_reviewer_mentions}"
                        f"{_issue_.html_url} "
                        f"{this_open_exceeded_pr_comment}"
                    )

                    # If send_notifications true,
                    # create a mention comment on the PR
                    if (
                        int(this_pr_age.days) >
                        int(self._open_pr_threshold)
                    ):
                        if self._verbose:
                            print(
                                f"{_issue_.html_url} "
                                "Exceeded the Open Days Limit!\n"
                            )
                            print(
                                "Constructing PullRequest "
                                "Notification Comment:"
                            )
                            print(f"\n{this_pr_comment_msg}\n")
                        if self._notify:
                            ThisPullRequest.create_issue_comment(
                                this_pr_comment_msg
                            )  # pragma: no cover
                            if self._verbose:
                                print(
                                    "Comment published successfully!\n"
                                )  # pragma: no cover
                        else:
                            if self._verbose:  # pragma: no cover
                                print(
                                    "Notifications currently disabled: "
                                    "The constructed notification comment "
                                    "was not published to the pull request.\n"
                                )  # pragma: no cover
                    else:
                        if self._verbose:
                            print(
                                f"{_issue_.html_url} "
                                "Within the Open Days Limit.\n"
                            )

                    # Construct Required DataPoint Dictionary
                    # to render the report:
                    this_pr_data.update(
                        id=_issue_.id,
                        repository=_issue_.repository.name,
                        repository_url=_issue_.repository.html_url,
                        number=_issue_.number,
                        submitter=_issue_.user.login,
                        reviewers=this_pr_reviewers,
                        link=_issue_.html_url,
                        title=_issue_.title,
                        body=_issue_.body,
                        created=ThisPullRequest.created_at,
                        age=this_pr_age,
                        age_days=int(this_pr_age.days),
                        state=ThisPullRequest.state,
                        is_merged=ThisPullRequest.merged,
                        merged=ThisPullRequest.merged_at,
                        mergable=ThisPullRequest.mergeable,
                        merge_state=ThisPullRequest.mergeable_state,
                        merged_by=ThisPullRequest.merged_by,
                        review_count=ThisPullReviews.totalCount,
                        days_open_threshold=int(self._open_pr_threshold)
                    )

                    # Add the storage object to the OpenPullRequests list
                    self._search_results.append(this_pr_data)
                    ThisSearchProgress.next()

                ThisSearchProgress.finish()

                if self._verbose:
                    print("Printing Collected Open Pull Request DataSet: ")
                    for _pr_ in self._search_results:
                        print(f"\n{_pr_}\n")

                print(
                    f"{len(self._search_results)} / "
                    f"{ThisSearchResults.totalCount} "
                    "of the returned search results were verified as open "
                    "pull requests.\n"
                )
                return self._search_results
            except Exception as e:  # pragma: no cover
                ThisParseSearchException = (
                    "An unexpected error occurred parsing "
                    "the PullRequest response dataset:\n"
                )  # pragma: no cover
                print(f"{ThisParseSearchException}\n")  # pragma: no cover
                self.log(
                    ThisParseSearchException, 'error', __id
                )  # pragma: no cover
                self._exception_handler(__id, e)  # pragma: no cover
                return None  # pragma: no cover

    # def write(self, path=None):
    #     """ GithubReports Report Writer

    #     GithubReports method that will take the data that was collected
    #     about the open pull requests and pass it to an HTML template via
    #     Jinja, which will allow us to spit out a nicely html formatted
    #     Open PR report Template.
    #     """
    #     # Define this methods identity for functional logging:
    #     __id = inspect.stack()[0][3]
    #     self.log(f"{__id} method called.", 'info', __id)

    #     # Set Jinja Template and Output Paths
    #     this_jinja_template_path = os.path.join(os.getcwd(), 'templates')
    #     this_jinja_output_path = os.path.join(os.getcwd(), 'reports')
    #     this_jinja_output_file = "OpenPRs.html"

    #     # If a custom path was set then set it
    #     if (
    #         path is not None and
    #         isinstance(path, str) and
    #         os.path.exists(path)
    #     ):
    #         this_jinja_output_path = path

    #     # Construct the full path to the output file
    #     this_report = os.path.join(
    #         this_jinja_template_path,
    #         this_jinja_output_file
    #     )

    #     # Instantiate JinjaUtils Object and Load the Open PR Report Template.
    #     # We don't need error checking as the JinjaUtils
    #     # module already handles it in the module the same way this one does.
    #     ThisJinja = JinjaUtils(verbose=self._verbose)

    #     # Set Jinja env
    #     ThisJinja.template_directory = this_jinja_template_path
    #     ThisJinja.load = 'Github_Open_PR_Report.j2'

    #     # Render the template
    #     print(f"Jinja is Rendering: {this_report}...")
    #     ThisJinja.render(
    #         RepoNamespace=self.repo_namespace,
    #         OpenPullRequests=self._search_results
    #     )

    #     # Write the template.
    #     print(f"Jinja is Writing File: {this_report}...")
    #     ThisJinja.write(
    #         output_directory=this_jinja_output_path,
    #         output_file=this_jinja_output_file,
    #         backup=False
    #     )
