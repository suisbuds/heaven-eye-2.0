import os
import argparse
from ultralytics import YOLO

"""
    python train_yolov8.py --task detect --data ./data/data.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16
    python train_yolov8.py --task classify --data ./data/data.yaml --model yolov8n-cls.pt --epochs 50 --imgsz 224 --batch 32
    python train_yolov8.py --task segment --data ./data/data.yaml --model yolov8n-seg.pt --epochs 150 --imgsz 640 --batch 16
    python train_yolov8.py --task pose --data ./data/data.yaml --model yolov8n-pose.pt --epochs 200 --imgsz 640 --batch 16
"""

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, required=True,
                        help='选择任务类型: detect, classify, segment 或 pose')
    parser.add_argument('--data', type=str, default='./data/data.yaml',
                        help='数据集配置文件 (dataset.yaml)')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='预训练权重文件路径或 ultralytics 模型名')
    parser.add_argument('--epochs', type=int, default=100,
                        help='训练轮数')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='输入图像大小')
    parser.add_argument('--batch', type=int, default=16,
                        help='批量大小')
    parser.add_argument('--val', action='store_true',
                        help='是否进行验证集评估')
    parser.add_argument('--test', action='store_true',
                        help='是否进行测试集评估')
    return parser.parse_args()

def train_yolov8(task: str, data: str, model: str, epochs: int, imgsz: int, batch: int):
    """使用 YOLOv8 进行训练"""
    yolo_model = YOLO(model)

    if task == 'detect':
        yolo_model.train(
            task='detect',
            data=data,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch
        )
    elif task == 'classify':
        yolo_model.train(
            task='classify',
            data=data,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch
        )
    elif task == 'segment':
        yolo_model.train(
            task='segment',
            data=data,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch
        )
    elif task == 'pose':
        yolo_model.train(
            task='pose',
            data=data,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch
        )
    else:
        raise ValueError("任务类型错误，请使用 detect, classify, segment 或 pose")

def evaluate_model(task: str, model_path: str, data: str, imgsz: int, evaluate_type: str):
    """
    使用验证集或测试集评估模型。
    evaluate_type: 'val' 或 'test'
    """
    yolo_model = YOLO(model_path)
    yolo_model.val(task=task, data=data, imgsz=imgsz, split=evaluate_type)

def main():
    opt = parse_opt()
    # 训练
    train_yolov8(
        task=opt.task,
        data=opt.data,
        model=opt.model,
        epochs=opt.epochs,
        imgsz=opt.imgsz,
        batch=opt.batch
    )

    # 获取 best.pt 路径
    best_path = os.path.join('runs', opt.task, 'weights', 'best.pt')

    # 验证集评估
    if opt.val and os.path.exists(best_path):
        evaluate_model(opt.task, best_path, opt.data, opt.imgsz, 'val')

    # 测试集评估
    if opt.test and os.path.exists(best_path):
        evaluate_model(opt.task, best_path, opt.data, opt.imgsz, 'test')

if __name__ == '__main__':
    main()