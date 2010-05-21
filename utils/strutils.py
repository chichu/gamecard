#encoding:utf-8
import urllib

def get_username_from_cookie(request):
    '''
       _178:uid+"#"+email+"#"+username
       _i:加密信息段_md5验证段_timestamp
       md5验证段的内容=uid<>email<>username<>timestamp+4b21e6f4
       用_178c里得到的uid，username，email去和_i中的md5段验证
    '''
    if (not request.COOKIES.has_key('_178c')) or (not request.COOKIES.has_key("_i")):
        return '' 
    (uid,email,username) = tuple(urllib.unquote(request.COOKIES.get('_178c')).split('#'))
    (code,md5code,timestamp) = tuple(urllib.unquote(request.COOKIES.get('_i')).split('_'))
    seed = "%s<>%s<>%s<>%s%s" % (uid,email,username,timestamp,'4b21e6f4')
    import md5
    m = md5.new(seed)
    m.digest()
    if md5code == m.hexdigest():
        return username 
    return '' 
    
def check_cardfile_format(line,format):
    return (len(line.split(",")) == len(format.split("&")))

def get_collect_name(item_id):
    return "card_ids_%s"%item_id
    
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
    return tmp_items
    
def insert_card_ids(all_line,item):
    from dbutils import get_mongodb_collect
    collect_name = get_collect_name(item.id)
    collect =  get_mongodb_collect(collect_name)
    collect.create_index("status",unique=False)
    if item.format.find("count") == -1:
        collect.create_index("card_id",unique=True)
    else:
        all_line = transfer_format(all_line)
    inserts = []
    if item.format.find("passwd") == -1:
        inserts = get_cardfile_set(all_line)
    else:
        inserts = get_cardfile_set(all_line,has_passwd=True)
    for insert in inserts:
        try:
            collect.insert(insert)
        except Exception,e:
            continue 
    return collect.count()


MAX_LENGTH = 5
def get_ordered_act(acts,start_alpha_index):
    hot = acts.filter(is_hot=True).order_by('-start_time')
    new = acts.order_by('-start_time')
    if len(hot) > MAX_LENGTH:
        hot =  hot[0:MAX_LENGTH]
    if len(new) > MAX_LENGTH:
        new =  new[0:MAX_LENGTH]
    return_list = [hot,new]
    alphas = get_alpha_ordered_act(acts,start_alpha_index)
    return_list.append(alphas)
    return tuple(return_list)

ALL_ALPHA = "ABCDEFGHIJKLMNOPQRSTWXYZ"    
def get_alpha_ordered_act(acts,start_alpha_index):
    alphas = []
    for i in range(0,len(ALL_ALPHA)):
        alpha = ALL_ALPHA[i]
        tmp = acts.filter(name_start_alpha__iexact=alpha.strip()) 
        #if bool(tmp):
         #   alphas.append((i/4+start_alpha_index,alpha,tmp))
        alphas.append((i/4+start_alpha_index,alpha,tmp))
    return alphas
    
