"""
Main interface for accessanalyzer service.

Usage::

    import boto3
    from mypy_boto3.accessanalyzer import (
        AccessAnalyzerClient,
        Client,
        ListAnalyzedResourcesPaginator,
        ListAnalyzersPaginator,
        ListArchiveRulesPaginator,
        ListFindingsPaginator,
        )

    session = boto3.Session()

    client: AccessAnalyzerClient = boto3.client("accessanalyzer")
    session_client: AccessAnalyzerClient = session.client("accessanalyzer")

    list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
    list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
    list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
"""
from mypy_boto3_accessanalyzer.client import AccessAnalyzerClient, AccessAnalyzerClient as Client
from mypy_boto3_accessanalyzer.paginator import (
    ListAnalyzedResourcesPaginator,
    ListAnalyzersPaginator,
    ListArchiveRulesPaginator,
    ListFindingsPaginator,
)


__all__ = (
    "AccessAnalyzerClient",
    "Client",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
)
