#encoding:utf-8

def get_cardfile_dict(format,line):
    values = line.split(',')
    keys = format.split('&')
    if len(values) != len(keys) or len(values) == 0:
        return None
    return_items = []
    count = 1
    if len(value) > 1:
        count = (keys[1] == "count") and int(values[1]) or 1 
    for j in range(0,count):
        tmp_dict = {"status":"normal"}
        for i in range(0,len(values)):
            tmp_dict[keys[i].strip()] = values[i].strip()
        return_items.append(tmp_dict)
    return return_items
    
def check_cardfile_format(first_line,item_format):
    print (len(first_line.split(",")) == len(item_format.split("&")))
    return (len(first_line.split(",")) == len(item_format.split("&")))

def get_collect_name(item_id):
    CARDID_FILE_TEMPLATE = "%s-id_cards"
    return CARDID_FILE_TEMPLATE%(item_id)

ALPHA_SECT = ["ABCD","EFGH","IJKL","MNOP","QRST","WXYZ"]
MAX_LENGTH = 10
def get_ordered_act(acts):
    hot = acts.filter(is_hot=True)
    new = acts.order_by('-start_time')
    if len(hot) > MAX_LENGTH:
        hot =  hot[0:9]
    if len(new) > MAX_LENGTH:
        new =  new[0:9]
    return_list = [hot] 
    for sect in ALPHA_SECT: 
        return_list.append(acts.filter(name_start_alpha__in=sect))
    return_list.append(new)
    return turple(return_list)
    
