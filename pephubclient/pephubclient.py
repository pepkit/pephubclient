import json
import os
from typing import NoReturn, Optional, Literal

import pandas as pd
import peppy
from peppy.const import (
    NAME_KEY,
    DESC_KEY,
    CONFIG_KEY,
    SUBSAMPLE_RAW_LIST_KEY,
    SAMPLE_RAW_DICT_KEY,
)
import requests
import urllib3
from pydantic.error_wrappers import ValidationError
from ubiquerg import parse_registry_path

from pephubclient.constants import (
    PEPHUB_PEP_API_BASE_URL,
    PEPHUB_PUSH_URL,
    RegistryPath,
    ResponseStatusCodes,
    PEPHUB_PEP_SEARCH_URL,
)
from pephubclient.exceptions import (
    IncorrectQueryStringError,
    PEPExistsError,
    ResponseError,
)
from pephubclient.files_manager import FilesManager
from pephubclient.helpers import MessageHandler, RequestManager
from pephubclient.models import (
    ProjectDict,
    ProjectUploadData,
    SearchReturnModel,
    ProjectAnnotationModel,
)
from pephubclient.pephub_oauth.pephub_oauth import PEPHubAuth

urllib3.disable_warnings()


class PEPHubClient(RequestManager):
    USER_DATA_FILE_NAME = "jwt.txt"
    home_path = os.getenv("HOME")
    if not home_path:
        home_path = os.path.expanduser("~")
    PATH_TO_FILE_WITH_JWT = (
        os.path.join(home_path, ".pephubclient/") + USER_DATA_FILE_NAME
    )

    def __init__(self):
        self.registry_path = None

    def login(self) -> NoReturn:
        """
        Log in to PEPhub
        """
        user_token = PEPHubAuth().login_to_pephub()

        FilesManager.save_jwt_data_to_file(self.PATH_TO_FILE_WITH_JWT, user_token)

    def logout(self) -> NoReturn:
        """
        Log out from PEPhub
        """
        FilesManager.delete_file_if_exists(self.PATH_TO_FILE_WITH_JWT)

    def pull(self, project_registry_path: str, force: Optional[bool] = False) -> None:
        """
        Download project locally

        :param str project_registry_path: Project registry path in PEPhub (e.g. databio/base:default)
        :param bool force: if project exists, overwrite it.
        :return: None
        """
        jwt_data = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)
        project_dict = self._load_raw_pep(
            registry_path=project_registry_path, jwt_data=jwt_data
        )

        self._save_raw_pep(
            reg_path=project_registry_path, project_dict=project_dict, force=force
        )

    def load_project(
        self,
        project_registry_path: str,
        query_param: Optional[dict] = None,
    ) -> peppy.Project:
        """
        Load peppy project from PEPhub in peppy.Project object

        :param project_registry_path: registry path of the project
        :param query_param: query parameters used in get request
        :return Project: peppy project.
        """
        jwt = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)
        raw_pep = self._load_raw_pep(project_registry_path, jwt, query_param)
        peppy_project = peppy.Project().from_dict(raw_pep)
        return peppy_project

    def push(
        self,
        cfg: str,
        namespace: str,
        name: Optional[str] = None,
        tag: Optional[str] = None,
        is_private: Optional[bool] = False,
        force: Optional[bool] = False,
    ) -> None:
        """
        Push (upload/update) project to Pephub using config/csv path

        :param str cfg: Project config file (YAML) or sample table (CSV/TSV)
            with one row per sample to constitute project
        :param str namespace: namespace
        :param str name: project name
        :param str tag: project tag
        :param bool is_private: Specifies whether project should be private [Default= False]
        :param bool force: Force push to the database. Use it to update, or upload project. [Default= False]
        :return: None
        """
        peppy_project = peppy.Project(cfg=cfg)
        self.upload(
            project=peppy_project,
            namespace=namespace,
            name=name,
            tag=tag,
            is_private=is_private,
            force=force,
        )

    def upload(
        self,
        project: peppy.Project,
        namespace: str,
        name: str = None,
        tag: str = None,
        is_private: bool = False,
        force: bool = True,
    ) -> None:
        """
        Upload peppy project to the PEPhub.

        :param peppy.Project project: Project object that has to be uploaded to the DB
        :param namespace: namespace
        :param name: project name
        :param tag: project tag
        :param force: Force push to the database. Use it to update, or upload project.
        :param is_private: Make project private
        :param force: overwrite project if it exists
        :return: None
        """
        jwt_data = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)
        if name:
            project[NAME_KEY] = name

        upload_data = ProjectUploadData(
            pep_dict=project.to_dict(
                extended=True,
                orient="records",
            ),
            tag=tag,
            is_private=is_private,
            overwrite=force,
        )
        pephub_response = self.send_request(
            method="POST",
            url=self._build_push_request_url(namespace=namespace),
            headers=self._get_header(jwt_data),
            json=upload_data.dict(),
            cookies=None,
        )
        if pephub_response.status_code == ResponseStatusCodes.ACCEPTED:
            MessageHandler.print_success(
                f"Project '{namespace}/{name}:{upload_data.tag}' was successfully uploaded"
            )
        elif pephub_response.status_code == ResponseStatusCodes.CONFLICT:
            raise ResponseError(
                "Project already exists. Set force to overwrite project."
            )
        elif pephub_response.status_code == ResponseStatusCodes.UNAUTHORIZED:
            raise ResponseError("Unauthorized! Failure in uploading project.")
        elif pephub_response.status_code == ResponseStatusCodes.FORBIDDEN:
            raise ResponseError(
                "User does not have permission to write to this namespace!"
            )
        else:
            raise ResponseError(
                f"Unexpected Response Error. {pephub_response.status_code}"
            )
        return None

    def find_project(
        self,
        namespace: str,
        query_string: str = "",
        limit: int = 100,
        offset: int = 0,
        filter_by: Literal["submission_date", "last_update_date"] = None,
        start_date: str = None,
        end_date: str = None,
    ) -> SearchReturnModel:
        """
        Find project in specific namespace and return list of PEP annotation

        :param namespace: Namespace where to search for projects
        :param query_string: Search query
        :param limit: Return limit
        :param offset: Return offset
        :param filter_by: Use filter date. Option: [submission_date, last_update_date]
        :param start_date: filter beginning date
        :param end_date: filter end date (if none today's date is used)
        :return:
        """
        jwt_data = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)

        query_param = {
            "q": query_string,
            "limit": limit,
            "offset": offset,
        }
        if filter_by in ["submission_date", "last_update_date"]:
            query_param["filter_by"] = filter_by
            query_param["filter_start_date"] = start_date
            if end_date:
                query_param["filter_end_date"] = end_date

        url = self._build_project_search_url(
            namespace=namespace,
            query_param=query_param,
        )

        pephub_response = self.send_request(
            method="GET",
            url=url,
            headers=self._get_header(jwt_data),
            json=None,
            cookies=None,
        )
        if pephub_response.status_code == ResponseStatusCodes.OK:
            decoded_response = self._handle_pephub_response(pephub_response)
            project_list = []
            for project_found in json.loads(decoded_response)["items"]:
                project_list.append(ProjectAnnotationModel(**project_found))
            return SearchReturnModel(**json.loads(decoded_response))

    @staticmethod
    def _save_raw_pep(
        reg_path: str,
        project_dict: dict,
        force: bool = False,
    ) -> None:
        """
        Save project locally.

        :param dict project_dict: PEP dictionary (raw project)
        :param bool force: overwrite project if exists
        :return: None
        """
        reg_path_model = RegistryPath(**parse_registry_path(reg_path))
        folder_path = FilesManager.create_project_folder(registry_path=reg_path_model)

        def full_path(fn: str) -> str:
            return os.path.join(folder_path, fn)

        project_name = project_dict[CONFIG_KEY][NAME_KEY]
        sample_table_filename = "sample_table.csv"
        yaml_full_path = full_path(f"{project_name}_config.yaml")
        sample_full_path = full_path(sample_table_filename)
        if not force:
            extant = [
                p for p in [yaml_full_path, sample_full_path] if os.path.isfile(p)
            ]
            if extant:
                raise PEPExistsError(
                    f"{len(extant)} file(s) exist(s): {', '.join(extant)}"
                )

        config_dict = project_dict.get(CONFIG_KEY)
        config_dict[NAME_KEY] = project_name
        config_dict[DESC_KEY] = project_dict[CONFIG_KEY][DESC_KEY]
        config_dict["sample_table"] = sample_table_filename

        sample_pandas = pd.DataFrame(project_dict.get(SAMPLE_RAW_DICT_KEY, {}))

        subsample_list = [
            pd.DataFrame(sub_a)
            for sub_a in project_dict.get(SUBSAMPLE_RAW_LIST_KEY) or []
        ]

        filenames = []
        for idx, subsample in enumerate(subsample_list):
            fn = f"subsample_table{idx + 1}.csv"
            filenames.append(fn)
            FilesManager.save_pandas(subsample, full_path(fn), not_force=False)
        config_dict["subsample_table"] = filenames

        FilesManager.save_yaml(config_dict, yaml_full_path, not_force=False)
        FilesManager.save_pandas(sample_pandas, sample_full_path, not_force=False)

        if config_dict.get("subsample_table"):
            for number, subsample in enumerate(subsample_list):
                FilesManager.save_pandas(
                    subsample,
                    os.path.join(folder_path, config_dict["subsample_table"][number]),
                    not_force=False,
                )

        MessageHandler.print_success(
            f"Project was downloaded successfully -> {folder_path}"
        )
        return None

    def _load_raw_pep(
        self,
        registry_path: str,
        jwt_data: Optional[str] = None,
        query_param: Optional[dict] = None,
    ) -> dict:
        """project_name
        Request PEPhub and return the requested project as peppy.Project object.

        :param registry_path: Project namespace, eg. "geo/GSE124224:tag"
        :param query_param: Optional variables to be passed to PEPhub
        :param jwt_data: JWT token.
        :return: Raw project in dict.
        """
        if not jwt_data:
            jwt_data = FilesManager.load_jwt_data_from_file(self.PATH_TO_FILE_WITH_JWT)
        query_param = query_param or {}
        query_param["raw"] = "true"

        self._set_registry_data(registry_path)
        pephub_response = self.send_request(
            method="GET",
            url=self._build_pull_request_url(query_param=query_param),
            headers=self._get_header(jwt_data),
            cookies=None,
        )
        if pephub_response.status_code == ResponseStatusCodes.OK:
            decoded_response = self._handle_pephub_response(pephub_response)
            correct_proj_dict = ProjectDict(**json.loads(decoded_response))

            # This step is necessary because of this issue: https://github.com/pepkit/pephub/issues/124
            return correct_proj_dict.dict(by_alias=True)

        if pephub_response.status_code == ResponseStatusCodes.NOT_EXIST:
            raise ResponseError("File does not exist, or you are unauthorized.")
        if pephub_response.status_code == ResponseStatusCodes.INTERNAL_ERROR:
            raise ResponseError(
                f"Internal server error. Unexpected return value. Error: {pephub_response.status_code}"
            )

    def _set_registry_data(self, query_string: str) -> None:
        """
        Parse provided query string to extract project name, sample name, etc.

        :param query_string: Passed by user. Contain information needed to locate the project.
        :return: Parsed query string.
        """
        try:
            self.registry_path = RegistryPath(**parse_registry_path(query_string))
        except (ValidationError, TypeError):
            raise IncorrectQueryStringError(query_string=query_string)

    @staticmethod
    def _get_header(jwt_data: Optional[str] = None) -> dict:
        """
        Create Authorization header

        :param jwt_data: jwt string
        :return: Authorization dict
        """
        if jwt_data:
            return {"Authorization": jwt_data}
        else:
            return {}

    def _build_pull_request_url(self, query_param: dict = None) -> str:
        """
        Build request for getting projects form pephub

        :param query_param: dict of parameters used in query string
        :return: url string
        """
        query_param = query_param or {}
        query_param["tag"] = self.registry_path.tag

        endpoint = self.registry_path.namespace + "/" + self.registry_path.item

        variables_string = PEPHubClient._parse_query_param(query_param)
        endpoint += variables_string

        return PEPHUB_PEP_API_BASE_URL + endpoint

    def _build_project_search_url(
        self, namespace: str, query_param: dict = None
    ) -> str:
        """
        Build request for searching projects form pephub

        :param query_param: dict of parameters used in query string
        :return: url string
        """

        variables_string = PEPHubClient._parse_query_param(query_param)
        endpoint = variables_string

        return PEPHUB_PEP_SEARCH_URL.format(namespace=namespace) + endpoint

    @staticmethod
    def _build_push_request_url(namespace: str) -> str:
        """
        Build project uplaod request used in pephub

        :param namespace: namespace where project will be uploaded
        :return: url string
        """
        return PEPHUB_PUSH_URL.format(namespace=namespace)

    @staticmethod
    def _parse_query_param(pep_variables: dict) -> str:
        """
        Grab all the variables passed by user (if any) and parse them to match the format specified
        by PEPhub API for query parameters.

        :param pep_variables: dict of query parameters
        :return: PEPHubClient variables transformed into string in correct format.
        """
        parsed_variables = []

        for variable_name, variable_value in pep_variables.items():
            parsed_variables.append(f"{variable_name}={variable_value}")
        return "?" + "&".join(parsed_variables)

    @staticmethod
    def _handle_pephub_response(pephub_response: requests.Response):
        """
        Check pephub response
        """
        decoded_response = PEPHubClient.decode_response(pephub_response)

        if pephub_response.status_code != ResponseStatusCodes.OK:
            raise ResponseError(message=json.loads(decoded_response).get("detail"))

        return decoded_response
