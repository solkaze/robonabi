# ライブラリ等のインポート ------------------------------------------
import cv2
import numpy as np
import locateTarget as lt
import stateMachine as sm
import time

from ClsDualMotorControl import ClsDualMotorControl
#from ClsDualMotorControl import ClsDualMotorControl

# イメージセンサの初期化 ------------------------------------------
videoCap = cv2.VideoCapture(0)
sWidthSensor = 640
sHeightSensor = 480
videoCap.set(cv2.CAP_PROP_FRAME_WIDTH, sWidthSensor)
videoCap.set(cv2.CAP_PROP_FRAME_HEIGHT, sHeightSensor)

# 処理画像サイズの決定 ------------------------------------------
sResizeRatio = 0.5
if videoCap.isOpened():
    sReturn, imCamera = videoCap.read()
    print('W: ', imCamera.shape[1], ', H:', imCamera.shape[0])
    sWidth = int(imCamera.shape[1] * sResizeRatio)
    sHeight = int(imCamera.shape[0] * sResizeRatio)

# 画像処理・表示ループ外の変数 ------------------------------------
sDisplayRate = 10
sMode = 1
sFrame = 0

# 画像記録バッファ -----------------------------------------------
imGray = np.ndarray((sHeight, sWidth))
imRedBinary = np.ndarray((sHeight, sWidth))
imGreenBinary = np.ndarray((sHeight, sWidth))

# ステート初期化 -------------------------------------------------
sState = sm.IDLE

# Dual motor controller初期設定 ---------------------------------
vPortsDrive = [23, 22, 25, 9, 10]  #AIN1, AIN2, BIN1, BIN2, STBY
vPortsPWM = [12, 13]
sFrequency = 10000
ClsDmc = ClsDualMotorControl(vPortsDrive, vPortsPWM, sFrequency)

Red_Flag = False
Blue_Flag = False
Goal_Flag = False
#タイマー開始
timeout = 180
start_time = time.time() #開始時間の取得
goal_time = 0


# 敵検出時のタイマー変数
enemy_detected_start_time = None
enemy_detected_duration = 0

# 画像処理・表示ループ -------------------------------------------
while videoCap.isOpened() :
    
    # 現在の時間との差分を記録
    elapsed_time = time.time() - start_time
    
    # 終了処理
    if elapsed_time > timeout:
        break
    # 画像の取得 -----------------------------------------------
    sReturn, imCamera = videoCap.read()
    if not sReturn:
        break

    # 画像サイズの変更 ------------------------------------------
    imResize = cv2.resize(imCamera , (sWidth, sHeight))
    
    # キーボード入力 -------------------------------------------- 
    sKey = cv2.waitKey(1) & 0xFF
    if sKey >= ord('0') and sKey <= ord('9'):
        sMode = sKey - ord('0')

    # 動作モードの選択 ------------------------------------------- 
    if sMode == 1:
        imDisplay = imResize
        if sKey == ord('w'):
            ClsDmc.stop()

            ClsDmc.driveMotor(0, 0, 80)
            ClsDmc.driveMotor(1, 0, 85)
        elif sKey == ord('x'):
            ClsDmc.stop()
        elif sKey == ord('a'):
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 80)
            ClsDmc.driveMotor(1, 0, 60)
        elif sKey == ord('d'):
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 50)
            ClsDmc.driveMotor(1, 0, 80)
        elif sKey == ord('s'):
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 1, 80)
            ClsDmc.driveMotor(1, 1, 80)
            
        if sFrame == 999:
            print('1000 frames have passed')
            
    elif sMode == 2:
        imDisplay = imResize
        imGaussianHSV = lt.preprocess(imResize)

         # 赤色、青色、黄色のターゲットの検出処理
        if not Red_Flag:
            vFlagInfo, imBinary, Size = lt.locateFlag(imGaussianHSV)
            if Size >= 60:
                Red_Flag = True
        elif not Blue_Flag:
            vFlagInfo, imBinary, Size = lt.locateTower(imGaussianHSV)
            if Size >= 60:
                Blue_Flag = True
        else:
            vFlagInfo, imBinary, Size = lt.locateGoal(imGaussianHSV)
        
        vEnemyInfo, imEnemyBinary, EnemySize = lt.locateEnemy(imGaussianHSV)
        sPreviousState = sState

        count = 0
        # 赤色が見えている場合は青色をターゲットに移動
        if not Red_Flag or not Blue_Flag:
            sState = sm.stateMachine(sState, vFlagInfo, vEnemyInfo)

        if sState == sm.AVOID_L:
            # 敵を検出して左に移動し始めた時間を記録
            if enemy_detected_start_time is None:
                enemy_detected_start_time = time.time()
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 90)  # 左モーターのスピード
            ClsDmc.driveMotor(1, 0, 50)  # 右モーターのスピード
        elif sState == sm.AVOID_R:
            # 左移動の終了時間を計測し、その時間分だけ右移動
            if enemy_detected_start_time is not None:
                enemy_detected_duration = time.time() - enemy_detected_start_time
                enemy_detected_start_time = None  # タイマーをリセット

            # 右に移動する時間を左移動した時間に基づいて計算
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 50)  # 左モーターのスピード
            ClsDmc.driveMotor(1, 0, 90)  # 右モーターのスピード
            time.sleep(enemy_detected_duration)  # 左移動した時間分右に移動

            # 右移動が完了したら、敵検出時間をリセット
            enemy_detected_duration = 0

        elif sState == sm.IDLE:
            ClsDmc.stop()
        elif sState == sm.FORWARD:
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 100)
            ClsDmc.driveMotor(1, 0, 100)
        elif sState == sm.LEFT:
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 100)
            ClsDmc.driveMotor(1, 0, 60)
        elif sState == sm.RIGHT:
            ClsDmc.stop()
            ClsDmc.driveMotor(0, 0, 60)
            ClsDmc.driveMotor(1, 0, 100)

        if vEnemyInfo[0] != -1:
            cv2.line(imDisplay, (vEnemyInfo[0], 1), (vEnemyInfo[0], sHeight), (0,255,0))
        if vFlagInfo[0] != -1:
            cv2.line(imDisplay, (vFlagInfo[0], 1), (vFlagInfo[0], sHeight), (255, 0, 0))
        if sPreviousState != sState:
            print('current state is :', sState)

    # 画像の表示 ----------------------------------------------
    if sFrame % sDisplayRate == 0:
        cv2.imshow('input', imDisplay)
        #cv2.imshow('red', imRedBinary)
        #cv2.imshow('green', imGreenBinary)

    # コマンドの処理 --------------------------------------------
    if sKey == ord('q'):
        break

    # フレーム番号の更新 ----------------------------------------    
    if sFrame == 999:
        sFrame = 0
    else:
        sFrame =sFrame + 1

# 終了処理 ----------------------------------------------------
ClsDmc.stop()            
cv2.destroyAllWindows()
videoCap.release()