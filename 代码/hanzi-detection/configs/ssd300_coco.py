# model settings
model = dict(
    type='SingleStageDetector',
    pretrained='ssdvgg2.pth',
    backbone=dict(
        type='SSDVGG',
        input_size=300,
        depth=16,
        with_last_pool=False,
        ceil_mode=True,
        out_indices=(3, 4),
        out_feature_indices=(22, 34),
        l2_norm_scale=20),
    neck=None,
    bbox_head=dict(
        type='SSDHead',
        input_size=300,
        in_channels=(512, 1024, 512, 256, 256, 256),
        num_classes=1+1,
        anchor_strides=(8, 16, 32, 64, 100, 300),
        basesize_ratio_range=(0.15, 0.9),
        anchor_ratios=([2], [2, 3], [2, 3], [2, 3], [2], [2]),
        target_means=(.0, .0, .0, .0),
        target_stds=(0.1, 0.1, 0.2, 0.2)))
train_cfg = dict(
    assigner=dict(
        type='MaxIoUAssigner',
        pos_iou_thr=0.5,
        neg_iou_thr=0.5,
        min_pos_iou=0.,
        ignore_iof_thr=-1,
        gt_max_assign_all=False),
    smoothl1_beta=1.,
    allowed_border=-1,
    pos_weight=-1,
    neg_pos_ratio=3,
    debug=False)
test_cfg = dict(
    nms=dict(type='nms', iou_thr=0.45),
    min_bbox_size=0,
    score_thr=0.02,
    max_per_img=200)
# model training and testing settings
# dataset settings 


dataset_type= 'KittiDataset'
label_vocab= ['background', 'car', 'cyclist', 'pedestrian']
dataset_root= '/home/chenriquan/Datasets/KITTIdevkit/KITTI/'
ann_root = dataset_root + 'split_1:1/'
data_root = dataset_root + 'data_object_image_2/'
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[1, 1, 1], to_rgb=True)
data = dict(
    imgs_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
            type=dataset_type,
            ann_file=ann_root + 'train.pkl',
            img_prefix=data_root + 'training/image_2/',
            img_scale=(1300, 800),
            img_norm_cfg=img_norm_cfg,
            size_divisor=None,
            flip_ratio=0.5,
            with_mask=False,
            with_crowd=False,
            with_label=True,
            test_mode=False,
            extra_aug=dict(
                photo_metric_distortion=dict(
                    brightness_delta=32,
                    contrast_range=(0.5, 1.5),
                    saturation_range=(0.5, 1.5),
                    hue_delta=18),
                expand=dict(
                    mean=img_norm_cfg['mean'],
                    to_rgb=img_norm_cfg['to_rgb'],
                    ratio_range=(1, 4)),
                random_crop=dict(
                    min_ious=(0.1, 0.3, 0.5, 0.7, 0.9), min_crop_size=0.3)),
            resize_keep_ratio=False),
    val=dict(
        type=dataset_type,
        ann_file=ann_root + 'test.pkl',
        img_prefix=data_root + 'training/image_2/',
        img_scale=(1300, 800),
        img_norm_cfg=img_norm_cfg,
        size_divisor=None,
        flip_ratio=0,
        with_mask=False,
        with_label=False,
        test_mode=True,
        resize_keep_ratio=False),
    test=dict(
        type=dataset_type,
        ann_file=ann_root + 'test.pkl',
        img_prefix=data_root + 'training/image_2/',
        img_scale=(1300, 800),
        img_norm_cfg=img_norm_cfg,
        size_divisor=None,
        flip_ratio=0,
        with_mask=False,
        with_label=False,
        test_mode=True,
        resize_keep_ratio=False))
# optimizer
optimizer = dict(type='SGD', lr=2e-3, momentum=0.9, weight_decay=5e-4)
optimizer_config = dict()
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[8, 11])
checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs = 12
dist_params = dict(backend='nccl')
log_level = 'INFO'
kitti_ap_hook_cfg = dict(
    eval_cpg_path = 'tools/kitti_evaluate/evaluate_object',
    dataset_root = dataset_root,
    label_vocab = label_vocab,
    interval = 10*50
)
import time
tid = time.strftime("%Y%m%d_%H%M%S", time.localtime())
work_dir = './work_dirs_ssd/faster_rcnn_r50_fpn_kitti_'+tid
load_from = None
resume_from = None
workflow = [('train', 1)]
