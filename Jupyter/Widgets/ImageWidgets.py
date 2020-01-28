import ipywidgets


def create_image_from_file(filename, image_square=28):

    with open(filename, "rb") as file:
        image = file.read()
        image_object = ipywidgets.Image(
            value=image,
            format='png',
            width=image_square,
            height=image_square,
        )

    return image_object


def change_image_from_file(filename, existing_widget):
    with open(filename, "rb") as file:
        image = file.read()
        existing_widget.value = image
