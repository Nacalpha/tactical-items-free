# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
compFactory = serverApi.GetEngineCompFactory()

LEVEL_ID = serverApi.GetLevelId()

# 在modMain中注册的Server System类
class NacalphaTacServerSystem(ServerSystem):

    # ServerSystem的初始化函数
    def __init__(self, namespace, systemName):
        # 首先调用父类的初始化函数
        super(NacalphaTacServerSystem, self).__init__(namespace, systemName)
        print ("===== NacalphaTacServerSystem init =====")
        # 初始时调用监听函数监听事件
        self.ListenEvent()

    # 监听函数，用于定义和监听函数。函数名称除了强调的其他都是自取的，这个函数也是。
    def ListenEvent(self):
        # 在自定义的ServerSystem中监听引擎的事件ServerChatEvent，回调函数为OnServerChat
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)

    # 反监听函数，用于反监听事件，在代码中有创建注册就对应了销毁反注册是一个好的编程习惯，不要依赖引擎来做这些事。
    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ServerChatEvent", self, self.OnServerChat)

    # 监听ServerChatEvent的回调函数
    def OnServerChat(self, args):
        print ("==== OnServerChat ==== "), args
        # 生成掉落物品
        # 当我们输入的信息等于右边这个值时，创建相应的物品
        # 创建Component，用来完成特定的功能，这里是为了创建Item物品
        playerId = args["playerId"]
        comp = serverApi.CreateComponent(playerId, "Minecraft", "item")
        if args["message"] == "合成":    
            args['cancel'] = True                  
            # 调用SpawnItemToPlayerInv接口生成物品到玩家背包，参数参考《MODSDK文档》
            comp.SpawnItemToPlayerInv({"itemName":"nacal_tac:tac_guidebook", "count":1, 'auxValue': 0}, playerId)
            def LaterTrigger():
                comp = compFactory.CreateMsg(playerId)
                comp.NotifyOneMessage(playerId, "§e§l[战术投掷道具-可合成]§r合成帮助书已发送到背包", "")
            comp=compFactory.CreateGame(LEVEL_ID)
            comp.AddTimer(0.1,LaterTrigger)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        print ("===== NacalphaTacServerSystem Destroy =====")
        # 调用上面的反监听函数来销毁
        self.UnListenEvent()
