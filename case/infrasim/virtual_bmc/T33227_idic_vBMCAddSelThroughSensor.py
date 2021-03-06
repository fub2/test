'''
*********************************************************
Copyright @ 2015 EMC Corporation All Rights Reserved
*********************************************************
'''
from case.CBaseCase import *
import re

class T33227_idic_vBMCAddSelThroughSensor(CBaseCase):

    def __init__(self):
        CBaseCase.__init__(self, self.__class__.__name__)

    def config(self):
        CBaseCase.config(self)
        self.enable_ipmi_console()

    def test(self):
        for obj_rack in self.stack.get_rack_list():
            for obj_node in obj_rack.get_node_list():
                self.log('INFO', 'Add sel into node {} of rack {} through sensor ...'.
                         format(obj_node.get_name(), obj_rack.get_name()))

                # Get product name from FRU data.
                ret, rsp = obj_node.get_bmc().ipmi.ipmitool_standard_cmd('fru print 0')
                # Test fail if this nodes ipmi can't response
                if ret != 0:
                    self.result(BLOCK, 'Node {} on rack {} fail to response ipmitool fru print'.
                                format(obj_node.get_name(), obj_rack.get_name()))
                    continue

                fru = {}
                for item in rsp.split('\n'):
                    key = item.split(': ')[0].strip()
                    value = item.split(': ')[-1].strip()
                    fru[key] = value

                try:
                    # Try to find the corresponding sensor id by product name from JSON file.
                    sensor_id = self.data[fru['Product Name']]

                except KeyError, e:
                    # If product name missing, block this case.
                    self.result(BLOCK,
                    """
                    KeyError: {}.
                    Please supplement product name of node ({}) and the corresponding sensor id in {}.json.
                    For more details, please read the document: https://infrasim.readthedocs.org/en/latest/
                    """
                                .format(e, e, self.__class__.__name__))

                else:

                    sensor_value = 1.00

                    # Add sel through sensor
                    ipmi_console = obj_node.ssh_ipmi_console
                    ipmi_console.send_command_wait_string(str_command='sensor value set {} {} {}'.
                                                          format(sensor_id, sensor_value, chr(13)),
                                                          wait='IPMI_SIM',
                                                          int_time_out=3,
                                                          b_with_buff=False)

                    time.sleep(3)

                    # Get sel by using ipmitool
                    ret, rsp = obj_node.get_bmc().ipmi.ipmitool_standard_cmd('sel list')
                    self.log('INFO', 'ret: {}'.format(ret))
                    self.log('INFO', 'rsp: \n{}'.format(rsp))

                    if ret != 0:
                        # Failed to get sel by using ipmitool
                        self.result(FAIL, 'Node {} on rack {} fail to add BMC sel through sensor, '
                                    'ipmitool return: {}, expect: 0, rsp: \n{}'.
                                    format(obj_node.get_name(), obj_rack.get_name(), ret, rsp))

                    else:
                        is_match = re.search("Pre-Init", rsp)

                        if is_match != None:
                            self.log('INFO', 'Get sel from vBMC: {}'.format(rsp))

                        else:
                            # Failed to add sel through sensor
                            self.result(FAIL, 'Nothing from vBMC. Node is {}, ipmi-console access: {}:{}'.
                                        format(obj_node.get_name(),
                                               obj_node.get_ip(),
                                               obj_node.get_port_ipmi_console()))

                time.sleep(1)

    def deconfig(self):
        self.log('INFO', 'Deconfig')
        CBaseCase.deconfig(self)
