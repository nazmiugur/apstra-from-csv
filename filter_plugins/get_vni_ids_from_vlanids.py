class FilterModule(object):

    def filters(self):
        return {
            'get_vni_names_from_vlanids': self.get_vni_names_from_vlanids,
        }

    def get_vni_names_from_vlanids(self, value, vlanlist):
        retval=[]
        for vlan in vlanlist:
           for vni in value:
              if(vni['vlan_id'] == str(vlan)):
                 retval.append("Tagged VxLAN '"+ vni['name']+"'")
        return retval
            
