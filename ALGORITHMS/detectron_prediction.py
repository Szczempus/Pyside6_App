import os
import cv2
# from sahi.model import Detectron2DetectionModel
# from sahi.predict import get_sliced_prediction
from math import floor
import matplotlib.pyplot as plt
from detectron2.utils.visualizer import Visualizer
from detectron2.engine import DefaultPredictor
from detectron2 import config, model_zoo


def config_init(train_dataset: str, iterations: int, im_batch_size: int, num_of_classes: int,
                test_dataset=None,
                model_weights_path=None):
    cfg = config.get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = train_dataset
    if test_dataset is not None:
        cfg.DATASETS.TEST = test_dataset
    else:
        cfg.DATASETS.TEST = []

    # 8 have the best time results
    cfg.DATALOADER.NUM_WORKERS = 8
    if model_weights_path is not None:
        cfg.MODEL.WEIGHTS = model_weights_path
    else:
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = im_batch_size
    cfg.SOLVER.BASE_LR = 0.00001
    cfg.SOLVER.MAX_ITER = iterations
    cfg.SOLVER.STEPS = []
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = num_of_classes
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.TEST.DETECTIONS_PER_IMAGE = 2000
    cfg.SOLVER.AMP.ENABLED = True
    cfg.INPUT.FORMAT = "BGR"
    # cfg.INPUT.MIN_SIZE_TEST = 0
    # cfg.INPUT.MIN_SIZE_TEST = 65535
    return cfg


def prediction(cfg, img, model_path=None, score_thresh=None):
    if model_path is None:
        if os.path.exists(os.path.join(cfg.OUTPUT_DIR, 'salata_15_07.pth')):
            cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, 'salata_15_07.pth')
        else:
            raise NameError('No model in default path. Please check it or pass correct path')
    else:
        if os.path.exists(model_path):
            cfg.MODEL.WEIGHTS = model_path
        else:
            raise NameError('Incorrect path to model. Please check it and ty again')
    if score_thresh is None:
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    else:
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh

    # filename, file_extension = os.path.splitext(img_path)

    predictor = DefaultPredictor(cfg)

    im = img
    im_copy = im
    im_w = im.shape[1]
    im_h = im.shape[0]

    num_of_col = 1
    num_of_row = 1

    more_tiles = False

    if (im_w or im_h) > 1000:
        num_of_col = (im_w // 254)
        num_of_row = (im_h // 254)
        more_tiles = True

    num_of_instances = 0
    tile_w, tile_h = int(floor(im_w / num_of_col)), int(floor(im_h / num_of_row))

    # TODO Obczaić jak działa metoda tqdm.update i zamenić ją z obecnym range'm
    for pos_y in range(0, im_h, tile_h):
        for pos_x in range(0, im_w, tile_w):
            tile = im[pos_y:pos_y + tile_h, pos_x:pos_x + tile_w]
            outputs = predictor(tile)
            num_of_instances += len(outputs['instances'])
            v = Visualizer(tile[:, :, ::-1], metadata=None, scale=1)
            out = v.draw_instance_predictions(outputs['instances'].to('cpu'))
            # out = v.draw_sem_seg(outputs['sem_seg'].to('cpu'))
            if not more_tiles:
                # cv2.imshow("Predictions tile", out.get_image()[:, :, ::-1])
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                im_copy = out.get_image()[:, :, ::-1]
            else:
                im_copy[pos_y:pos_y + tile_h, pos_x:pos_x + tile_w] = out.get_image()[:, :, ::-1]

    return im_copy


if __name__ == "__main__":

    model_path = "./model_final.pth"
    # try:
    #     detection_model = Detectron2DetectionModel(
    #         model_path=model_path,
    #         config_path=model_path,
    #         confidence_threshold=0.5,
    #         image_size=256,
    #         device="cuda:0"
    #     )
    # except Exception as e:
    #     print(e)
    #
    # # cfg = config_init("", 4000, 8, 1)
    # try:
    #     image = cv2.imread(
    #         r"C:\Users\quadro5000\PycharmProjects\detectron2_training\detectron2\predicted_images\OSAVI_mod.png")
    #     result = get_sliced_prediction(image, detection_model, slice_width=256, slice_height=256,
    #                                    overlap_height_ratio=0.2,
    #                                    overlap_width_ratio=0.2)
    #
    # except Exception as e:
    #     print(e)
    #
    # plt.imshow(image)
    # plt.show()
