
mod_list={
    0: 'NONE',
    1: 'NF',
    2: 'EZ',
    3: 'NV',
    4: 'HD',
    5: 'HR',
    6: 'SD',
    7: 'DT',
    8: 'Relax',
    9: 'HT',
    10: 'NC',
    11: 'FL',
    12: 'AT',
    13: 'SO',
    14: 'AP',
    15: 'PF',
    16: 'PF',
    
}

def getMod(num=16504):
    '''NC出现的话删除DT，PF出现的话删除SD'''
    mods = []
    i=1
    while num:
        if num&0x1:
            mods.append(mod_list.get(i))
        num=num>>1
        i+=1
    if not mods:
        return ['none']
    if 'NC' in mods:
        mods.remove('DT')
    if 'PF' in mods:
        mods.remove('SD')
    
    return mods


if __name__ == '__main__':
    getMod(584)
