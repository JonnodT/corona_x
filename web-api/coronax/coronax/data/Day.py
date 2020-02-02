

'''
 user_id = req_dict['id']
        day_idx = req_dict['day_idx']
        general_eval = req_dict['general_eval']
        sleep_time = req_dict['sleep_time']
        symptoms = req_dict['symptoms']
        blog = req_dict['blog']

'''
class Day:
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            self.key = value