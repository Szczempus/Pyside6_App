"""
Konieczne biblioteki:
- środowisko, z którego poziomu można uruchomić pakiet deepforest,
- biblioteka sahi,
- biblioteka labelbox

Skrypt ponownie trenuje sieć RetinaNet na modelu deepforest.
Adnotacje pisane są w pliku .csv w formacie:
    path/to/image1.jpg, x1, y1, x2, y2, class_name
    path/to/image2.jpg, x1, y1, x2, y2, class_name
    ...

Kolejność wykonywania skryptu:
1. Pocięcie zdjęcia do folderu funkcją slice_from_path()
2. Wstępna predykcja pociętych zdjęć funkcją fast_prediction()
3. Import danych ze wstępnych predykcji do danego projektu Labelbox API funkcją annotation_import()
4. Poprawka przygotowanych oznaczeń i ich zatwierdzenie na stronie
5. Export adnotacji do formatu .csv funkcją export_labels()
6. Ponowny trening sieci funkcją retraining_custom_model()
"""

import os
import tempfile
import torch
import numpy as np
import pandas as pd
from sahi.slicing import slice_image
from deepforest import main, get_data
from labelbox.schema.dataset import Dataset
from labelbox import Client, MALPredictionImport, Project
from labelbox.data.annotation_types import (
    Label, ImageData, ObjectAnnotation, Rectangle, Point, LabelList)
from labelbox.data.serialization import NDJsonConverter


def fast_prediction(path_to_image_dir: str) -> None:
    """

    :param path_to_image_dir: folder, w którym znajdują się pocięte zdjęcia do wstępnej predykcji
    :return: plik .csv z adnotacjami zapisany w folderze ze zdjęciami o nazwie folderu,
     w którym jest przechowywany
    """

    # Path declaration
    cwd = os.getcwd()
    path =cwd + path_to_image_dir
    print(path)

    # Fast annotations
    model = main.deepforest()
    model.use_amp = True
    model.use_release()
    # annotations = model.predict_file(csv_file=path, root_dir=path, device='cuda' )

    annotations: pd.DataFrame = pd.DataFrame(
        columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"]
    )

    for images in os.listdir(path):
        if images.format() == ('.jpg' or '.png'):
            temp_annotations: pd.DataFrame = model.predict_tile(raster_path=path + "\\" + images,
                                                                return_plot=False,
                                                                patch_size=1000,
                                                                patch_overlap=0.1,
                                                                iou_threshold=0.4,
                                                                thresh=0.2)
            if temp_annotations is None:
                continue
            annotations = annotations.append(temp_annotations, ignore_index=True)
            annotations['image_path'].fillna(images, inplace=True)
            print(annotations)

    print("After loop: ", annotations)

    # Saving to file in content directory
    annotations.to_csv(path + "\\" + path_to_image_dir.split("\\")[1] + ".csv", index=False)


def slice_from_path(path_to_image: str) -> None:
    """

    :param path_to_image: ścieżka z obrazem do pocięcia
    :return: folder z pociętymi obrazami
    """
    cwd = os.getcwd()

    image = path_to_image

    path = image

    slice_image_result = slice_image(image=path, output_dir=cwd + "\\sliced19\\",
                                     output_file_name="Las19_sliced", slice_width=2000,
                                     slice_height=2000)

    print(slice_image_result)


def read_csv(path: str) -> None:
    """

    :param path: ścieżka do folderu z adnotacjami .csv wygenerowanymi z label.ai API
    :return: sformatowany plik zgodny z przyjętym formatem do trenowania deepforest
    """
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


def retraining_custom_model(path: str) -> None:
    """

    :param path: ścieżka z plikiem .csv zgodnym z formatem do trenowania sieci
    deepforest - musi by w tym samym folderze, co pocięte zdjęcia
    :return: nowy zestaw wag
    """

    model = main.deepforest()
    model.use_release()
    cwd = os.getcwd()
    tmpdir = tempfile.TemporaryDirectory().name

    annotations = get_data(cwd + path)

    # annotations = get_data(cwd + "\\sliced19\\tuszyma_transfer_learning.csv")

    # csv = pd.read_csv(annotations)
    # sample_image_path = csv['image_path'][0]
    # raster_path = cwd + "\\sliced19\\" + sample_image_path
    # sample_image = rasterio.open(raster_path)

    model.config['gpus'] = -1
    model.config['workers'] = 10
    model.config['batch_size'] = 10

    model.config['train']['epochs'] = 5
    model.config['train']['csv_file'] = annotations
    model.config['train']['root_dir'] = os.path.dirname(annotations)
    model.config['train']['fast_dev_run'] = False

    # loader = model.train_dataloader()

    print(model.config['train']['root_dir'])
    print(model.config['train']['csv_file'])

    # model.create_trainer()
    model.create_trainer(amp_backend="apex", enable_progress_bar=True)

    model.trainer.fit(model)

    model.trainer.save_checkpoint(r"{}\tuszyma19.pl".format(tmpdir))
    # model_path = os.path.dirname(annotations)

    torch.save(model.state_dict(), "../weights/tuszyma19.pth")


def annotation_import(path: str, api_key):
    """

    :param path: ścieżka do wygenerowanego pliku .csv po wstępnej predykcji
    :param api_key: klucz api konta, w którym jest projekt
    :return: przesłanie adnotacji do projektu na stronie
    """

    # Preparing Labelbox API

    # Accesing to client user
    client = Client(api_key=api_key)

    project: Project = client.get_project('cl0i05w3f9zby0zbz9pwu4ccu')

    # print(project.name, project.uid)

    # Get datasets in project
    datasets = project.datasets()

    # print(type(datasets))

    for dataset in datasets:
        print(dataset.name, dataset.uid)
        if dataset.name == "Las":
            # Get that what we want to label
            working_dataset: Dataset = client.get_dataset(dataset.uid)


    # Preparing csv annotations


    cwd = os.getcwd()
    csv_file = cwd + path

    df = pd.read_csv(csv_file)

    annotations = df.to_numpy()

    list_of_external_ids = annotations[:, 0]

    list_of_external_ids = np.unique(list_of_external_ids)
    # print(list_of_external_ids)

    list_of_external_ids = list_of_external_ids.tolist()


    # Getting data rows

    data_rows = client.get_data_row_ids_for_external_ids(external_ids=list_of_external_ids)

    # print(data_rows.keys())

    # client.get_data_row()

    def signing_function(obj_bytes: bytes) -> str:
        url = client.upload_data(content=obj_bytes, sign=True)
        return url

    for _, key in enumerate(data_rows.keys()):
        # data_row_uid = data_rows[key][0]
        # image_data_rows = working_dataset.data_rows()
        data_row = working_dataset.data_row_for_external_id(key)
        image_to_label = ImageData(uid=data_row.uid)
        # print(image_to_label)
        annotations_labels = []
        for annotation in annotations:
            if annotation[0] == key:
                rectangle = Rectangle(start=Point(x=annotation[1], y=annotation[2]),
                                      end=Point(x=annotation[3], y=annotation[4]))
                rectangle_annotation = ObjectAnnotation(
                                        value=rectangle, name="Tree",
                                        feature_schema_id="cl0i0lmf43u2w10ca1ojfasfs")
                annotations_labels.append(rectangle_annotation)
            else:
                continue

        label = Label(data=image_to_label, annotations=annotations_labels)

        label.add_url_to_masks(signing_function)

        ndjasnon_labels = list(NDJsonConverter.serialize([label]))

        upload_job = MALPredictionImport.create_from_objects(
            client=client,
            project_id=project.uid,
            predictions=ndjasnon_labels,
            name=f"Upload from {key}"
        )

        print(upload_job.errors)


def export_labels(path, api_key):
    """

    :param path: ścieżka do zapisania zmodyfikowanego pliku .csv z adnotacjami
    :param api_key: klucz konta do Labelbox API
    :return: plik .csv z adnotacjami gotowymi do przetrenowania
    """

    cwd = os.getcwd()
    client = Client(api_key=api_key)
    project: Project = client.get_project('cl0i05w3f9zby0zbz9pwu4ccu')

    labels = project.label_generator()
    labels: LabelList = labels.as_list()

    data_frame = pd.DataFrame(columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"])

    for label in labels:
        image_path = label.data.external_id
        for annotation in label.annotations:
            class_name = annotation.name
            x_min = annotation.value.start.x
            y_min = annotation.value.start.y
            x_max = annotation.value.end.x
            y_max = annotation.value.end.y

            data = {"image_path": image_path,
                    "xmin": x_min,
                    "ymin": y_min,
                    "xmax": x_max,
                    "ymax": y_max,
                    "label": class_name}

            data_frame = data_frame.append(data, ignore_index=True)

    data_frame.to_csv(cwd + path, index=False)


if __name__ == "__main__":
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbDA5bmprd2s1b2M3MHo3bzRidnM5ZzZoIiwib3JnYW5pemF0aW9uSWQiOiJjbDA5bmprdng1b2M2MHo3bzFnNXIyNmdiIiwiYXBpS2V5SWQiOiJjbDBpM3g4YzlnYjN2MHpiazlwZzg3eWgzIiwic2VjcmV0IjoiNmM2YjNiYzllNGZlNGJkNzk4YTUwMjM1NDVlNjFiNTkiLCJpYXQiOjE2NDY3NDI0MjYsImV4cCI6MjI3Nzg5NDQyNn0.PI7YFV_m5idr_v8Z3hpWCQel_kK1pt0vG6i6JK3gWBM"
    # fast_prediction("\\sliced19")
    # annotation_import("\\sliced19\\sliced19.csv", API_KEY)
    # export_labels("\\sliced19\\tuszyma_transfer_learning.csv", API_KEY)
    # slice()
    # read_csv(r"C:\Users\quadro5000\Downloads\tuszyma-2022-03-04T033748.csv")
    retraining_custom_model(None)

