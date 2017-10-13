
def png2txt():
    # 打开图片
    f = open('test.png','rb')

    # 写文件
    f2 = open('test.txt','wb')
    f2.write(f.read())

    f.close()
    f2.close()


def txt2png():
    # 打开文件
    f = open('test.txt','rb')

    # 写文件
    f2 = open('test2.png','wb')
    f2.write(f.read())

    f.close()
    f2.close()

def png2byte(img):
    # 打开文件
    f = open(img, 'rb')
    b = f.read()
    f.close()
    return b

def post2site(img, groupid=641236878):
    import requests 
    import json
    url = 'http://new.int100.site/bot/save_img.php'
    res = requests.post(url, data = png2byte(img))
    print(res.text)
    url2 = 'http://new.int100.site/bot/send_msg.php?to=%s&msg=%s&type=1' % (groupid, res.text)
    res = requests.get(url2)
     

# post2site('t.png')