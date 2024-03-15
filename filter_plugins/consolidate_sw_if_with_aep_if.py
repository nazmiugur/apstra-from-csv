class FilterModule(object):

    def filters(self):
        return {
            'consolidate_sw_if_with_aep_if': self.consolidate_sw_if_with_aep_if,
        }
    

    def convAepIftoBareIf(self, aep_portname):
      retval=""
      try: 
         portname=aep_portname.split(" -> ")[0]
         retval=portname
      except:
         print("aep_portname is not in the expected format")
         print(aep_portname)
      return retval

    def getRackIDandLabel(self, sw_name, aep_if_list):
       retval=[]
       for aep_if in aep_if_list:
          if(sw_name == aep_if['sw_label']):
             retval.append(aep_if['rack_id'])
             retval.append(aep_if['rack_label'])
             break
       return retval




    def findIndex(self, sw_if_list, portname, sw_id):
       switch_index=0
       port_index=0
       retval=[]
       for switch in sw_if_list:
          port_index=0
          for port in switch:
             if((port['sw_id']==sw_id) and (port['interface_name'] == portname)):
               retval.append(switch_index)
               retval.append(port_index)
             else:
               port_index=port_index+1
          switch_index=switch_index+1
       return retval

    def findPortSpeed(self, if_id, ifsinfo):
       retval=""
       for interface in ifsinfo['items']:
          if(interface['iface']['id'] == if_id):
             retval=interface['link']['speed'].split("G")[0]
       return retval
       



    def consolidate_sw_if_with_aep_if(self, value):
       aep_if_list=value['aep_ifs']
       sw_if=value['sw_if']
       if 'ifsinfo' in value:
          ifsinfo=value['ifsinfo']
       for aep_if in aep_if_list:
          portname=self.convAepIftoBareIf(aep_if['interface_aep_label'])
          indexes=self.findIndex(sw_if,portname, aep_if['sw_id'])
          if(len(indexes)==2):
             print(sw_if[indexes[0]][indexes[1]])
             sw_if[indexes[0]][indexes[1]].update({"rack_id": aep_if['rack_id']})
             sw_if[indexes[0]][indexes[1]].update({"rack_label": aep_if['rack_label']})
             if 'ifsinfo' in value:
                speed=self.findPortSpeed(aep_if['interface_aep_id'], ifsinfo)
                sw_if[indexes[0]][indexes[1]].update({"interface_speed":speed})
             sw_if[indexes[0]][indexes[1]].update({"interface_aep_id": aep_if['interface_aep_id']})
             sw_if[indexes[0]][indexes[1]].update({"interface_aep_label": aep_if['interface_aep_label']})
       for switch in sw_if:
           for port in switch:
              rackinfo=self.getRackIDandLabel(port['sw_label'], aep_if_list)
              if(len(rackinfo)==2):
                port.update({"rack_id": rackinfo[0]})
                port.update({"rack_label": rackinfo[1]})
              else:
                port.update({"rack_id": ""})
                port.update({"rack_label": ""})
              port.update({"connected_to_id": ""})
              if 'ifsinfo' in value:
                speed=self.findPortSpeed(aep_if['interface_aep_id'], ifsinfo)  
              port.update({"connected_to_type": ""})
              port.update({"connected_to_label": ""})
       if 'ifsinfo' in value:
          ifsinfo=value['ifsinfo']
          for iface in ifsinfo['items']:
             portname=iface['iface']['if_name']
             sw_id=iface['system']['id']
             sw_name=iface['system']['label']
             connected_to_id=iface['remote_system']['id']
             connected_to_type=iface['remote_system']['type']
             connected_to_label=iface['remote_system']['label']
             indexes=self.findIndex(sw_if,portname, sw_id)
             if(len(indexes)==2):
                rackinfo=self.getRackIDandLabel(sw_name, aep_if_list)
                if(len(rackinfo)==2):
                   sw_if[indexes[0]][indexes[1]].update({"rack_id": rackinfo[0]})
                   sw_if[indexes[0]][indexes[1]].update({"rack_label": rackinfo[1]})
                if(connected_to_id !=""):
                   speed=connected_to_id=iface['link']['speed'].split("G")[0]
                   sw_if[indexes[0]][indexes[1]].update({"speed": speed})
                sw_if[indexes[0]][indexes[1]].update({"connected_to_id": connected_to_id})
                sw_if[indexes[0]][indexes[1]].update({"connected_to_type": connected_to_type})
                sw_if[indexes[0]][indexes[1]].update({"connected_to_label": connected_to_label})
       return sw_if
           
