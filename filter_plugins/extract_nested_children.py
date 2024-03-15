class FilterModule(object):

    def filters(self):
        return {
            'extract_nested_children': self.extract_nested_children,
        }

    def extract_nested_children(self, value):
        go_inner_loop=True
        retval=""
        interimval=value
        while(go_inner_loop):
          if(interimval['children_count']==1):
            interimval=interimval['children'][0]
            go_inner_loop=True
          if(interimval['children_count']!=1):
            go_inner_loop=False
        retval=interimval
        return retval
