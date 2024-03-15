class FilterModule(object):

    def filters(self):
        return {
            'get_racks_pgsql_ready_format_old': self.get_racks_pgsql_ready_format_old,
        }

    def get_racks_pgsql_ready_format_old(self, value, bp_id):
       rack_dict={}
       retval=[]
       for switch in value:
          for port in switch:
             if(port['rack_id'] in rack_dict ):
                break
             else:
                rack_dict.update({port['rack_id']: port['rack_label']})
                sql_statement="'"+str(port['rack_label'])+"','"+str(bp_id)+"','"+str(port['rack_id'])+"'"
                if(port['sw_type']=='leaf'):
                   retval.append(sql_statement)
       return retval

