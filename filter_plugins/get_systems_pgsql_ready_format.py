class FilterModule(object):

    def filters(self):
        return {
            'get_systems_pgsql_ready_format': self.get_systems_pgsql_ready_format,
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


    def recordsToBeAdded(self,value,tokens,bp_id):
        retval=[]
        for key in value.keys():
          if ((self.missingInDB(tokens,value[key]['id'],bp_id) == False) and (value[key]['system_type'] == 'server')):
            sql_statement="'"+str(value[key]['label'])+"','"+str(bp_id)+"','"+str(value[key]['id']+"','"+value[key]['system_type'])+"'"
            retval.append(sql_statement)
        return retval

    def recordsTobeDeleted(self,value,tokens,bp_id):
        tokensTobeDeleted=[]
        for token in tokens:
           tokenExistsInRunningConfig=False
           for key in value.keys():
              if((value[key]['id'] == token[1]) and (bp_id == token[0])):
                 tokenExistsInRunningConfig=True
           if(tokenExistsInRunningConfig==False):      
              tokensTobeDeleted.append(token[1])   
        return tokensTobeDeleted 




        
    

    def get_systems_pgsql_ready_format(self, value, bp_id, queryResult):
        retval=[]
        tokens=self.tokenizeSQLoutput(queryResult)
        recordsToBeAdded=self.recordsToBeAdded(value,tokens,bp_id)
        recordsTobeDeleted=self.recordsTobeDeleted(value,tokens,bp_id)
        retval.append(recordsToBeAdded)
        retval.append(recordsTobeDeleted)
        #return tokens
        return retval       

