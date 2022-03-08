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


if __name__ == "__main__":
    # slice()
    # read_csv(r"C:\Users\quadro5000\Downloads\tuszyma-2022-03-04T033748.csv")
    trainig()
    pass
