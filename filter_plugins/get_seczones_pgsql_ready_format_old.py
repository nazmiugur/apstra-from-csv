class FilterModule(object):

    def filters(self):
        return {
            'get_seczones_pgsql_ready_format': self.get_seczones_pgsql_ready_format,
        }

    def get_seczones_pgsql_ready_format(self, value, bp_id):
        retval=[]
        for key in value.keys():
           sql_statement="'"+str(value[key]['label'])+"','"+str(bp_id)+"','"+str(value[key]['id'])+"'"
           retval.append(sql_statement)
        return retval       

