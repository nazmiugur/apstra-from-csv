class FilterModule(object):

    def filters(self):
        return {
            'get_leafport_pgsql_ready_format': self.get_leafport_pgsql_ready_format,
        }


        

    def tokenizeSQLoutput(self,queryResult):
       retval=[]
       for query in queryResult:
          line=query['row'].replace('(',"").replace(')',"").replace('\"\"','')
          linetoken=line.split(",")
          retval.append(linetoken)
       return retval

    def missingInDB(self,tokens,interface_name,bp_id,interface_speed,interface_aep_id,sw_id):
        retval=True
        for token in tokens:
#          if((token[0] == interface_name) and (token[1] == bp_id) and (str(token[2]) == str(interface_speed)) and(token[3] == interface_aep_id) and (token[4] == sw_id)):
           if((token[0] == interface_name) and (token[1] == bp_id) and (token[2] == interface_speed)  and (token[3] == interface_aep_id) and (token[4] == sw_id)):
              retval=False
        return retval




    def recordsToBeAdded(self,value,tokens,bp_id):
        retval=[]
        for switch in value:
           for leafport in switch:  
              if ((self.missingInDB(tokens,leafport['interface_name'],bp_id,str(leafport['interface_speed'].replace(',','-')), leafport['interface_aep_id'], leafport['sw_id'])) == True):
                 sql_statement="'"+str(leafport['interface_name'])+"','"+str(leafport['interface_speed'].replace(',','-'))+"','"+str(bp_id)+"','"+str(leafport['interface_aep_id']+"','")+str(leafport['sw_id'])+"'"
                 retval.append(sql_statement)
        return retval

    def recordsTobeDeleted(self,value,tokens,bp_id):
        tokensTobeDeleted=[]
        for token in tokens:
           deleteToken=True
           for switch in value:
              for leafport in switch:
                 if((token[0] == leafport['interface_name']) and (token[1] == bp_id) and (token[2] == str(leafport['interface_speed'].replace(',','-')))  and (token[3] == leafport['interface_aep_id']) and (token[4] == str(leafport['sw_id']))):
                     deleteToken=False   
           if(deleteToken==True):
              tokensTobeDeleted.append(token)
        return tokensTobeDeleted 



        
    

    def get_leafport_pgsql_ready_format(self, value, bp_id, queryResult):
        retval=[]
        tokens=self.tokenizeSQLoutput(queryResult)
        recordsToBeAdded=self.recordsToBeAdded(value,tokens,bp_id)
        recordsTobeDeleted=self.recordsTobeDeleted(value,tokens,bp_id)
        retval.append(recordsToBeAdded)
#       retval.append(tokens)
        retval.append(recordsTobeDeleted)
        return retval       

