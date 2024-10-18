# 状態定義 ----------------------------------------------------
IDLE = 0
FORWARD = 1
BACKWARD = 2
RIGHT = 3
LEFT = 4
AVOID_L = 5 #左回避移動
AVOID_R = 6 #回避分右移動

# ステートマシン -------------------------------------------------
def stateMachine(sState, vFlagInfo, vEnemyInfo):
    sHorizontalCenter = 160
    sPositionThreshHigh = 20
    sPositionThreshLow = 5
    sSizeThreshHigh = 80
    sSizeThreshLow = 5

    if sState == AVOID_L:#敵検出終了で右移動
        if vEnemyInfo[0] == -1:
            sState = AVOID_R

    elif sState == AVOID_R: #右移動完了で通常動作に戻す
        if vFlagInfo[0] < sHorizontalCenter + sPositionThreshLow:
            sState = FORWARD
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE

    elif sState == IDLE:
        if vFlagInfo[0] != -1 and vFlagInfo[2] < sSizeThreshHigh:
            sState = FORWARD

    elif sState == FORWARD:
        if vEnemyInfo[0] != -1:#敵検出中 （緑が写っている）の場合
            sState = AVOID_L 
        elif vFlagInfo[0] > sHorizontalCenter + sPositionThreshHigh:
            sState = RIGHT
        elif vFlagInfo[0] < sHorizontalCenter - sPositionThreshHigh:
            sState = LEFT
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE
        
    elif sState == RIGHT:
        if vEnemyInfo[0] != -1:#敵検出中（緑が写っている）の場合
            sState = AVOID_L
        elif vFlagInfo[0] < sHorizontalCenter + sPositionThreshLow:
            sState = FORWARD
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE

    elif sState == LEFT:
        if vFlagInfo[0] > sHorizontalCenter - sPositionThreshLow:
            sState = FORWARD
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE

   
    return sState

# ステートマシン -------------------------------------------------
def stateMachineGoal(sState, vFlagInfo, vEnemyInfo):

    sHorizontalCenter = 160
    sPositionThreshHigh = 30
    sPositionThreshLow = 5
    sSizeThreshHigh = 400
    sSizeThreshLow = 5

    if sState == IDLE:
        if vFlagInfo[0] != -1 and vFlagInfo[2] < sSizeThreshHigh:
            sState = FORWARD
    elif sState == FORWARD:
        if vFlagInfo[0] > sHorizontalCenter + sPositionThreshHigh:
            sState = RIGHT
        elif vFlagInfo[0] < sHorizontalCenter - sPositionThreshHigh:
            sState = LEFT
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE
    elif sState == RIGHT:
        if vFlagInfo[0] < sHorizontalCenter + sPositionThreshLow:
            sState = FORWARD
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE
    elif sState == LEFT:
        if vFlagInfo[0] > sHorizontalCenter - sPositionThreshLow:
            sState = FORWARD
        elif vFlagInfo[2] < sSizeThreshLow or vFlagInfo[2] > sSizeThreshHigh or vFlagInfo[0] == -1:
            sState = IDLE

    return sState