import subprocess
from PIL import Image
import time
import random
import os



def jump(distance):
    a = random.uniform(1.390, 1.394)
    # 控制随机数的精度round(数值，精度)
    b = random.randint(2, 5)
    print('按压系数:%.5f' % round(a, b), end='   ')
    press_time = distance * round(a, b)       #按压时间系数
    press_time = max(press_time, 250)
    press_time = int(press_time)
    point = (random.randint(715, 923), (random.randint(1412, 1658)))
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {time}'.format(
        x1 = point[0],
        y1 = point[1],
        x2 = point[0] +random.randint(1, 3),
        y2 = point[1] +random.randint(1, 3),
        time = press_time
    )

    os.system(cmd)

def find_piece_board(img_path):
    #找到棋子棋盘坐标的位子
    img = Image.open(img_path)
    #获取图片尺寸
    w, h = img.size
    img_pixel = img.load()
    #确定搜索新棋盘起始高度，以50为布长开始找
    stary_y = None
    stary_xx = 0

    for i in range(int(h/3), int(h*2/3), 10):
        first_pixel = img_pixel[0, i]
        #循环这一行其它的点
        for j in range(1, w):
            pixel = img_pixel[j, i]
            #pixel里面有4个值，前3个是表示颜色，最后一个是透明度
            if pixel[0]!=first_pixel[0] or pixel[1]!=first_pixel[1] or pixel[2]!=first_pixel[2]:
                if not ((50<pixel[0]<60) and (53<pixel[1]<63) and (95<pixel[2]<105)):
                    stary_y = i - 10
                    stary_xx = j

                    break
        if stary_y:
            break


    #找棋子
    left = 0
    right = 0
    piece_y_max = 0
    #从新奇盘顶点开始找
    for i in range(stary_y, int(h*2/3)):
        flag = True

        #左右去掉1/8节约内存
        for j in range(int(w/8), int(w*7/8)):
            pixel = img_pixel[j, i]
            if (50<pixel[0]<60) and (53<pixel[1]<63) and (95<pixel[2]<105):
                if flag:
                    left = j
                    flag = False

                right = j
                piece_y_max = max(i, piece_y_max)

    piece_x = (left+right)//2
    piece_y = piece_y_max - 18

    #找棋盘
    for i in range(stary_y, int(h*2/3)):
        flag = True
        first_pixel = img_pixel[0, i]
        for j in range(stary_xx-30, stary_xx+30):
            pixel = img_pixel[j, i]

            if abs(pixel[0] -first_pixel[0]) + abs(pixel[1] -first_pixel[1]) + abs(pixel[2] -first_pixel[2]) > 5:
                    if not ((50<pixel[0]<60) and (53<pixel[1]<63) and (95<pixel[2]<105)) :
                        if flag:
                            left = j
                            right = j
                            flag = False
                        else:
                            right = j

        if not flag:
            break

    board_x = (left+right)//2
    top_point = img_pixel[board_x, i]


    #从顶点往下+280反向找下底点
    for k in range(i+280, i, -1):
        pixel = img_pixel[board_x, k]
        if abs(pixel[0] - top_point[0]) + abs(pixel[1] - top_point[1]) + abs(pixel[2] - top_point[2]) < 10:
            break

    board_y = (i+k)//2

    return (piece_x, piece_y), (board_x, board_y)



def run():
    #获取手机截图
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    #这是一个二进制数据/系统会自动增加/r/n的换行信息
    screenshot = process.stdout.read()
    print(screenshot)
    screenshot = screenshot.replace(b'\r\n', b'\n')

    with open('autojump.png', 'wb')as f:
        f.write(screenshot)


def game():
    oper = input('请确保手机已连接电脑到电脑ADB，微信跳一跳已到开始界面！确定开始？Y/N：')
    if oper != 'y' and oper != 'Y':
        exit('退出')

    while True:
        run()
        piece, board = find_piece_board('autojump.png')
        print(piece, board, end='   ')
        #计算距离
        # if piece[0] == board[0]:
        #     print('0000')
        #     break
        distance = ((piece[0]-board[0])**2 + (piece[1]-board[1])**2)**0.5
        jump(distance)
        #随机休眠
        a = random.uniform(1, 3)
        b = random.randint(0, 5)
        time_ran = round(a, b)
        time.sleep(time_ran)
        print('休眠时间:%.5f' % time_ran)


if __name__ == '__main__':
    game()