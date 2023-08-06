import uuid
import random
import elist.elist as elel

def gen_guid():
    rand = str(uuid.uuid4()).split('-')
    uni =  str(uuid.uuid1()).split('-')
    arr = [rand,uni]
    guid = []
    for i in range(len(rand)):
        index = random.randint(0,1)
        guid.append(arr[index][i])
    return(elel.join(guid,'-'))     

