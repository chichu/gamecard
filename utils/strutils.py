#encoding:utf-8

def check_cardfile_format(line,format):
    return (len(line.split(",")) == len(format.split("&")))

def transfer_format(lines):
    tmp_list = []
    for line in lines: 
        card_id = line.split(",")[0]
        count = int(line.split(",")[1])
        tmp_list.extend([card_id]*count)
    return tmp_list
       
def get_cardfile_set(all_line,has_passwd=False):
    tmp_items = []
    for line in all_line:
        line = line.strip()
        if has_passwd:
            tmp_dict = {"status":"normal","card_id":line.split(",")[0],"passwd":line.split(",")[1]}
        else:
            tmp_dict = {"status":"normal","card_id":line}
        tmp_items.append(tmp_dict)
    return return_items
    
def insert_card_ids(all_line,item):
    collect_name = get_collect_name(item.id)
    cursor =  get_mongodb_cursor(collect_name)
    cursor.create_index("status",unique=False)
    if item.format.index("count") == -1:
        cursor.create_index("card_id",unique=True)
    else:
        all_line = transfer_format(all_line)
    inserts = []
    if item.format.index("passwd") == -1:
        inserts = get_cardfile_set(all_line)
    else:
        inserts = get_cardfile_set(all_line,has_passwd=True)
    for insert in inserts:
        try:
            cursor.insert(insert)
        except Exception,e:
            continue 
    curosr.commit()
    return cursor.count()

ALL_ALPHA = "ABCDEFGHIJKLMNOPQRSTWXYZ"
MAX_LENGTH = 5
def get_ordered_act(acts,start_alpha_index):
    hot = acts.filter(is_hot=True).order_by('-start_time')
    new = acts.order_by('-start_time')
    if len(hot) > MAX_LENGTH:
        hot =  hot[0:MAX_LENGTH]
    if len(new) > MAX_LENGTH:
        new =  new[0:MAX_LENGTH]
    return_list = [hot,new]
    alphas = []
    for i in range(0,len(ALL_ALPHA)):
        alpha = ALL_ALPHA[i]
        tmp = acts.filter(name_start_alpha__iexact=alpha.strip()) 
        alphas.append((i/4+start_alpha_index,alpha,tmp))
    return_list.append(alphas)
    return tuple(return_list)
    
