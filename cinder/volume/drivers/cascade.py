#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Driver for cascaded cinder service.

"""

import os
import socket

from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import excutils
from oslo_utils import importutils
from oslo_utils import units
#import six

from cinder.brick.local_dev import lvm as lvm
from cinder import exception
from cinder.i18n import _, _LE, _LI, _LW
from cinder.image import image_utils
from cinder import interface
from cinder import objects
from cinder import utils
from cinder.volume import driver
from cinder.volume import utils as volutils

LOG = logging.getLogger(__name__)

volume_opts = [
    cfg.StrOpt('auth_url',
               default=None,
               help='auth_url of keystone that API calls are cascaded to.'),
    cfg.StrOpt('project_domain_name',
               default='Default',
               help=''),
    cfg.StrOpt('project_name',
               default='service',
               help=''),
    cfg.StrOpt('user_domain_name',
               default='Default',
               help=''),
    cfg.StrOpt('username',
               default=None,
               help='username for the cascaded Cinder.'),
    cfg.StrOpt('password',
               default=None,
               help='password for the cascaded Cinder.'),
    cfg.StrOpt('auth_type',
               default='',
               help='password for the cascaded Cinder.'),
    cfg.StrOpt('os_region_name',
               default=None,
               help='Region name.'),
    cfg.StrOpt('service_type',
               default='volumev2',
               help=''),
    cfg.StrOpt('service_name',
               default='cinderv2',
               help=''),
    cfg.StrOpt('insterface',
               default='publicURL',
               help=''),
    cfg.StrOpt('cascaded_storage_az',
               default=None,
               help='')
]

##[cinder-1]
##
##auth_uri = http://192.168.31.91:5000
##project_domain_name = Default
##project_name = service
##user_domain_name = Default
##password = stack
##username = cinder
##auth_url = http://192.168.31.91:35357
##auth_type = password
##
##os_region_name = 'RegionOne'
##service_type = 'volumev2'
##service_name = 'cinderv2'
##insterface = 'publicURL'
###storage_availability_zone = ''
##volume_driver = cinder.volume.drivers.cascade.CinderCascadeDriver
##volume_backend_name = cinder-1


CONF = cfg.CONF
CONF.register_opts(volume_opts)


@interface.volumedriver
class CinderCascadeDriver(driver.VolumeDriver):
    """Cascading Cinder API calls to other cloud."""

    VERSION = '0.0.1'

    def __init__(self, *args, **kwargs) :
        LOG.debug('cascade: __init__() called.')
        super(CinderCascadeDriver, self).__init__(*args, **kwargs)
        #TODO(thatsdone):
        #add initial cascaded cinder connection check.
        self.configuration.append_config_values(volume_opts)
        self.backend_name = self.configuration.safe_get('volume_backend_name')

    def check_for_setup_error(self):
        LOG.debug('cascade: check_for_setup_error() called.')

    def get_volume_stats(self, refresh=False):
        """Get volume status.

        If 'refresh' is True, run update the stats first.
        """
        LOG.debug('cascade: get_volume_stats() called.')
        data = {}
        if refresh:
            data["volume_backend_name"] = 'cinder-1' # self.backend_name
            data["vendor_name"] = 'Open Source'
            data["storage_protocol"] = 'iSCSI'
            data["pools"] = [{'pool_name': 'cinder-1',
                             'free_capacity_gb': 100.0}]
            self._stats = data
            # capacity etc.


#{u'filter_function': None, u'goodness_function': None, u'volume_backend_name': u'lvmdriver-1', u'driver_version': u'3.0.0', u'sparse_copy_volume': False,
#
# u'pools': [
#     {u'pool_name': u'lvmdriver-1',
#      u'filter_function': None,
#      u'goodness_function': None,
#      u'total_volumes': 0,
#      u'multiattach': True,
#      u'provisioned_capacity_gb': 0.0,
#      u'allocated_capacity_gb': 0,
#      u'thin_provisioning_support': False,
#      u'free_capacity_gb': 10.01,
##      u'location_info': u'LVMVolumeDriver:xenial:stack-volumes-lvmdriver-1:default:0',
#      u'total_capacity_gb': 10.01,
#      u'thick_provisioning_support': True,
#      u'reserved_percentage': 0,
#      u'QoS_support': False,
#      u'max_over_subscription_ratio': 1.0}
# ]
# , u'vendor_name': u'Open Source', u'storage_protocol': u'iSCSI'}
#
#
#            
#2016-09-20 01:28:01.651 DEBUG cinder.scheduler.host_manager [req-3a3da104-3e7e-4d5a-adcd-24e3d18dd202 None] Received volume service update from xenial@lvmdriver-1: {u'filter_function': None, u'goodness_function': None, u'volume_backend_name': u'lvmdriver-1', u'driver_version': u'3.0.0', u'sparse_copy_volume': False, u'pools': [{u'pool_name': u'lvmdriver-1', u'filter_function': None, u'goodness_function': None, u'total_volumes': 0, u'multiattach': True, u'provisioned_capacity_gb': 0.0, u'allocated_capacity_gb': 0, u'thin_provisioning_support': False, u'free_capacity_gb': 10.01, u'location_info': u'LVMVolumeDriver:xenial:stack-volumes-lvmdriver-1:default:0', u'total_capacity_gb': 10.01, u'thick_provisioning_support': True, u'reserved_percentage': 0, u'QoS_support': False, u'max_over_subscription_ratio': 1.0}], u'vendor_name': u'Open Source', u'storage_protocol': u'iSCSI'} update_service_capabilities /opt/stack/cinder/cinder/scheduler/host_manager.py:450

        return data
        
    def initialize_connection(self, volume, connector, **kwargs):
        LOG.debug('cascade: initialize_connection() called.')
        return {
            'driver_volume_type': 'cascade',
            'data': {'device_path': 'dummy_provider_location'},
        }
        return None

    def create_volume(self, volume):
        LOG.debug('cascade: create_volume() called.')
         
    def delete_volume(self, volume):
        LOG.debug('cascade: delete_volume called.')

    def ensure_export(self, context, volume): 
        LOG.debug('cascade: ensure_esport() called.')

    def get_manageable_volumes(self, cinder_volumes, marker, limit, offset,
                               sort_keys, sort_dirs):
        LOG.debug('cascade: get_manageable_volumes() called.')
        entries = []
        return volutils.paginate_entries_list(entries, marker, limit, offset,
                                              sort_keys, sort_dirs)


        
#########################################s
#stack@xenial:/opt/stack/cinder/cinder/volume/drivers$ egrep -A 4 NotImplemented  ../driver.py   | grep def" "    | awk '{printf("# %s\n", $0);}'
#     def validate_connector_has_setting(connector, setting):
#     def ensure_export(self, context, volume):
#     def unmanage(self, volume):
#     def freeze_backend(self, context):
#     def get_replication_updates(self, context):
#     def create_group(self, context, group):
#     def delete_group(self, context, group, volumes):
#     def update_group(self, context, group,
#     def create_group_from_src(self, context, group, volumes,
#     def create_group_snapshot(self, context, group_snapshot, snapshots):
#     def delete_group_snapshot(self, context, group_snapshot, snapshots):
#     def create_volume(self, volume):
#     def create_volume_from_snapshot(self, volume, snapshot):
#     def create_replica_test_volume(self, volume, src_vref):
#     def delete_volume(self, volume):
#     def create_snapshot(self, snapshot):
#     def delete_snapshot(self, snapshot):
#     def local_path(self, volume):
#     def clear_download(self, context, volume):
#     def manage_existing(self, volume, existing_ref):
#     def manage_existing_get_size(self, volume, existing_ref):
#     def get_manageable_volumes(self, cinder_volumes, marker, limit, offset,
#     def unmanage(self, volume):
#     def manage_existing_snapshot_get_size(self, snapshot, existing_ref):
#     def get_manageable_snapshots(self, cinder_snapshots, marker, limit, offset,
#     def unmanage_snapshot(self, snapshot):
#     def promote_replica(self, context, volume):
#     def ensure_export(self, context, volume):
#     def create_export(self, context, volume, connector):
#     def create_export_snapshot(self, context, snapshot, connector):
#     def remove_export(self, context, volume):
#     def remove_export_snapshot(self, context, snapshot):
#     def initialize_connection(self, volume, connector, **kwargs):
#     def initialize_connection_snapshot(self, snapshot, connector, **kwargs):
#     def create_consistencygroup_from_src(self, context, group, volumes,
#     def delete_consistencygroup(self, context, group, volumes):
#     def update_consistencygroup(self, context, group,
#     def create_cgsnapshot(self, context, cgsnapshot, snapshots):
#     def delete_cgsnapshot(self, context, cgsnapshot, snapshots):
#     def clone_image(self, volume, image_location, image_id, image_meta,
#     def validate_connector(self, connector):
#stack@xenial:/opt/stack/cinder/cinder/volume/drivers$
