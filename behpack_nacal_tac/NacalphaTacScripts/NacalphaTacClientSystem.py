# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()

ENGINE_NAMESPACE = clientApi.GetEngineNamespace()
ENGINE_SYSTEM_NAME = clientApi.GetEngineSystemName()
LEVEL_ID = clientApi.GetLevelId()

ClientSystem = clientApi.GetClientSystemCls()
ClientCompFactory = clientApi.GetEngineCompFactory()

class NacalphaTacClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        # 首先初始化NacalphaTacClientSystem的基类ClientSystem
        super(NacalphaTacClientSystem, self).__init__(namespace, systemName)
        print ("==== NacalphaTacClientSystem Init ====")
        self.ListenForEvent(ENGINE_NAMESPACE, ENGINE_SYSTEM_NAME, "UiInitFinished", self, self.UiInitFinished)

    def UiInitFinished(self, args):
        def LaterTrigger():
            ClientCompFactory.CreateTextNotifyClient(LEVEL_ID).SetLeftCornerNotify("§e§l[战术投掷道具-可合成]§r发送§a“合成”§f可合成帮助书，使用§a“创造模式背包-自然-生物蛋”§f可获取道具")
        comp=ClientCompFactory.CreateGame(LEVEL_ID)
        comp.AddTimer(5,LaterTrigger)

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):
        pass