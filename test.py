# Тесты
import pytest
from main import extract_path, extract_bind_addresses, create_collection


def test_extract_path():
    
    assert extract_path('--path.settings C:\\Users\\Administrator\\ELK\\logstash-8.11.1\\config --another.key qweqweqwe') == \
           'C:\\Users\\Administrator\\ELK\\logstash-8.11.1\\config'
    
    assert extract_path('--path.settings "C:\\Program Files\\Elastic" --another.key qweqweqwe') == \
           'C:\\Program Files\\Elastic'
    
    assert extract_path('--path.settings C:\\Program Files\\Elastic --another.key qweqweqwe') == \
           'C:\\Program Files\\Elastic'

def test_extract_path_no_match():
    assert extract_path('No path settings found') is None

def test_extract_bind_addresses():
    config = """
    listen tcp_public
    mode tcp
    bind 10.0.210.252:9000,10.0.210.253:9000
    bind ipv4@172.30.148.13:443 ssl crt /etc/haproxy/site.pem
    bind ipv6@:80
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy
    bind 2a00:f920:192::233:80
    server tcpsrv0 192.168.1.101:9999
    use_backend dghj
    """

    expected = [
        '10.0.210.252:9000',
        '10.0.210.253:9000',
        'ipv4@172.30.148.13:443',
        'ipv6@:80',
        '2a00:f920:192::233:80'
    ]

    assert extract_bind_addresses(config) == expected

def test_extract_bind_addresses_empty():
    assert extract_bind_addresses("") == []

def test_create_collection():
    bind_addresses = [
        '10.0.210.252:9000',
        '10.0.210.253:9000',
        'ipv4@172.30.148.13:443',
        'ipv6@:80',
        '2a00:f920:192::233:80'
    ]

    expected = [
        {'IP': '10.0.210.252', 'Type': 'ipv4', 'Port': 9000},
        {'IP': '10.0.210.253', 'Type': 'ipv4', 'Port': 9000},
        {'IP': '172.30.148.13', 'Type': 'ipv4', 'Port': 443},
        {'IP': '::', 'Type': 'ipv6', 'Port': 80},
        {'IP': '2a00:f920:192::233', 'Type': 'ipv6', 'Port': 80}
    ]

    assert create_collection(bind_addresses) == expected

def test_create_collection_empty():
    assert create_collection([]) == []