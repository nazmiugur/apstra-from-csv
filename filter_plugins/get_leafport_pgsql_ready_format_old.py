class FilterModule(object):

    def filters(self):
        return {
            'get_leafport_pgsql_ready_format': self.get_leafport_pgsql_ready_format,
        }

    def get_leafport_pgsql_ready_format(self, value, bp_id):
       retval=[]
       for switch in value:
          for port in switch:
            speed=str(port['interface_speed']).replace(",","-")
            sql_statement="'"+str(port['interface_name'])+"','"+str(speed)+"','"+str(bp_id)+"','"+str(port['interface_aep_id'])+"','"+str(port['sw_id'])+"'"
            if(port['sw_type']=='leaf'):
                retval.append(sql_statement)
       return retval

