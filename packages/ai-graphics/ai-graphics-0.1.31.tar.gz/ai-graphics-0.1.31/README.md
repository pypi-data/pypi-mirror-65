# 1、使用方法
```
import cv2  
import graphics as g
```

## 1.1 场景图识别
```
cl = g.Classifier(model_name="../models/classifier.pth", ctx_id=-1)  
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)  
label = cl.predict(src)
```

## 1.2 场景图裁剪
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)  
ic = g.ImageCrop(model_name="../models/basnet.pth", ctx_id=-1)    
bbox = ic.crop_margin(src, (1000, 1000))  
image = ic.crop_image(src, (1000, 1000)) 
```

## 1.3 白底图/透明图裁剪
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)    
bbox = g.Graphics.crop_margin(src, threshold1=15, threshold2=55)
dst = src[bbox[0]:bbox[1] + 1, bbox[2]:bbox[3] + 1]
```

## 1.4 白底图/透明图增加边框
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED) 
dst = g.Graphics.add_border(src, [10, 10, 40, 40], (255, 255, 255))
```

## 1.5 商品图倒影特效
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)  
image = g.Graphics.layer_reflection(src, top=0, down=0.3, transparency=0.15)
```

## 1.6 人物图蒙层特效
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)  
image = g.Graphics.layer_mask(src)
```

## 1.7 图像透明通道融合
```
src = cv2.imread('27.png', cv2.IMREAD_UNCHANGED)  
image = g.Graphics.alpha_compose(src, image, x=0, y=0)
```
        
# 2、安装相关工具以及打包：
```
python -m pip install --user --upgrade setuptools wheel  
python -m pip install --user --upgrade twine  
python setup.py sdist bdist_wheel
```

# 3、在 https://pypi.org/ 或 https://test.pypi.org/ 注册账号 Cachcheng 并上传包
```
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

# 4、查看pypi地址：
```
https://pypi.org/project/ai-graphics/
```

