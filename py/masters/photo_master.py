from PIL import Image
from io import BytesIO


def get_new_photo(file):
    try:
        image = Image.open(BytesIO(file))

        bw_image = image.convert('L')

        output_stream = BytesIO()
        bw_image.save(output_stream, format='JPEG')
        output_stream.seek(0)

        return output_stream

    except:
        return None


if __name__ == "__main__":
    pass
