import hashlib
import json
import random
import requests
import string
import time


class Polygon:
    """
    """

    # API methods
    _CONTEST_PROBLEMS = 'contest.problems'
    _PROBLEM_INFO = 'problem.info'
    _PROBLEM_UPDATE_INFO = 'problem.updateInfo'
    _PROBLEM_STATEMENTS = 'problem.statements'
    _PROBLEM_SAVE_STATEMENT = 'problem.saveStatement'
    _PROBLEM_STATEMENT_RESOURCES = 'problem.statementResources'
    _PROBLEM_SAVE_STATEMENT_RESOURCE = 'problem.saveStatementResource'
    _PROBLEMS_LIST = 'problems.list'
    _PROBLEM_CHECKER = 'problem.checker'
    _PROBLEM_CHECKER = 'problem.checker'
    _PROBLEM_VALIDATOR = 'problem.validator'
    _PROBLEM_INTERACTOR = 'problem.interactor'
    _PROBLEM_FILES = 'problem.files'
    _PROBLEM_SOLUTIONS = 'problem.solutions'
    _PROBLEM_VIEW_FILE = 'problem.viewFile'
    _PROBLEM_VIEW_SOLUTION = 'problem.viewSolution'
    _PROBLEM_SCRIPT = 'problem.script'
    _PROBLEM_TESTS = 'problem.tests'
    _PROBLEM_TEST_INPUT = 'problem.testInput'
    _PROBLEM_TEST_ANSWER = 'problem.testAnswer'
    _PROBLEM_SET_VALIDATOR = 'problem.setValidator'
    _PROBLEM_SET_CHECKER = 'problem.setChecker'
    _PROBLEM_SET_INTERACTOR = 'problem.setInteractor'
    _PROBLEM_SAVE_FILE = 'problem.saveFile'
    _PROBLEM_SAVE_SOLUTION = 'problem.saveSolution'
    _PROBLEM_EDIT_SOLUTION_EXTRA_TAGS = 'problem.editSolutionExtraTags'
    _PROBLEM_SAVE_SCRIPT = 'problem.saveScript'
    _PROBLEM_SAVE_TEST = 'problem.saveTest'
    _PROBLEM_ENABLE_GROUPS = 'problem.enableGroups'
    _PROBLEM_ENABLE_POINTS = 'problem.enablePoints'
    _PROBLEM_VIEW_TEST_GROUP = 'problem.viewTestGroup'
    _PROBLEM_SAVE_TEST_GROUP = 'problem.saveTestGroup'
    _PROBLEM_VIEW_TAGS = 'problem.viewTags'
    _PROBLEM_SAVE_TAGS = 'problem.saveTags'
    _PROBLEM_VIEW_GENERAL_DESCRIPTION = 'problem.viewGeneralDescription'
    _PROBLEM_SAVE_GENERAL_DESCRIPTION = 'problem.saveGeneralDescription'
    _PROBLEM_VIEW_GENERAL_TUTORIAL = 'problem.viewGeneralTutorial'
    _PROBLEM_SAVE_GENERAL_TUTORIAL = 'problem.saveGeneralTutorial'


    def __init__(self, api_url, api_key, api_secret):
        self.request_config = RequestConfig(api_url, api_key, api_secret)

    def problems_list(self):
        """
        """
        response = self._request_ok_or_raise(self._PROBLEMS_LIST)
        return [Problem(self, p_json) for p_json in response.result]

    def problem_info(self, problem_id):
        """
        """
        response = self._request_ok_or_raise(
            self._PROBLEM_INFO,
            args={ 'problemId': problem_id },
        )
        return ProblemInfo(response.result)

    def problem_update_info(self, problem_id, problem_info):
        """
        """
        response = self._request_ok_or_raise(
            self._PROBLEM_UPDATE_INFO,
            args={
                'problemId': problem_id,
                'inputFile': problem_info.input_file,
                'outputFile': problem_info.output_file,
                'interactive': problem_info.interactive, # TODO
                'timeLimit': problem_info.time_limit,
                'memoryLimit': problem_info.memory_limit,
            },
        )
        return response.result

    def problem_view_tags(self, problem_id):
        """
        """
        response = self._request_ok_or_raise(
            self._PROBLEM_VIEW_TAGS,
            args={ 'problemId': problem_id },
        )
        return response.result

    def problem_save_tags(self, problem_id, tags):
        """
        """
        tags_str = ','.join(tags)
        response = self._request_ok_or_raise(
            self._PROBLEM_SAVE_TAGS,
            args={
                'problemId': problem_id,
                'tags': tags_str,
            },
        )
        return response.result

    def problem_view_general_description(self, problem_id):
        """
        """
        response = self._request_ok_or_raise(
            self._PROBLEM_VIEW_GENERAL_DESCRIPTION,
            args={ 'problemId': problem_id },
        )
        return response.result

    def problem_save_general_description(self, problem_id, description):
        """
        """
        response = self._request_ok_or_raise(
            self._PROBLEM_SAVE_GENERAL_DESCRIPTION,
            args={
                'problemId': problem_id,
                'description': description,
            },
        )
        return response.result

    def contest_problems(self, contest_id):
        """
        """
        response = self._request_ok_or_raise(
            self._CONTEST_PROBLEMS,
            args={ 'contestId': contest_id },
        )
        return {
            name: Problem(self, p_json)
            for name, p_json in response.result.items()
        }

    def _request_ok_or_raise(self, method_name, args=None):
        response = self._request(method_name, args=args)
        if response.status != Response.STATUS_OK:
            raise Exception(response.comment)
        return response

    def _request(self, method_name, args=None):
        request = Request(self.request_config, method_name, args)
        return request.issue()


class Problem:
    """
    """

    # JSON field names
    _ID_FIELD = 'id'
    _OWNER_FIELD = 'owner'
    _NAME_FIELD = 'name'
    _DELETED_FIELD = 'deleted'
    _FAVORITE_FIELD = 'favourite'
    _ACCESS_TYPE_FIELD = 'accessType'
    _REVISION_FIELD = 'revision'
    _LATEST_PACKAGE_FIELD = 'latestPackage'
    _MODIFIED_FIELD = 'modified'

    def __init__(self, polygon, problem_json):
        self._polygon = polygon

        self.id = problem_json.get(Problem._ID_FIELD)
        self.owner = problem_json.get(Problem._OWNER_FIELD)
        self.name = problem_json.get(Problem._NAME_FIELD)
        self.deleted = problem_json.get(Problem._DELETED_FIELD)
        self.favorite = problem_json.get(Problem._FAVORITE_FIELD)
        self.access_type = problem_json.get(Problem._ACCESS_TYPE_FIELD)
        self.revision = problem_json.get(Problem._REVISION_FIELD)
        self.latest_package = problem_json.get(Problem._LATEST_PACKAGE_FIELD)
        self.modified = problem_json.get(Problem._MODIFIED_FIELD)

    def __str__(self):
        return '{}:{}'.format(self.name, self.id)

    def info(self):
        return self._polygon.problem_info(self.id)

    def update_info(self, problem_info):
        return self._polygon.problem_update_info(self.id, problem_info)

    def view_tags(self):
        return self._polygon.problem_view_tags(self.id)

    def save_tags(self, tags):
        return self._polygon.problem_save_tags(self.id, tags)

    def view_general_description(self):
        return self._polygon.problem_view_general_description(self.id)

    def save_general_description(self, description):
        return self._polygon.problem_save_general_description(
            self.id, description)


class ProblemInfo:
    """
    """
    
    # JSON field names
    _INPUT_FILE = 'memoryLimit'
    _OUTPUT_FILE = 'timeLimit'
    _INTERACTIVE = 'interactive'
    _TIME_LIMIT = 'outputFile'
    _MEMORY_LIMIT = 'inputFile'

    def __init__(self, problem_info_json):
        self.input_file = problem_info_json[ProblemInfo._INPUT_FILE]
        self.output_file = problem_info_json[ProblemInfo._OUTPUT_FILE]
        self.interactive = problem_info_json[ProblemInfo._INTERACTIVE]
        self.time_limit = problem_info_json[ProblemInfo._TIME_LIMIT]
        self.memory_limit = problem_info_json[ProblemInfo._MEMORY_LIMIT]


class Request:
    """
    Request to Polygon API.
    TODO: update
    Usage example:
    >>> request = Request(Request.CONTEST_PROBLEMS,
    ...                   args={'contestId': contest_id})
    >>> response = request.issue()
    >>> problems = response["result"]
    """

    def __init__(self, config, method_name, args=None):
        if args is None:
            args = {}

        self.config = config
        self.method_name = method_name
        self.args = args

    def issue(self):
        """Issues request and returns parsed JSON response"""

        args = dict(self.args)
        args['apiKey'] = self.config.api_key
        args['time'] = int(time.time())
        args['apiSig'] = self.get_api_signature(args, self.config.api_secret)
        response = requests.get(
            self.config.api_url + self.method_name, params=args)
        return Response(json.loads(response.text))

    def get_api_signature(self, args, api_secret):
        rand_bit = ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for _ in range(6))

        arg_tuples = list(sorted(args.items()))
        args_bit = '&'.join(key + '=' + str(value) for key, value in arg_tuples)
        api_signature_string = '{}/{}?{}#{}'.format(
            rand_bit, self.method_name, args_bit, api_secret)
        api_signature = (
            rand_bit +
            hashlib.sha512(api_signature_string.encode('utf-8')).hexdigest())
        return api_signature


class Response:
    """
    """

    # JSON field names
    FIELD_STATUS = 'status'
    FIELD_COMMENT = 'comment'
    FIELD_RESULT = 'result'

    # Status values
    STATUS_OK = 'OK'
    STATUS_FAILED = 'FAILED'
    STATUS_UNKNOWN = 'UNKNOWN'

    def __init__(self, response_json):
        self.status = response_json.get(Response.FIELD_STATUS)
        if self.status not in [Response.STATUS_OK, Response.STATUS_FAILED]:
            self.status = Response.STATUS_UNKNOWN

        self.comment = response_json.get(Response.FIELD_COMMENT, '')
        self.result = response_json.get(Response.FIELD_RESULT)


class RequestConfig:
    def __init__(self, api_url, api_key, api_secret):
        self.api_url = api_url
        self.api_key = api_key
        self.api_secret = api_secret
