# 状態定義 ----------------------------------------------------
IDLE = 0
FORWARD = 1
BACKWARD = 2
RIGHT = 3
LEFT = 4

# ステートマシン -------------------------------------------------
def stateMachine(sState, vFlagInfo, vEnemyInfo):

    sHorizontalCenter = 160
    sPositionThreshHigh = 20
    sPositionThreshLow = 5
    sSizeThreshHigh = 80
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