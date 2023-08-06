import efuntool.efuntool as eftl
import elist.elist as elel
from efdir import fs
import ndtreepy.cmmn as cmmn



def calc_next_id(tree):
    if(len(tree) ==0):
        return(0)    
    else:    
        ids = tree.keys()
        return(max(ids)+1)


def creat_root(*args):
    _id = eftl.optional_arg(0,*args)
    if(_id < 0):
        raise(ValueError('root _id must >=0'))
    else:    
        r = {
            "_id":_id,
            "_fstch":None,
            "_lsib":None,
            "_rsib":None,
            "_parent":None,
            "_tree":_id
        }
        r["_guid"] = cmmn.gen_guid()
        return(r)

def creat_tree(*args):
    root = creat_root(*args)
    tree = {}
    tree[root["_id"]] = root
    return(tree)



def creat_nd(tree,*args):
    dflt = calc_next_id(tree) 
    _id = eftl.optional_arg(dflt,*args)
    if(_id < 0):
        raise(ValueError('_id must >=0'))
    else:    
        nd =  {
            "_id":_id,
            "_fstch":None,
        }
        nd["_guid"] = cmmn.gen_guid()
    return(nd)


###



def is_inited(nd):
    cond = ("_tree" in nd) and (nd["_tree"] >=0)
    return(cond)

def is_root(nd):
    cond0 = ("_tree" in nd) and (nd["_tree"] == nd["_id"])
    cond1 = is_inited(nd)
    return(cond0 and cond1)


def is_fstch(nd):
    cond = ("_lsib" in nd) and (nd["_lsib"] == None)
    return(cond)


def is_lstch(nd):
    cond = ("_rsib" in nd) and (nd["_rsib"] == None)
    return(cond)


def is_leaf(nd):
    cond = ("_fstch" in nd) and (nd["_fstch"] == None)
    return(cond)


def is_lonely(tree,nd):
    cond = is_root(nd)
    if(cond):
        return(True)
    else:
        parent = get_parent(tree,nd)
        children = get_children(tree,parent)
        return(len(children) == 1)

#########

def append_child(tree,nd,*args):
    dflt = creat_nd(tree)
    child = eftl.optional_arg(dflt,*args)
    child["_tree"] = nd["_tree"]
    child["_rsib"] = None
    cond = is_leaf(nd)
    if(cond):
        nd["_fstch"] = child["_id"]
        child["_lsib"] = None
    else:    
        old_lstch = get_lstch(tree,nd)
        del old_lstch["_parent"] 
        old_lstch["_rsib"] = child["_id"]
    child["_parent"]  = nd["_id"] 
    tree[child["_id"]] = child
    return(child)


###########




def get_children(tree,nd):
    children = []
    child = get_fstch(tree,nd)
    while(child != None):
        children.append(child)
        child = get_rsib(tree,child)
    return(children)


def get_fstch(tree,nd):
    fstch = None if(is_leaf(nd)) else tree[nd["_fstch"]]
    return(fstch)


def get_lstch(tree,nd):
    children = get_children(tree,nd)
    if(len(children) == 0):
        return(None)
    else:
        return(children[-1])


#####

def get_rsib(tree,nd):
    rsib = None if(is_lstch(nd)) else tree[nd["_rsib"]]
    return(rsib)





def get_lstsib(tree,nd,including_self=False):
    lstrsib = nd
    rsib = get_rsib(tree,nd)
    while(rsib != None):
        lstrsib = rsib
        rsib = get_rsib(tree,rsib)
    if(including_self):
        return(lstrsib)
    else:
        cond = (lstrsib["_id"] != nd["_id"])
        rslt = lstrsib if(cond) else None
        return(rslt)

def get_sibs(tree,nd,including_self=False): 
    parent = get_parent(tree,nd)
    sibs = []
    if(parent != None):
        sibs = get_children(tree,parent)
    else:
        sibs = [nd]
    if(including_self):
        pass
    else:
        sibs = elel.filter(sibs,lambda sib:sib["_id"]!=nd["_id"])
    return(sibs) 

def get_sibseq(tree,nd):
    sibs = get_sibs(tree,nd,including_self=True)
    seq = elel.cond_select_indexes_all(sibs,cond_func=lambda sib:sib==nd)[0]
    return(seq)


def get_lsib(tree,nd):
    sibs = get_sibs(tree,nd,including_self=True)
    seq = elel.cond_select_indexes_all(sibs,cond_func=lambda sib:sib==nd)[0]
    if(seq == 0):
        return(None)
    else:
        return(sibs[seq-1])

#####
def get_parent(tree,nd):
    cond = is_root(nd)
    parent = None
    if(cond):
        parent = None
    else:
        lstrsib = get_lstsib(tree,nd,True)
        parent = tree[lstrsib["_parent"]]
    return(parent)    


def get_root(tree):
    ids = list(tree.keys())
    _id = ids[0]
    nd = tree[_id]
    parent = get_parent(tree,nd)
    lst_parent = nd 
    while(parent != None):
        lst_parent = parent
        parent = get_parent(tree,parent)
    return(lst_parent)    


def get_ances(tree,nd,including_self=False):
    ances = []
    parent = get_parent(tree,nd)
    while(parent != None):
        ances.append(parent)
        parent = get_parent(tree,parent)
    if(including_self):
        ances = [nd] + ances
    else:
        pass
    return(ances)

####

def get_depth(tree,nd):
    ances = get_ances(tree,nd,including_self=True)
    return(len(ances) - 1)


####

def get_rsib_of_fst_ance_having_rsib(tree,nd):
    parent = get_parent(tree,nd)
    while(parent != None):
        rsib = get_rsib(tree,parent)
        if(rsib != None):
            return(rsib)
        else:
            parent = get_parent(tree,parent)
    return(None) 


def get_sdfs_next(tree,nd):
    fstch = get_fstch(tree,nd)
    if(fstch != None):
        return(fstch)
    else:
        rsib = get_rsib(tree,nd)
        if(rsib != None):
            return(rsib)
        else:
            return(get_rsib_of_fst_ance_having_rsib(tree,nd))


def get_sdfs(tree,nd):
    nd_depth = get_depth(tree,nd)
    sdfs = []
    while(nd != None):
        sdfs.append(nd)
        nd = get_sdfs_next(tree,nd)
        if(nd != None):
            depth = get_depth(tree,nd)
            if(depth < nd_depth):
                break
    return(sdfs)   


def tree2sdfs(tree):
    root = get_root(tree)
    sdfs = get_sdfs(tree,root)
    return(sdfs)

####

def update_disconnected_nodes(tree,nd):
    nsdfs = get_sdfs(tree,nd)
    treeid = nsdfs[0]['_id']
    for nd in nsdfs:
        nd['_tree'] = treeid
    return(nsdfs)


def update_orig_nodes(tree,nsdfs):
    ntree = {}
    for nd in nsdfs:
        _id = nd['_id']
        ntree[_id] = nd
        del tree[_id]
    return([ntree,tree])  


def leafize(nd):
    nd['_fstch'] = None
    return(nd)

def rootize(nd):
    nd['_lsib'] = None
    nd['_rsib'] = None
    nd['_parent'] = None
    return(nd)

def sdfs2tree(sdfs):
    tree = {}
    for nd in sdfs:
        tree[nd['_id']] = nd
    return(tree)    


def disconnect(tree,nd):
    cond = is_root(nd)
    if(cond):
        return([nd,{},tree])
    elif(is_lonely(tree,nd)):
        parent =  tree[nd['_parent']]
        leafize(parent);
        nsdfs = update_disconnected_nodes(tree,nd)
        new_tree,old_tree = update_orig_nodes(tree,nsdfs)
        rootize(nd)
        return([nd,new_tree,old_tree])         
    else:
        if(is_fstch(nd)):
            rsib = get_rsib(tree,nd)
            rsib['_lsib'] = None
            parent = get_parent(tree,nd) 
            parent['_fstch'] = nd['_rsib']  
            nsdfs = update_disconnected_nodes(tree,nd)
            new_tree,old_tree = update_orig_nodes(tree,nsdfs)
            rootize(nd)
            return([nd,new_tree,old_tree])
        elif(is_lstch(nd)): 
            lsib = get_lsib(tree,nd) 
            lsib['_rsib'] = nd['_rsib']
            lsib['_parent'] = nd['_parent']
            nsdfs = update_disconnected_nodes(tree,nd) 
            new_tree,old_tree = update_orig_nodes(tree,nsdfs)
            rootize(nd)
            return([nd,new_tree,old_tree])
        else:
            lsib = get_lsib(tree,nd) 
            lsib['_rsib'] = nd['_rsib']
            nsdfs = update_disconnected_nodes(tree,nd)
            new_tree,old_tree = update_orig_nodes(tree,nsdfs)
            rootize(nd)
            return([nd,new_tree,old_tree])




###
def dump(tree):
    return(json.dumps(tree))

def dump2file(tree,attr):
    root = ndnd.get_root(tree)
    fs.wjson(root[attr]+'.json',tree)

def load(fn):
    tree = {}
    if(isinstance(fn,str)):
        tree = fs.rjson(fn)
    else:
        tree = fn
    ntree = {}
    for k in tree:
        ntree[int(k)] = tree[k]
    return(ntree)


###

def get_nds_via_attr(tree,attr,val):
    nds = []
    for _id in tree:
        nd = tree[_id]
        cond = (attr in nd)
        if(cond):
            v = nd[attr]
            if(v == val):
                nds.append(nd)
            else:
                pass        
        else:
            pass
    return(nds)



###
