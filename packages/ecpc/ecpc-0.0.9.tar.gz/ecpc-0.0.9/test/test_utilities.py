import pytest
from ecpc import utilities
from ecpc.configuration import ECPC_DIR, config


def test_valid_selection():
    utilities.valid_selection('eu-west-1', 't2.small')
    with pytest.raises(ValueError):
        result = utilities.valid_selection('xxxx', 't2.small')
    with pytest.raises(ValueError):
        result = utilities.valid_selection('eu-west-1', 'xxxx')
    
def test_nonexistent_uid():
    region = 'eu-west-1'
    uid = 'ABC123'
    assert utilities.get_instance_id(region, uid) is None
    assert utilities.get_security_group_id(region, uid) is None
    assert utilities.get_key_pair(region, uid) is None
    assert utilities.get_pem_file(ECPC_DIR, uid) is None

def test_security_group_functions():
    region = 'eu-west-1'
    uid = 'ABC123'
    result = utilities.create_security_group(region, uid)
    assert utilities.get_security_group_id(region, uid) is not None
    utilities.delete_security_group(region, uid)
    assert utilities.get_security_group_id(region, uid) is None
    
def test_key_pair_functions():
    region = 'eu-west-1'
    uid = 'ABC123'
    key_material = utilities.create_key_pair(region, uid)
    result = utilities.create_pem_file(ECPC_DIR, uid, key_material)
    assert utilities.get_key_pair(region, uid) is not None
    assert utilities.get_pem_file(ECPC_DIR, uid) is not None
    utilities.delete_key_pair(region, uid)
    utilities.delete_pem_file(ECPC_DIR, uid)
    assert utilities.get_key_pair(region, uid) is None
    assert utilities.get_pem_file(ECPC_DIR, uid) is None
    
def test_ami_from_source():
    region = 'eu-west-1'
    source = '099720109477/ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*'
    image_id = utilities.ami_from_source(region, source),
    assert image_id is not None

def test_get_username():
    username = utilities.get_username()
    assert username is not None
