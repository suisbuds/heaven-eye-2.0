# Heaven Eye

## Backgrounds

Heaven Eye 项目旨在解决现代城市管理中人流和车流检测的复杂需求
为提升交通管理效率, 我们开发了基于 PySide6 和 Qt 框架的桌面应用程序 Heaven Eye, 并集成了分类, 检测, 姿态预估和分割模型, 以提供可靠的交通流量数据支持

## Project Structure

```shell
.
├── assets
├── config
├── data
│   ├── test
│   │   ├── images
│   │   └── labels
│   ├── train
│   │   ├── images
│   │   └── labels
│   └── valid
│       ├── images
│       └── labels
├── docs
├── img
├── models
│   ├── classify
│   ├── detect
│   ├── pose
│   └── segment
├── runs
├── ui
└── utils
```
## Features

- [x] 对象检测
- [x] 姿势识别
- [x] 实例分割
- [x] 分类任务
- [x] 图像推理
- [x] 视频推理
- [x] 模型选择
- [x] 置信度阈值调节
- [x] 重叠度阈值调节
- [x] 延迟时间调节
- [x] 推理结果保存
- [x] Docker 打包镜像 

## UI 

### Tech

- GUI 基于 Python 和 Pyside6 (Qt 6) 实现
  - PySide6 是 Qt 6 框架的官方 Python 绑定, 允许开发者在 Python 环境下开发复杂的 Qt 应用, 并能利用 Qt Designer 简化 UI 开发
  - Qt 框架支持跨平台应用程序开发
  - 利用 pyside6-uic 将设计文件 home.ui 转换为 Python 模块
  - 利用 pyside6-rcc 将资源文件 resources.qrc 编译为 Python 模块

### Design

- 界面
  - home page
    - 选择检测模式
  - detect page
    - content
      - 实时显示检测目标、类型、进度和帧率
      - 源文件和检测结果对比
      - 动态控制检测过程
    - navgation panel
      - 打开检测文件 (*.mp4 *.mkv *.avi *.flv *.jpg *.png)
      - 返回 home page
    - settings panel
      - 更换模型
      - 调节置信度阈值
      - 调节重叠度阈值
      - 调节延迟时间
      - 保存推理结果和输入源 (labels.txt)

![](/assets/1.png)

![](/assets/2.png)

- 交互
  - navgation panel 和 settings panel 动画
  - 检测分割线动画
  - 仿 mac 窗口按钮, 窗口缩放动画

- 风格
  - 基于 Material You Guidelines 设计
    - 统一 icon, 圆角和字体 (Segoe UI)
    - Heaven Eye 提供舒适视觉体验的色彩组合, 并利用色彩的变化表现不同的氛围, 达到功能性和美学的平衡

![](/assets/3.png)

![](/assets/4.webp) 

## Highlights & Difficulties

### 模型训练

- 利用 [Roboflow](https://roboflow.com/?ref=ultralytics) 获取数据集, 并进行数据增强
- 基于 Ultralytics YOLOv8 Nano 模型, 针对准备的数据集不断调整训练参数 (epochs、batch、lr、imgsz、optimizer) 以进行微调
- 利用验证集和测试集评估模型训练的效果 (mAP, precision, recall) 并持续优化
- 将训练好的模型导出为不同格式 (Pytorch, ONNX, TensorRT) 

**训练流程**

![](/assets/7.png)

**YOLOv8 模型架构**

- Backbone: 主干网络负责提取图像的特征
  - P1到P5: 特征层, 每层的输入和输出尺寸逐渐减小, 但特征的抽象程度增加
  - Conv: 使用卷积进行特征提取
  - C2f: 特征提取模块
  - SPPF模块: 空间金字塔池化, 让模型理解图像中不同尺度的物体
- Head: 头部根据提取的特征进行物体检测
  - Upsample: 上采样将特征图的尺寸放大, 帮助模型识别小物体
  - Concat: 将多个特征图连接起来, 融合不同层的特征
  - Detect: 模型的最终输出层
- Loss: 损失函数衡量模型预测与真实结果的差距
  - Cls: 分类损失
  - Bbox: 边界框损失
  - Loss: 总损失

![](/assets/5.webp)

**模型对比**

![](/assets/6.avif)


### Heaven Eye 模型集成

**YoloPredictor** 

统一加载模型并执行检测、分类、分割和姿态预估任务

- 初始化配置  
  - `get_cfg(cfg, overrides)` 解析配置参数
  - 指定结果文件的保存路径
- 模型管理
  - `setup_model` 加载模型
  - 模型预热, 优化推理速度
- 获取检测源 
  - 在 detect page 选择检测源 (*.mp4 *.mkv *.avi *.flv *.jpg *.png)
  -  `setup_source` 建立数据集迭代器, 持续读取数据集中的图片或视频帧
- Preprocess  
  - 分类: 调用 `classify_preprocess` 将图像转换为分类模型兼容的格式  
  - 检测, 分割, 姿态: 调用 `preprocess` 进行图像尺寸变换、类型转换
- Inference
  - 接收输入图像执行模型推理, 得到 `preds` 存储原始预测结果
- Postprocess
  - 执行对应 `postprocess` 进行 NMS, 坐标缩放, Mask 解析, 关键点转换等计算, 并将 `preds` -> `Results`
  - Task
    - `postprocess`  
    - `classify_postprocess`  
    - `segment_postprocess`  
    - `pose_postprocess`  
- 结果输出
  - `write_results` 将 `Results` 绘制到图像上, 并利用信号发送到 `MainWindow`  实时展示结果和统计信息
  - 更新进度条和帧率信息
- 异常处理
  - 捕捉推理过程中的异常, 并打印错误信息

## Details

- `conf_thres`: 过滤模型预测的结果, 能够减少误报，提高检测的准确性
- `iou_thres`: 非极大值抑制 (NMS) 中使用, 以移除多余检测框
  - 高阈值允许更多重叠框, 适用于密集目标检测场景
  - 低阈值会过滤掉重复检测框, 适用于目标分散检测场景
- `speed_thres`: 调节推理速度, 以便同步视频帧率和降低处理负载
- `labels.txt`: `<class_id> <x_center> <y_center> <width> <height>`
  - `save_labels` 将标签信息写入 labels.txt
  - 统计交通流量并可视化结果
  - 生成标注数据, 进一步微调模型





