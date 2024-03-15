class FilterModule(object):

    def filters(self):
        return {
            'flatten_children_list_to_ifs': self.flatten_children_list_to_ifs,
        }


    def flatten_children_list_to_ifs(self, value):
       retval=[]
       for child in value:
          if(child["type"]=="rack"):
             for child2 in child["children"]:
                if((child2["type"] =="leaf") or (child2["type"] =="leaf-pair")):
                   for child3 in child2['children']:
                      if(child3["type"]=="interface"):
                         transient_item={}
                         transient_item.update({"rack_id": child["id"]})
                         transient_item.update({"rack_label": child["label"]})
                         transient_item.update({"sw_id": child2["id"]})
                         transient_item.update({"sw_type": child2["type"]})
                         transient_item.update({"sw_label": child2["label"]})
                         transient_item.update({"interface_aep_id": child3["id"]})
                         transient_item.update({"interface_aep_label": child3["label"]})
                         retval.append(transient_item)
       return retval
