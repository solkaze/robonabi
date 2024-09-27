import cv2
import numpy as np

def preprocess(imInput):
	# 入力画像をHSVに変換し、平滑化
	imInputHSV = cv2.cvtColor(imInput, cv2.COLOR_BGR2HSV)
	imGaussianHSV = cv2.blur(imInputHSV, (3, 3))

	return imGaussianHSV

def locateFlag(imInputHSV):
	# 対象色の定義１（赤の場合）
	vMinHSV = np.array([0,180,0])
	vMaxHSV = np.array([10,255,255])
	imRed1 = cv2.inRange(imInputHSV, vMinHSV, vMaxHSV)

	# 対象色の定義２（赤の場合は色相が最大と最小に分かれるため2つ必要）
	vMinHSV = np.array([160,180,0])
	vMaxHSV = np.array([180,255,255])
	imRed2 = cv2.inRange(imInputHSV, vMinHSV, vMaxHSV)

	# 対象色のエリア画像の作成
	imRed = imRed1 + imRed2
	imRedBinary = imRed / 255

	# 対象色エリア（最も縦に長いもの）の水平位置の割り出し
	vSumRedVertical = np.sum(imRedBinary, axis=0)
	sMaxIndex = vSumRedVertical.argmax()
	
	# 対象色エリアの縦の長さが5画素よりも大きい場合、ターゲットに設定
	if vSumRedVertical[sMaxIndex] > 5:
		sHorizontal = sMaxIndex
		sVertical = -1
		sSize = vSumRedVertical[sMaxIndex]
	else:
		sHorizontal = -1
		sVertical = -1
		sSize = -1

	return (sHorizontal, sVertical, sSize), imRedBinary

def locateEnemy(imInputHSV):
	imGreenBinary = imInputHSV

	sHorizontal = -1
	sVertical = -1
	sSize = -1

	return (sHorizontal, sVertical, sSize), imGreenBinary