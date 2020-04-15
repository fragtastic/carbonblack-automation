# !/usr/bin/env python3
import logging
import argparse
from cbapi import CbPSCBaseAPI
from cbapi.psc import Device
import mappings


def assign_device(device):
    metadict = get_meta_dict(device)
    if 'AD_LDAP' in metadict:
        logging.debug(metadict['AD_LDAP'])
        return assign_device_by_ad(device, metadict)
    else:
        return assign_device_by_os(device)

def assign_device_by_ad(device, metadict):
    logging.debug(metadict)
    if mappings.OrganizationalUnits.DOMAIN_CONTROLLER in metadict['AD_LDAP']:
        device.update_policy(mappings.policy.DOMAIN_CONTROLLERS)
        return 1
    else:
        logging.info(f'Could not assign device {device.id} by AD. Falling back to OS matching.')
        return assign_device_by_os(device)
    return 0

def assign_device_by_os(device):
    oldPolicy = device.policy_id
    newPolicy = device.policy_id
    if device.os_version.startswith(mappings.OperatingSystem.linux):
        newPolicy = mappings.policy.LINUX # 'Linux'
    elif device.os_version.startswith(mappings.OperatingSystem.macos):
        newPolicy = mappings.policy.MACOS # 'MacOS'
    elif device.os_version.startswith(mappings.OperatingSystem.windows_workstation):
        newPolicy = mappings.policy.WINDOWS_WORKSTATION # 'Windows Workstation'
    elif device.os_version.startswith(mappings.OperatingSystem.windows_server):
        newPolicy = mappings.policy.WINDOWS_SERVER # 'Windows Server'
    else:
        newPolicy = mappings.policy.UNKNOWN # 'Unknown'
    if oldPolicy != newPolicy:
        logging.info(f'Changing policy for device deviceID:{device.id} from "{oldPolicy}" to "{newPolicy}"')
        device.update_policy(newPolicy)
        return 1
    else:
        return 0

def get_meta_dict(device):
    metadict = {}
    for metadata in device.device_meta_data_item_list:
        metadict[metadata['key_name']] = metadata['key_value']
    return metadict

def run_assign_devices(policy_ids=[mappings.policy.STANDARD, mappings.policy.UNKNOWN]):
    cbapi = CbPSCBaseAPI(profile='psc')
    devices = cbapi.select(Device).set_status(['REGISTERED']).set_policy_ids(policy_ids)
    logging.info(f'Number of devices found {len(devices)}')
    devices_assigned = 0
    for device in devices:
        try:
            devices_assigned += assign_device(device)
        except Exception as e:
            logging.error(e)
    logging.info(f'Number of devices assigned {devices_assigned}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log-level', dest='logLevel', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level')
    args = parser.parse_args()

    if args.logLevel:
        logging.basicConfig(level=getattr(logging, args.logLevel))

    run_assign_devices()
