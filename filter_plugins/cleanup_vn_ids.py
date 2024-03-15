class FilterModule(object):

    def filters(self):
        return {
            'cleanup_vn_ids': self.cleanup_vn_ids,
        }

    def cleanup_vn_ids(self, value, vn_name):
        for k,val in value['nodes'].items():
            if val["label"] == vn_name:
               return (val["id"])
            
