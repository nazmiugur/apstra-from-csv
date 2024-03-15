class FilterModule(object):

    def filters(self):
        return {
            'cleanup_specific_leaf_ids': self.cleanup_specific_leaf_ids,
        }

    def cleanup_specific_leaf_ids(self, value, leaves):
        leaf_names=leaves.split(",")
        leaf_ids=[]
        for leafname in leaf_names:
           for k,val in value['nodes'].items():
               if ((val["role"] == "leaf") and (val["label"] == leafname)):
                  leaf_ids.append(val["id"])
        return(leaf_ids)
               
