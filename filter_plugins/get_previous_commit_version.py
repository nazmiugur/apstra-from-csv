class FilterModule(object):

    def filters(self):
        return {
            'get_revisions_pgsql_ready_format': self.get_revisions_pgsql_ready_format,
        }

    def get_revisions_pgsql_ready_format(self, value, bp_id):
        retval=[]
        for item in value:
           sql_statement="'"+str(item['user'])+"','"+str(bp_id)+"','"+str(item['revision_id'])+"'"
           retval.append(sql_statement)
        return retval       

