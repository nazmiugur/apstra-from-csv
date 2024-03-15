class FilterModule(object):

    def filters(self):
        return {
            'get_leaf_pgsql_ready_format': self.get_leaf_pgsql_ready_format,
        }

    def get_leaf_pgsql_ready_format(self, value, bp_id):
       switch_dict={}
       retval=[]
       for switch in value:
          for port in switch:
             if(port['sw_id'] in switch_dict ):
                break
             else:
                switch_dict.update({port['sw_id']: port['sw_label']})
                sql_statement="'"+str(port['sw_id'])+"','"+str(port['sw_label'])+"','"+str(bp_id)+"','"+str(port['rack_id'])+"'"
                if(port['sw_type']=='leaf'):
                   retval.append(sql_statement)
       return retval

