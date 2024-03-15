class FilterModule(object):

    def filters(self):
        return {
            'flatten_filtered_managed_devices': self.flatten_filtered_managed_devices,
        }

    def flatten_filtered_managed_devices(self, value):
       retval=[]
       for device in value['items']:
          devports=[]
          for interface in device['DP']['ports']:
             trindex=len(interface['transformations'])-1
             trindex=0
             transient_item={}
             transient_item.update({"interface_name": interface['transformations'][trindex]['interfaces'][0]['name']})
             speed=""
             for transformation in interface['transformations']:
                speedval = transformation['interfaces'][0]['speed']['value']
                speed= str(speed)+","+str(speedval)
             transient_item.update({"interface_speed": str(speed[1:]) })
             transient_item.update({"sw_id": device['system']['id']})
             transient_item.update({"sw_label": device['system']['label']})
             transient_item.update({"sw_type": device['system']['role']})
             transient_item.update({"interface_aep_id": ""})
             transient_item.update({"interface_aep_label": ""})
             transient_item.update({"rack_id": ""})
             transient_item.update({"rack_label": ""})
             devports.append(transient_item)
          retval.append(devports)
       return retval
