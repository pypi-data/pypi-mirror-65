"""
Main interface for servicediscovery service client

Usage::

    import boto3
    from mypy_boto3.servicediscovery import ServiceDiscoveryClient

    session = boto3.Session()

    client: ServiceDiscoveryClient = boto3.client("servicediscovery")
    session_client: ServiceDiscoveryClient = session.client("servicediscovery")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, Type, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_servicediscovery.paginator import (
    ListInstancesPaginator,
    ListNamespacesPaginator,
    ListOperationsPaginator,
    ListServicesPaginator,
)
from mypy_boto3_servicediscovery.type_defs import (
    CreateHttpNamespaceResponseTypeDef,
    CreatePrivateDnsNamespaceResponseTypeDef,
    CreatePublicDnsNamespaceResponseTypeDef,
    CreateServiceResponseTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeregisterInstanceResponseTypeDef,
    DiscoverInstancesResponseTypeDef,
    DnsConfigTypeDef,
    GetInstanceResponseTypeDef,
    GetInstancesHealthStatusResponseTypeDef,
    GetNamespaceResponseTypeDef,
    GetOperationResponseTypeDef,
    GetServiceResponseTypeDef,
    HealthCheckConfigTypeDef,
    HealthCheckCustomConfigTypeDef,
    ListInstancesResponseTypeDef,
    ListNamespacesResponseTypeDef,
    ListOperationsResponseTypeDef,
    ListServicesResponseTypeDef,
    NamespaceFilterTypeDef,
    OperationFilterTypeDef,
    RegisterInstanceResponseTypeDef,
    ServiceChangeTypeDef,
    ServiceFilterTypeDef,
    UpdateServiceResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ServiceDiscoveryClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    CustomHealthNotFound: Type[Boto3ClientError]
    DuplicateRequest: Type[Boto3ClientError]
    InstanceNotFound: Type[Boto3ClientError]
    InvalidInput: Type[Boto3ClientError]
    NamespaceAlreadyExists: Type[Boto3ClientError]
    NamespaceNotFound: Type[Boto3ClientError]
    OperationNotFound: Type[Boto3ClientError]
    ResourceInUse: Type[Boto3ClientError]
    ResourceLimitExceeded: Type[Boto3ClientError]
    ServiceAlreadyExists: Type[Boto3ClientError]
    ServiceNotFound: Type[Boto3ClientError]


class ServiceDiscoveryClient:
    """
    [ServiceDiscovery.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.can_paginate)
        """

    def create_http_namespace(
        self, Name: str, CreatorRequestId: str = None, Description: str = None
    ) -> CreateHttpNamespaceResponseTypeDef:
        """
        [Client.create_http_namespace documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_http_namespace)
        """

    def create_private_dns_namespace(
        self, Name: str, Vpc: str, CreatorRequestId: str = None, Description: str = None
    ) -> CreatePrivateDnsNamespaceResponseTypeDef:
        """
        [Client.create_private_dns_namespace documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_private_dns_namespace)
        """

    def create_public_dns_namespace(
        self, Name: str, CreatorRequestId: str = None, Description: str = None
    ) -> CreatePublicDnsNamespaceResponseTypeDef:
        """
        [Client.create_public_dns_namespace documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_public_dns_namespace)
        """

    def create_service(
        self,
        Name: str,
        NamespaceId: str = None,
        CreatorRequestId: str = None,
        Description: str = None,
        DnsConfig: DnsConfigTypeDef = None,
        HealthCheckConfig: HealthCheckConfigTypeDef = None,
        HealthCheckCustomConfig: HealthCheckCustomConfigTypeDef = None,
    ) -> CreateServiceResponseTypeDef:
        """
        [Client.create_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.create_service)
        """

    def delete_namespace(self, Id: str) -> DeleteNamespaceResponseTypeDef:
        """
        [Client.delete_namespace documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.delete_namespace)
        """

    def delete_service(self, Id: str) -> Dict[str, Any]:
        """
        [Client.delete_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.delete_service)
        """

    def deregister_instance(
        self, ServiceId: str, InstanceId: str
    ) -> DeregisterInstanceResponseTypeDef:
        """
        [Client.deregister_instance documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.deregister_instance)
        """

    def discover_instances(
        self,
        NamespaceName: str,
        ServiceName: str,
        MaxResults: int = None,
        QueryParameters: Dict[str, str] = None,
        HealthStatus: Literal["HEALTHY", "UNHEALTHY", "ALL"] = None,
    ) -> DiscoverInstancesResponseTypeDef:
        """
        [Client.discover_instances documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.discover_instances)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.generate_presigned_url)
        """

    def get_instance(self, ServiceId: str, InstanceId: str) -> GetInstanceResponseTypeDef:
        """
        [Client.get_instance documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_instance)
        """

    def get_instances_health_status(
        self,
        ServiceId: str,
        Instances: List[str] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> GetInstancesHealthStatusResponseTypeDef:
        """
        [Client.get_instances_health_status documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_instances_health_status)
        """

    def get_namespace(self, Id: str) -> GetNamespaceResponseTypeDef:
        """
        [Client.get_namespace documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_namespace)
        """

    def get_operation(self, OperationId: str) -> GetOperationResponseTypeDef:
        """
        [Client.get_operation documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_operation)
        """

    def get_service(self, Id: str) -> GetServiceResponseTypeDef:
        """
        [Client.get_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.get_service)
        """

    def list_instances(
        self, ServiceId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListInstancesResponseTypeDef:
        """
        [Client.list_instances documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_instances)
        """

    def list_namespaces(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[NamespaceFilterTypeDef] = None,
    ) -> ListNamespacesResponseTypeDef:
        """
        [Client.list_namespaces documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_namespaces)
        """

    def list_operations(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[OperationFilterTypeDef] = None,
    ) -> ListOperationsResponseTypeDef:
        """
        [Client.list_operations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_operations)
        """

    def list_services(
        self,
        NextToken: str = None,
        MaxResults: int = None,
        Filters: List[ServiceFilterTypeDef] = None,
    ) -> ListServicesResponseTypeDef:
        """
        [Client.list_services documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.list_services)
        """

    def register_instance(
        self,
        ServiceId: str,
        InstanceId: str,
        Attributes: Dict[str, str],
        CreatorRequestId: str = None,
    ) -> RegisterInstanceResponseTypeDef:
        """
        [Client.register_instance documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.register_instance)
        """

    def update_instance_custom_health_status(
        self, ServiceId: str, InstanceId: str, Status: Literal["HEALTHY", "UNHEALTHY"]
    ) -> None:
        """
        [Client.update_instance_custom_health_status documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_instance_custom_health_status)
        """

    def update_service(
        self, Id: str, Service: ServiceChangeTypeDef
    ) -> UpdateServiceResponseTypeDef:
        """
        [Client.update_service documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Client.update_service)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Paginator.ListInstances documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Paginator.ListInstances)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_namespaces"]) -> ListNamespacesPaginator:
        """
        [Paginator.ListNamespaces documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Paginator.ListNamespaces)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_operations"]) -> ListOperationsPaginator:
        """
        [Paginator.ListOperations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Paginator.ListOperations)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Paginator.ListServices documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.37/reference/services/servicediscovery.html#ServiceDiscovery.Paginator.ListServices)
        """
