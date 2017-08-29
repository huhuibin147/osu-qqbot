# -*- coding: utf-8 -*-

import random
user_dict = {}
rbq = set([])
rbq_list = {}
def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    #群限制 Q号 614892339
    if contact.ctype == 'group' and contact.qq == '614892339':
        if len(rbq) > 20:
            rbq.pop()
        rbq.add(member.name)
        if content == '!dalou':
            bot.SendTo(contact, 'dalouBot登场!')
        elif content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif '!setid' in content:
            user_dict[member.qq] = content.split(' ')[1]
            bot.SendTo(contact, '绑定成功!')
        elif content == '!id':
            bot.SendTo(contact, user_dict[member.qq])
        elif content == '!rbq':
            r = random.choice(list(rbq))
            msg = '%s 获得了一个 %s 作为rbq' % (member.name, r)
            if rbq_list.get(member.qq) is None:
                rbq_list[member.qq] = set([r])
            elif len(rbq_list[member.qq]) == 5:
                rem_r = random.choice(list(rbq_list[member.qq]))
                msg = 'rbq太多了,%s 已被抛弃!' % rem_r
                rbq_list[member.qq].remove(rem_r)
            else:
                rbq_list[member.qq].add(r)
            print(rbq_list)                
            bot.SendTo(contact, msg)
        elif content == '!myrbq':
            if rbq_list.get(member.qq) is None or len(rbq_list.get(member.qq)) == 0:
                bot.SendTo(contact, '你没有rbq醒醒!')
                return
            msg = '%s 有%s个rbq:\n' % (member.name, len(rbq_list[member.qq]))
            r_list = list(rbq_list[member.qq])
            for i,r in enumerate(r_list):
                msg2 = '%s.%s\n' % (str(i+1), r)
                msg += msg2
            msg = msg[0:-1]
            bot.SendTo(contact, msg)