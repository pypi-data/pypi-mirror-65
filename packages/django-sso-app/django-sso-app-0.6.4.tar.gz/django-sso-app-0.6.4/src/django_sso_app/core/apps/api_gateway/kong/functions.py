# Boostable functions
#
# import pyximport
# pyximport.install()


def get_apigateway_consumer_id(sso_id: str) -> str:
    """
    Translates from kong consumer.username to sso_id
    :param sso_id:
    :return:
    """
    return str(sso_id).replace('-', '_')


def get_apigateway_sso_id(apigateway_user_id: str) -> str:
    """
    Translates from sso_id to kong consumer.username
    :param apigateway_user_id:
    :return:
    """
    return str(apigateway_user_id).replace('_', '-')


def get_apigateway_profile_groups_from_header(groups_header: str) -> list:
    """
    Extracts apigateway consumer groups from header
    :param groups_header:
    :return:
    """
    if groups_header not in [None, '']:
        return list(map(str.strip, groups_header.split(',')))

    return []
