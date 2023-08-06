import os
import json
import grpc
from time import time
from datetime import date
from willowlabs.tools import tools, protobuffer_tools as pb_tools
from willowlabs.service_grpc.company_information import company_information_service_pb2 as pb2, company_information_service_pb2_grpc as pb2_grpc
from typing import Any, Optional, Union
from functools import wraps


def _check_jwt(f):
    @wraps(f)  # Needed to get the right function attributes and name
    def wrapped_function(self, *args, **kwargs):
        if self.jwt is None or self.jwt_expires is None or self.jwt_expires < time():
            self.get_json_web_token()
        return f(self, *args, *kwargs)

    return wrapped_function


class CompanyInformationClient:
    """
    Class to access Willow Labs API.
    :param configuration_path: The path of the configuration file.
    :param kwargs: Ekstra parameters. - Timeout, service_type, return_dict
    """

    def __init__(self, configuration_path: str, **kwargs: Any):
        self.configuration_path = configuration_path
        self.configuration = None
        self.service_type = kwargs.get("service_type", "production")
        self.credentials_info = None
        self.host = None
        self.issuer = None
        self.audiences = None
        self.jwt = None
        self.jwt_expires = None
        self.api_key = None
        self.timeout = kwargs.get("timeout", 60)        # Seconds
        self.scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        self.return_dict = kwargs.get("return_dict", False)




    def load_configuration(self):
        """
        Loads the config
        """
        self.configuration = tools.load_client_configuration(self.configuration_path)
        self.host = self.configuration["service"][self.service_type]["host"]
        self.issuer = self.configuration["authentication"]["issuer"]
        self.audiences = self.configuration["authentication"]["audiences"]
        self.api_key = self.configuration["service"][self.service_type]["api_key"]

    def load_credentials(self):
        if self.configuration is None:
            self.load_configuration()
        configuration = self.configuration["service"][self.service_type]
        path = configuration["service_account_credentials"]
        if path.endswith(".json") and os.path.exists(path):
            with open(path, "r") as fp:
                self.credentials_info = json.load(fp)
        else:
            raise FileNotFoundError(f"Unable to find credentials in path {path}.")

    def get_json_web_token(self):
        """
        Get the token
        :return:
        """
        if self.credentials_info is None:
            self.load_credentials()
        token, expires = tools.generate_jwt_token_from_impersonated_account(self.credentials_info, self.audiences,
                                                                            self.issuer)
        self.jwt = token
        self.jwt_expires = expires

    @_check_jwt
    def get_company_ownership(self, organisation_number: int, record_year: int, depth: int = 25, cutoff: float = 1.0,
                              top: int = 0) -> pb2.OwnershipResponse:
        """
        Get owners for a company.
        :param organisation_number: Organization number for the company the structure is needed for.
        :param record_year: The ownership year.
        :param depth: How deep
        :param cutoff: Minimum percentage of ownership for inclusion in result.
        :param top: The number of max elements returned (The top N owners).
        :return: The ownership structure.
        """
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.OwnershipRequest(organisation_number=organisation_number, record_year=record_year,
                                           depth=depth, cutoff=cutoff, top=top)
            ownership_information = stub.get_company_ownership(request, self.timeout, metadata=metadata)
        return ownership_information

    @_check_jwt
    def get_company_roles(self, organisation_number: int, query_date: date) -> pb2.RoleResponse:
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.RoleRequest(organisation_number=organisation_number,
                                      query_date=pb_tools.date_to_pb2_date(query_date))
            roles = stub.get_company_roles(request, self.timeout, metadata=metadata)
        return roles

    @_check_jwt
    def get_basic_company_information(self, organisation_number: int,
                                      query_date: Optional[date] = None) -> pb2.BasicCompanyInformationResponse:
        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.BasicCompanyInformationRequest(organisation_number=organisation_number,
                                                         query_date=pb_tools.date_to_pb2_date(query_date))
            results = stub.get_basic_company_information(request, self.timeout, metadata=metadata)
        return results

    @_check_jwt
    def get_company_signatory_information(self, organisation_number: int,
                                          authority_type: Union[str, int],
                                          query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        if isinstance(authority_type, str):
            try:
                authority_type = getattr(pb2.SignatoryAuthorityTypes, authority_type.upper())
            except AttributeError:
                raise ValueError(f"Unknown authority type '{authority_type}'. Authority type must be among "
                                 f"'POWER_OF_ATTORNEY', 'PROKURA', 'FULL_SIGNATORY_AUTHORITY', or 'SIGNATUR'.")

        if authority_type == pb2.SignatoryAuthorityTypes.UNKNOWN_AUTHORITY:
            raise ValueError(f"Authority type may not be UNKNOWN_AUTHORITY.")

        with grpc.secure_channel(self.host, grpc.ssl_channel_credentials()) as channel:
            stub = pb2_grpc.CompanyInformationStub(channel)
            metadata = [("authorization", f"Bearer {self.jwt}"), ("x-api-key", self.api_key)]
            request = pb2.SignatoryInformationRequest(organisation_number=organisation_number,
                                                      authority_type=authority_type,
                                                      query_date=pb_tools.date_to_pb2_date(query_date))
            results = stub.get_company_signatory_information(request, self.timeout, metadata=metadata)
        return results

    @_check_jwt
    def get_company_power_of_attorney(self, organisation_number: int,
                                      query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        """
        sadasd
        :param organisation_number: sds
        :param query_date: sdsa
        :return: sda
        """
        return self.get_company_signatory_information(organisation_number,
                                                      pb2.SignatoryAuthorityTypes.POWER_OF_ATTORNEY,
                                                      query_date=query_date)

    @_check_jwt
    def get_company_full_signatory_authority(self, organisation_number: int,
                                             query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        return self.get_company_signatory_information(organisation_number,
                                                      pb2.SignatoryAuthorityTypes.FULL_SIGNATORY_AUTHORITY,
                                                      query_date=query_date)

    @_check_jwt
    def get_company_prokura(self, organisation_number: int,
                            query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        return self.get_company_signatory_information(organisation_number, pb2.SignatoryAuthorityTypes.PROKURA,
                                                      query_date=query_date)

    @_check_jwt
    def get_company_signatur(self, organisation_number: int,
                             query_date: Optional[date] = None) -> pb2.SignatoryInformationResponse:
        return self.get_company_signatory_information(organisation_number, pb2.SignatoryAuthorityTypes.SIGNATUR,
                                                      query_date=query_date)
