class FilterModule(object):

    def filters(self):
        return {
            'consolidate_port_raws_in_csv': self.consolidate_port_raws_in_csv,
        }
    

    def consolidate_port_raws_in_csv(self, value):
       retval=[]
       hostnameDict={}
       for column in value:
          if((column['generic host hostname'] in hostnameDict) == False):
             if(column['generic host hostname'] != ""):
                tempColumn={}
                tempColumn.update({'NEW DESCRIPTION': column['NEW DESCRIPTION']})
                tempColumn.update({'etherchannel': column['etherchannel']})
                tempColumn.update({'etherchannel tipi': column['etherchannel tipi']})
                tempColumn.update({'generic host hostname': column['generic host hostname']})        
                tempColumn.update({'port vlan': column['port vlan']})
                tempColumn.update({'seri no': column['seri no']})
                tempColumn.update({'tag': column['tag']})  
                tempColumn.update({'trunk allowed vlans': column['trunk allowed vlans']})
                tempColumn.update({'SPEED': column['SPEED']})
                sport = []
                sport.append({column['SWITCH']:column['PORT']})
                tempColumn.update({'switchport': sport})                                         
                hostnameDict.update({column['generic host hostname']: tempColumn})
          elif((column['generic host hostname'] in hostnameDict) == True):
             hostnameDict[column['generic host hostname']]['switchport'].append({column['SWITCH']:column['PORT']})
       retVal=[]
       for key in hostnameDict.keys():
          tmpVal=hostnameDict[key]
          retVal.append(tmpVal)
       return retVal

