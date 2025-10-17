import uiautomator2 as u2
import time
import tqdm
# 连接设备，引号中的内容可通过adb devices列出后查看序列号
d = u2.connect("172.28.108.96:39771")
# 记录一共截屏多少张
count=0

start_time=time.time()
try:
    while(True):
        # 记录单张截图耗时
        single_pic_start=time.time()
        count+=1
        print("正在处理第"+str(count)+"张截屏")
        time.sleep(4)
        print("点击空白处")
        #需要手动配置空白处的坐标，我这个是在qq聊天标题处
        d.click(601, 184)
        print("点击截屏按钮")
        #需要手动配置悬浮窗的位置、单击为截屏
        d.click(977, 975)
        time.sleep(0.5)
        d(text="长截屏").click()
        print("正在截图中...")
        swipeCount=0
        while(d(text="当前页面中有影响图像拼接效果的内容").exists()==False|d(text="到达最大截屏长度").exists()==False|d(text="已到达页面底部").exists()==False):
            # time.sleep(0.1)
            d.swipe(257,1900,257,31,duration=0.1)
            swipeCount+=1
            print(f"滑动第{swipeCount}次")
            print(f"滑动第{swipeCount}次 ({swipeCount/45*100:.1f}%)", end="\r")
        print("\n截屏完成")
        d(text="完成").click()
        print("第"+str(count)+"张截屏处理完成")
        print("本次截屏处理时间:"+str(time.time()-single_pic_start)+"秒")
        # while(d(text="正在处理").exists()==True):
        #     print("正在处理...")
        time.sleep(6)
        print("开启下一张截屏")
except KeyboardInterrupt:
    print("程序已退出")
    end_time=time.time()
    print(f"执行时间: {end_time - start_time:.6f} 秒")
    print("已保存的图片数量为:"+str(count))
    print("平均截屏时间:"+str((end_time - start_time)/count)+"秒")
