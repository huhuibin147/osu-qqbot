#osu!新人群月度精彩视频集锦
replay_bilibili = [
    {
        'title':'第1集2017.5',
        'url':'https://www.bilibili.com/video/av10959103/'
    },
    {
        'title':'第2集2017.6',
        'url':'https://www.bilibili.com/video/av11800563/'
    },
    {
        'title':'第3集2017.7',
        'url':'https://www.bilibili.com/video/av12957061/'
    },
    {
        'title':'第4集2017.8(第一季完结)',
        'url':'https://www.bilibili.com/video/av14046324/'
    }
]

#名词解释
osu_words = {
    'map':'指beatmap，每首歌曲的每个难度都是一个beatmap，它是osu!的主体。',
    'fc':'fullcombo，全连，指一首map达到了它的最大combo数，也就是没有miss任何一个。有时候slider会 断尾，这时combo会少若干个，可以称之为伪fc，当然称为fc也可以。',
    'acc':'完成一张map后的正确率，也常用于玩家的总正确率。',
    'solo':'单人玩就叫solo。',
    'mp':'多人一起玩就叫mp。',
    'taiko':'太鼓模式。',
    'ctb':'接水果模式。',
    'afk':'暂离，可能是长时间的，也可能是短时间的。',
    'nf':'nofail，不失败模式',
    'ht':'halftime，半速模式',
    'hr':'hardrock，其实这我都不知道怎么翻译，反正就是减小点的大小，增加扣血量，加大oa的一个模式',
    'dt':'两个含义，一个是doubletime，名字意思是双倍速模式，但实际是1.5倍速；另一个是蛋疼。。',
    'hid':'hidden，渐隐模式',
    'fl':'flashlight，闪光灯模式',
    'sb':'storyboard，这个是做图时用到的，翻译为故事板，其实就是脚本，用于控制一些歌曲的图片效果，常用做显示歌曲制作者或者歌词之类的。',
    'bpm':'歌曲的速度，每分钟节拍数的单位。一般bpm越高需要的手速越快，map的难度也越高。',
    'oa':'歌曲的整体难度，一般指点出现的速度、光圈缩小的速度、转盘的难度、点击要求的精度等等。oa越高难度越大，目前rank的map oa不能超过9，否则是不能rank的。',
    'mapper':'做图的人统称为mapper。',
    'bat':'翻译蝙蝠，其实是osu!的管理员，他们有管理osu!的权限。',
    'mat':'主要是modding别人的图，觉得不错的可以pubble。pubble请看下面。',
    'mod':'或者modding，就是检查别人做的图并给出自己的意见。',
    'pending':'玩家做好一张图并上传后首先是pending状态，需要等待bat们的检查。',
    'wip':'还没有做完的图。',
    'star':'别人做完图后其他人可以在贴子的回复中给一个star，表示支持这张图。',
    'pubble':'一张做好的图如果有mat检查并通过了，mat会给一个pubble，这时候就可以找bat检查了。现在pubble系统已经不用了，所以可以直接找bat。',
    'bubble':'一张图如果bat检查通过后会给一个bubble，这时候再来一个bat检查并通过后就可以rank或者app了。',
    'rebubble':'如果一张bubble图被另一个bat检查后觉得有问题就会去掉bubble，这时候需要mapper重新修改过并提交，bat检查完并通过后才能rebubble。',
    'rank':'做的map可以被玩家玩并且可以统计用于排名的分数的就叫map被rank了。只有bat能rank map。',
    'app':'approved的缩写，指map虽然可以被玩家玩，但是由于时间过高或者combo太多或者分数过高，就会成为app的图，此时map的分数不能用于统计玩家的总排名，但是会记录玩家的acc。只有bat能app map。',
    '沙包':'玩osu!的新手或者玩了有一段时间但仍然玩的不是很好的玩家。',
    '触手':'指玩osu!非常厉害的玩家，比如随手FC5星图的，随手搞掉一张鬼畜的等等。范围太广不好评价。',
    '路人断':'指不该miss的地方结果miss了，就叫路人断（很让人恼火的一个东西……其实还是心态的问题）',
    'ht':'halftime，半速模式，但实际是0.75倍速。',
    'fl':'flashlight，手电筒模式',
    'ar':'光圈缩小的速度和点出现的速度',
    'circle':'map中的单个的小圆圈',
    'slider':'map中要拖动的滚动条，有单向的和来回的',
    'spinner':'map中的转圈，是转的，不是让你在转圈的最后点一下。。',
    'note':'一个个的粉饼就是了',
    'supporter':'会员，有一些会员专用的权限，可以游戏中直接下图，有更多的pending图位置，黄色字等等。',
    'charts':'每月的排名比赛，经常在打图结束的时候看到有两行排名，第二个就是月排名。官方在每月开始的时候会选一些图给大家打，这些图的总分最高的就是当月冠军，会获得1个月supporter。',
    'irc':'游戏中大家会看到一些灰色的字，那是使用irc聊天客户端登录的，只用来聊天用。',
    'AIMod':'电脑来判定你做的图有什么问题，一般主要用来看是不是有note没对准节奏线。',
    'snap':'有时候会有note没对准节奏线，这时候要把它对准叫就snap。',
    'distance':'note与note之间的间距，这在做图中非常重要，不考虑间距是很大的问题，乱摆note是新手做图常犯的错误。',
    'hit whistle finish clap':'四种音效，可自由替换。',
    'break time':'map中的休息时间，一般不宜过长，也不宜随便放break time，会影响打图的连贯性。',
    'timing':'map的时间设置，主要分为bpm和offset。',
    'timing points':'时间点，有红线（变bpm）、黄线（歌曲预览）、绿线（变速或者变音效）、蓝线（书签）',
    'offset':'当前时间线距离音效开始的时间差。offset和bpm都影响到一张图的打击准确率，如果bpm是正确的但是offset差了20ms都是错误的timing。',
    'mu':'加好友的意思',
    '复读':'osu的一项特殊行为，重复上面的人的话',
    'od':'判定,越高判定范围越小',
    'dalou':'群主一样的存在',
    'inter':'幕后黑手!'
}