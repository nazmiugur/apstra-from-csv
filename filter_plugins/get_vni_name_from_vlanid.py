class FilterModule(object):

    def filters(self):
        return {
            'get_vni_name_from_vlanid': self.get_vni_name_from_vlanid,
        }

    def get_vni_name_from_vlanid(self, value, vlanid):
        for vni in value:
           if(vni['vlan_id'] == str(vlanid)):
             return vni['name']
            
