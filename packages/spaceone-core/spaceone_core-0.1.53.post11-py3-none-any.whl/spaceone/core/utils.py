#!/usr/bin/env python3
import secrets
import uuid
from urllib.parse import urlparse

# import requests
import yaml


def generate_id(prefix: str = 'id', nbytes: int = 6) -> str:
    random_id = secrets.token_hex(nbytes)
    return f'{prefix}-{random_id}'


def random_string() -> str:
    return uuid.uuid4().hex


def load_yaml(yaml_str: str) -> dict:
    try:
        return yaml.load(yaml_str, Loader=yaml.Loader)

    except Exception:
        raise ValueError(f'YAML Load Error: {yaml_str}')


def load_yaml_from_file(yaml_file: str) -> dict:
    try:
        with open(yaml_file, 'r') as f:
            return load_yaml(f)
    except Exception:
        raise Exception(f'YAML Load Error: {yaml_file}')


def load_yaml_from_url(url: str):
    try:
        with requests.get(url) as ret:
            return load_yaml(ret.text)
    except Exception as e:
        raise Exception(f'Http call error: {url}. e={e}')


def parse_endpoint(endpoint: str) -> dict:
    try:
        o = urlparse(endpoint)
    except Exception:
        raise ValueError(f'Endpoint is invalid. ({endpoint})')

    return {
        'scheme': o.scheme,
        'hostname': o.hostname,
        'port': o.port,
        'path': o.path
    }


def parse_grpc_uri(uri: str) -> dict:
    try:
        endpoint_info = parse_endpoint(uri)

        if endpoint_info['scheme'] != 'grpc':
            raise ValueError(f'gRPC endpoint type is invalid. ({uri})')

        version, api_class, method = \
            filter(lambda x: x.strip() != '', endpoint_info['path'].split('/'))
    except Exception:
        raise ValueError(f'gRPC URI is invalid. ({uri})')

    return {
        'endpoint': f'{endpoint_info["hostname"]}:{endpoint_info["port"]}',
        'version': version,
        'api_class': api_class,
        'method': method
    }


def deep_merge(from_dict: dict, into_dict: dict) -> dict:
    for key, value in from_dict.items():
        if isinstance(value, dict):
            node = into_dict.setdefault(key, {})
            deep_merge(value, node)
        else:
            into_dict[key] = value

    return into_dict


def change_dict_value(data: dict, dotted_key: str, change_value, change_type='value') -> dict:
    # change_value = func or value(any type)
    if '.' in dotted_key:
        key, rest = dotted_key.split('.', 1)
        if key in data:
            if rest.startswith('[]') and isinstance(data[key], list):
                list_data = []
                for sub_data in data[key]:
                    if rest.strip() == '[]':
                        list_data.append(_change_value_by_type(change_type, sub_data, change_value))
                    else:
                        sub_rest = rest.split('.', 1)[1]
                        list_data.append(change_dict_value(sub_data, sub_rest, change_value, change_type))
                data[key] = list_data
            elif isinstance(data[key], dict):
                data[key] = change_dict_value(data[key], rest, change_value, change_type)
    else:
        if dotted_key in data:
            data[dotted_key] = _change_value_by_type(change_type, data[dotted_key], change_value)

    return data


def _change_value_by_type(change_type, original_value, change_value):
    if change_type == 'value':
        return change_value
    elif change_type == 'func':
        return change_value(original_value)
    else:
        return original_value


if __name__ == '__main__':
    pass
