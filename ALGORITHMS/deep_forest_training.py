import labelbox
import pandas as pd
import os
from sahi.slicing import slice_image
import torch
from deepforest import main
from deepforest import get_data
import tempfile

"""
Skrypt ponownie trenuje sieć RetinaNet na modelu deepforest.
Adnotacje pisane są w pliku .csv w formacie:
    path/to/image1.jpg, x1, y1, x2, y2, class_name
    path/to/image2.jpg, x1, y1, x2, y2, class_name
    ...
"""


def slice():
    CWD = os.getcwd()

    image = "\\Las19.jpg"

    path = CWD + image

    slice_image_result = slice_image(image=path, output_dir=CWD + "\\sliced19\\",
                                     output_file_name="Las19_sliced", slice_width=2000,
                                     slice_height=2000)

    print(slice_image_result)


def read_csv(path):
    df = pd.read_csv(path)

    df: pd.DataFrame = df.drop(["imageId", "width", "height", "imageUrl"], axis=1)

    df: pd.DataFrame = df.rename(columns={"imageName": "image_path", "class": "label"})

    filenames = df["image_path"].to_numpy()

    for i in range(len(filenames)):
        filenames[i] = filenames[i] + ".jpg"

    df["image_path"]: pd.DataFrame = filenames

    df: pd.DataFrame = df.reindex(columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"])

    df.to_csv("sliced/tuszyma_transfer_learning.csv", index=False)

    print(df)


def trainig():
    model = main.deepforest()
    model.use_release()
    CWD = os.getcwd()

    annotations = get_data(CWD + "\\sliced\\tuszyma_transfer_learning.csv")

    model.config['gpus'] = 1
    model.config['workers'] = 10
    model.config['batch_size'] = 5

    model.config['train']['epochs'] = 100
    model.config['train']['csv_file'] = annotations
    model.config['train']['root_dir'] = os.path.dirname(annotations)
    model.config['train']['fast_dev_run'] = False

    # loader = model.train_dataloader()

    # print(loader)
    print(model)

    # model.create_trainer()
    model.create_trainer(amp_backend="apex", enable_progress_bar=True)
    #
    model.trainer.fit(model)
    #
    tmpdir = tempfile.TemporaryDirectory().name
    # print(tmpdir)
    #
    model.trainer.save_checkpoint(r"{}\tuszyma.pl".format(tmpdir))
    #
    model_path = os.path.dirname(annotations)
    #
    torch.save(model.state_dict(), "tuszyma.pth")


def annotation_import(path: str, api_key):
    from labelbox.schema.ontology import OntologyBuilder, Tool, Classification, Option, Relationship
    from labelbox import Client, LabelImport, LabelingFrontend, MALPredictionImport, Project
    from labelbox.data.annotation_types import (
        Label, ImageData, ObjectAnnotation, MaskData,
        Rectangle, Point, Line, Mask, Polygon,
        Radio, Checklist, Text,
        ClassificationAnnotation, ClassificationAnswer
    )
    from labelbox.data.serialization import NDJsonConverter
    import uuid
    import json
    import numpy as np

    # CWD = os.getcwd()
    # csv_file = CWD + path
    #
    # df = pd.read_csv(csv_file)
    #
    # annotations = df.to_numpy()
    #
    # for annotation in annotations:


    client = Client(api_key=api_key)

    project: Project = client.get_project('cl0i05w3f9zby0zbz9pwu4ccu')

    print(project.name, project.uid)

    datasets = project.datasets

    print(datasets.source)


    # ontology_builder = OntologyBuilder(
    #     tools=[
    #         Tool(tool=Tool.Type.BBOX, name="box"),
    #         Tool(tool=Tool.Type.LINE, name="line"),
    #         Tool(tool=Tool.Type.POINT, name="point"),
    #         Tool(tool=Tool.Type.POLYGON, name="polygon"),
    #         Tool(tool=Tool.Type.SEGMENTATION, name="mask")],
    #     classifications=[
    #         Classification(class_type=Classification.Type.TEXT, instructions="text"),
    #         Classification(class_type=Classification.Type.CHECKLIST, instructions="checklist", options=[
    #             Option(value="first_checklist_answer"),
    #             Option(value="second_checklist_answer")
    #         ]),
    #         Classification(class_type=Classification.Type.RADIO, instructions="radio", options=[
    #             Option(value="first_radio_answer"),
    #             Option(value="second_radio_answer")
    #         ]),
    #     ])
    #
    # mal_project = client.create_project(name="image_mal_project")
    # li_project = client.create_project(name="image_label_import_project")
    # dataset = client.create_dataset(name="annotation_import_demo_dataset")
    # test_img_url = "https://raw.githubusercontent.com/Labelbox/labelbox-python/develop/examples/assets/2560px-Kitano_Street_Kobe01s5s4110.jpg"
    # data_row = dataset.create_data_row(row_data=test_img_url)
    # editor = next(client.get_labeling_frontends(where=LabelingFrontend.name == "Editor"))
    #
    # mal_project.setup(editor, ontology_builder.asdict())
    # mal_project.datasets.connect(dataset)
    #
    # li_project.setup(editor, ontology_builder.asdict())
    # li_project.datasets.connect(dataset)
    #
    # point = Point(x=100, y=100)
    # point_annotation = ObjectAnnotation(value=point, name="point")
    #
    # rectangle = Rectangle(start=Point(x=30, y=30), end=Point(x=200, y=200))
    # rectangle_annotation = ObjectAnnotation(value=rectangle, name="box")
    #
    # line = Line(points=[Point(x=60, y=70), Point(x=65, y=100), Point(x=80, y=130), Point(x=40, y=200)])
    # line_annotation = ObjectAnnotation(value=line, name="line")
    #
    # polygon = Polygon(points=[Point(x=100, y=100), Point(x=110, y=110), Point(x=130, y=130), Point(x=170, y=170),
    #                           Point(x=220, y=220)])
    # polygon_annotation = ObjectAnnotation(value=polygon, name="polygon")
    #
    # array = np.zeros([128, 128, 3], dtype=np.uint8)
    # mask_data = MaskData(arr=array)
    # mask = Mask(mask=mask_data, color=(0, 0, 0))
    # mask_annotation = ObjectAnnotation(value=mask, name="mask")
    #
    # text = Text(answer="the answer to the text question")
    # text_annotation = ClassificationAnnotation(value=text, name="text")
    #
    # checklist = Checklist(answer=[ClassificationAnswer(name="first_checklist_answer"),
    #                               ClassificationAnswer(name="second_checklist_answer")])
    # checklist_annotation = ClassificationAnnotation(value=checklist, name="checklist")
    #
    # radio = Radio(answer=ClassificationAnswer(name="second_radio_answer"))
    # radio_annotation = ClassificationAnnotation(value=radio, name="radio")
    #
    # image_data = ImageData(uid=data_row.uid)
    #
    # label = Label(
    #     data=image_data,
    #     annotations=[
    #         point_annotation, rectangle_annotation, line_annotation, polygon_annotation, mask_annotation,
    #         text_annotation, checklist_annotation, radio_annotation
    #     ]
    # )
    #
    # # Create urls to mask data for upload
    # def signing_function(obj_bytes: bytes) -> str:
    #     url = client.upload_data(content=obj_bytes, sign=True)
    #     return url
    #
    # label.add_url_to_masks(signing_function)
    #
    # mal_label = Label(
    #     data=image_data,
    #     annotations=[
    #         point_annotation, rectangle_annotation, line_annotation, polygon_annotation, mask_annotation,
    #         text_annotation, checklist_annotation, radio_annotation
    #     ]
    # )
    #
    # label.add_url_to_masks(signing_function)
    #
    # mal_label.assign_feature_schema_ids(ontology_builder.from_project(mal_project))
    #
    # ndjson_labels = list(NDJsonConverter.serialize([mal_label]))
    #
    # upload_job = MALPredictionImport.create_from_objects(
    #     client=client,
    #     project_id=mal_project.uid,
    #     name="upload_label_import_job",
    #     predictions=ndjson_labels)
    #
    # print("Errors:", upload_job.errors)


if __name__ == "__main__":
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbDA5bmprd2s1b2M3MHo3bzRidnM5ZzZoIiwib3JnYW5pemF0aW9uSWQiOiJjbDA5bmprdng1b2M2MHo3bzFnNXIyNmdiIiwiYXBpS2V5SWQiOiJjbDBpM3g4YzlnYjN2MHpiazlwZzg3eWgzIiwic2VjcmV0IjoiNmM2YjNiYzllNGZlNGJkNzk4YTUwMjM1NDVlNjFiNTkiLCJpYXQiOjE2NDY3NDI0MjYsImV4cCI6MjI3Nzg5NDQyNn0.PI7YFV_m5idr_v8Z3hpWCQel_kK1pt0vG6i6JK3gWBM"
    annotation_import("\\sliced\\tuszyma_transfer_learning.csv", API_KEY)
    # slice()
    # read_csv(r"C:\Users\quadro5000\Downloads\tuszyma-2022-03-04T033748.csv")
    # trainig()
    pass
