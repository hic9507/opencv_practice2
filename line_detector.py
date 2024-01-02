import math
import cv2
import copy


def dist(P, A, B):

    area = abs((A[0] - P[0]) * (B[1] - P[1]) - (A[1] - P[1]) * (B[0] - P[0]))
    AB = ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5
    return (area / AB)


def detector(A, B, image, image_gray):

    print("---------- 픽셀 돌아가며 탐색 중 ----------")

    for i in range(len(A)):
        image = cv2.circle(image, (int(A[i][0]), int(A[i][1])), 4, (0, 255, 0),1)
    for i in range(len(B)):
        image = cv2.circle(image, (int(B[i][0]), int(B[i][1])), 4, (0, 255, 0), 1)

    blur = cv2.GaussianBlur(image_gray, ksize=(5, 5), sigmaX=0)
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    edged = cv2.Canny(blur, 14, 50)
    # edged = cv2.Canny(blur, 10, 250)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  # cv2.getStructuringElement(shape, ksize, [,anchor])

    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    # cv2.imshow('aaa', closed)
    # cv2.waitKey()

    num_of_line = len(A)*len(B)
    cnt_under_one = [0 for i in range(num_of_line)]


    ########## 이 두 for문은 25가지 대각선 고르기 위한 for문
    for q in range(len(A)):
        for w in range(len(B)):

            #탐색 영역 박스 그리기 파란색
            img = copy.deepcopy(image)
            img = cv2.rectangle(img, (A[q][0], A[q][1]), (B[w][0], B[w][1]), (255, 0, 0), 2)

            cnt_under_one[q *len(A) + w]=0

            ######### 이거는 한 대각선에 대해서 255점과 거리 계산하기 위한 for문
            if A[q][1] <= B[w][1]:
                for i in range(A[q][1] , B[w][1]+1):
                    if A[q][0] <= B[w][0]:
                        for j in range(A[q][0], B[w][0]+1):
                            if closed[i][j] == 255: ##i:y, j:x
                                d = dist((j, i), A[q], B[w])
                                if d < 3:
                                    img = cv2.circle(img, (j, i), 4, (0, 255, 255), 1)
                                    cnt_under_one[q * len(A) + w] += 1  # 각 대각선(25개)에 대한 흰점<1 의 카운트값 저장
                    else :
                        for j in range(B[w][0], A[q][0] + 1):
                            if closed[i][j] == 255: ##i:y, j:x
                                d = dist((j,i), A[q], B[w])
                                if d < 3:
                                    img = cv2.circle(img, (j,i), 4 , (0,255,255),1)
                                    cnt_under_one[q*len(A) + w] += 1 #각 대각선(25개)에 대한 흰점<1 의 카운트값 저장
            else:
                for i in range(B[w][1] ,A[q][1] +1):
                    if A[q][0] <= B[w][0]:
                        for j in range(A[q][0], B[w][0]+1):
                            if closed[i][j] == 255: ##i:y, j:x
                                d = dist((j, i), A[q], B[w])
                                if d < 3:
                                    img = cv2.circle(img, (j, i), 4, (0, 255, 255), 1)
                                    cnt_under_one[q * len(A) + w] += 1  # 각 대각선(25개)에 대한 흰점<1 의 카운트값 저장
                    else :
                        for j in range(B[w][0], A[q][0] + 1):
                            if closed[i][j] == 255: ##i:y, j:x
                                d = dist((j,i), A[q], B[w])
                                if d < 3:
                                    img = cv2.circle(img, (j,i), 4 , (0,255,255),1)
                                    cnt_under_one[q*len(A) + w] += 1 #각 대각선(25개)에 대한 흰점<1 의 카운트값 저장
            # ### 한 대각선 당 검출된 흰색 픽셀들을 노란색으로 표시 : 시각화
            cv2.imshow('img', img)
            cv2.waitKey(0)
            # print("cnt_under_one : ",cnt_under_one[q*len(A) + w])



    cnt_max = max(cnt_under_one) #이거는 아까 리스트 최댓값
    index = cnt_under_one.index(cnt_max) # 이거는 위 리스트 인덱스


     #이거는 for 문이랑 같은 원리라서 나중에 하는겅고
    qq = int(math.trunc(float(index/len(A))))
    ww = int(index%len(B))

    #### 찾은 라인 그리기
    cv2.line(image, (A[qq][0], A[qq][1]), (B[ww][0], B[ww][1]), (255,0,0), 3)
    # cv2.line(closed, (A[qq][0], A[qq][1]), (B[ww][0], B[ww][1]), (255,0,0), 3)



    ##이건 원래 라이 (form YOLO) = red
    # cv2.line(image, (A[int(len(A)/2)][0], A[int(len(A)/2)][1]), (B[int(len(B)/2)][0], B[int(len(B)/2)][1]), (0,0,255),3)

    print("탐색 완료, 라인 검출")


    # cv2.imshow('closed_resuld', closed)

    cv2.imshow('image', image)
    # cv2.waitKey()
    while(1):
        k = cv2.waitKey()
        if k==27:    # Esc key to stop
            break


    return [A[qq][0], A[qq][1]], [B[ww][0], B[ww][1]]