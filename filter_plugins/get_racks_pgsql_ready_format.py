class FilterModule(object):

    def filters(self):
        return {
            'get_racks_pgsql_ready_format': self.get_racks_pgsql_ready_format,
        }


        

    def tokenizeSQLoutput(self,queryResult):
       retval=[]
       for query in queryResult:
          line=query['row'].replace("(","").replace(")","")
          linetoken=line.split(",")
          retval.append(linetoken)
       return retval

    def missingInDB(self,tokens,rid,bp_id):
        retval=True
        for token in tokens:
           if((token[0] == bp_id) and (token[1] == rid)):
              retval=False
        return retval


    def get_disctint_rack_list(self, value,bp_id):
       rack_dict={}
       retval=[]
       for switch in value:
          for port in switch:
             if(port['rack_id'] in rack_dict ):
                break
             else:
                rack_dict.update({port['rack_id']: str(port['rack_label'])+'rack'})
                if(port['rack_id'] !=''):
                   rack_entry=[]
                   rack_entry.append(str(port['rack_id']))
                   rack_entry.append(str(port['rack_label']))
                   rack_entry.append(str(bp_id))
                   retval.append(rack_entry)
       return retval




    def recordsToBeAdded(self,value,tokens,bp_id):
        retval=[]
        racks=self.get_disctint_rack_list(value,bp_id)
        for rack in racks:
          if ((self.missingInDB(tokens,rack[0],bp_id) == True) ):
            sql_statement="'"+str(rack[1])+"','"+str(bp_id)+"','"+str(rack[0])+"'"
            retval.append(sql_statement)
        return retval

    def recordsTobeDeleted(self,value,tokens,bp_id):
        tokensTobeDeleted=[]
        racks=self.get_disctint_rack_list(value,bp_id)
        for token in tokens:
           tokenExistsInRunningConfig=False
           for rack in racks:
              if((rack[0] == token[1])):
                 tokenExistsInRunningConfig=True
           if(tokenExistsInRunningConfig==False):      
             #tokensTobeDeleted.append(token[1])   
              tokensTobeDeleted.append(token[1])
        return tokensTobeDeleted 




        
    

    def get_racks_pgsql_ready_format(self, value, bp_id, queryResult):
        retval=[]
        tokens=self.tokenizeSQLoutput(queryResult)
        recordsToBeAdded=self.recordsToBeAdded(value,tokens,bp_id)
        recordsTobeDeleted=self.recordsTobeDeleted(value,tokens,bp_id)
        retval.append(recordsToBeAdded)
        retval.append(recordsTobeDeleted)
        return retval       

