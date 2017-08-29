# -*- coding: utf-8 -*-

def onQQMessage(bot, contact, member, content):
    #contact :  ctype/qq/uin/nick/mark/card/name 
    #群限制 Q号 614892339
    if contact.ctype == 'group' and contact.qq == '614892339':
        if content == '!dalou':
            bot.SendTo(contact, 'dalouBot登场!')
        elif content == '!help':
            bot.SendTo(contact, 'dalou只会打爆你!')
        elif content in '!setid':
            
            bot.SendTo(contact, 'dalou只会打爆你!')