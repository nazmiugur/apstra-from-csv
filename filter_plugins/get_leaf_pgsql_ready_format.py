class FilterModule(object):

    def filters(self):
        return {
            'get_leaf_pgsql_ready_format': self.get_leaf_pgsql_ready_format,
        }


        

    def tokenizeSQLoutput(self,queryResult):
       retval=[]
       for query in queryResult:
          line=query['row'].replace("(","").replace(")","")
          linetoken=line.split(",")
          retval.append(linetoken)
       return retval

    def missingInDB(self,tokens,rid,bp_id):
        retval=False
        for token in tokens:
           if((token[0] == bp_id) and (token[1] == rid)):
              retval=True
        return retval


    def get_disctint_leaf_list(self, value,bp_id):
       switch_dict={}
       retval=[]
       for switch in value:
          for port in switch:
             if(port['sw_id'] in switch_dict ):
                break
             else:
                switch_dict.update({port['sw_id']: port['sw_label']})
                leaf_entry=[]
#                sql_statement="'"+str(port['sw_id'])+"','"+str(port['sw_label'])+"','"+str(bp_id)+"','"+str(port['rack_id'])+"'"
                leaf_entry.append(str(port['sw_id']))
                leaf_entry.append(str(port['sw_label']))
                leaf_entry.append(str(bp_id))
                leaf_entry.append(str(port['rack_id']))
                if(port['sw_type']=='leaf'):
#                   retval.append(sql_statement)
                   retval.append(leaf_entry)
       return retval




    def recordsToBeAdded(self,value,tokens,bp_id):
        retval=[]
        leaves=self.get_disctint_leaf_list(value,bp_id)
        for leaf in leaves:
          if ((self.missingInDB(tokens,leaf[0],bp_id) == False) ):
            sql_statement="'"+str(leaf[0])+"','"+str(leaf[1])+"','"+str(bp_id)+"','"+str(leaf[3])+"'"
#            sql_statement="'"+str(value[key]['label'])+"','"+str(bp_id)+"','"+str(value[key]['id'])+"'"
            retval.append(sql_statement)
        return retval

    def recordsTobeDeleted(self,value,tokens,bp_id):
        tokensTobeDeleted=[]
        leaves=self.get_disctint_leaf_list(value,bp_id)
        for token in tokens:
           tokenExistsInRunningConfig=False
           for leaf in leaves:
              if((leaf[0] == token[1]) and (bp_id == token[0])):
                 tokenExistsInRunningConfig=True
           if(tokenExistsInRunningConfig==False):      
              tokensTobeDeleted.append(token[1])   
        return tokensTobeDeleted 




        
    

    def get_leaf_pgsql_ready_format(self, value, bp_id, queryResult):
        retval=[]
        tokens=self.tokenizeSQLoutput(queryResult)
        recordsToBeAdded=self.recordsToBeAdded(value,tokens,bp_id)
        recordsTobeDeleted=self.recordsTobeDeleted(value,tokens,bp_id)
        retval.append(recordsToBeAdded)
        retval.append(recordsTobeDeleted)
        return retval       

