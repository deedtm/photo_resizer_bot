from PIL import Image
from typing import Optional
import os


class Resizer:
    def __init__(self, output_path: str | None = None):
        if output_path is None:
            self.output_path = os.path.join(
                os.sep.join(__file__.split('.')[1:]), 'output')
        else:
            self.output_path = output_path

        self.A4_SIZE = (2480, 3508)

    def resize_photo_to_a4(self, photo_path: str, output_path: Optional[str] = None):
        if output_path is None:
            output_path = self.output_path
        # Open the original photo
        with Image.open(photo_path) as img:
            # Get original dimensions
            original_width, original_height = img.size
            a4_size = self.A4_SIZE if original_width < original_height else tuple(
                reversed(self.A4_SIZE))

            # Determine the scaling factor to fit the photo within A4 dimensions
            scale_factor = min(
                a4_size[1] / original_height, a4_size[0] / original_width)

            # Calculate new dimensions
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Create a new image with A4 dimensions and white background
            a4_img = Image.new('RGB', a4_size, (255, 255, 255))

            # Calculate position to paste the resized image onto the A4 background
            paste_x = (a4_size[0] - new_width) // 2
            paste_y = (a4_size[1] - new_height) // 2

            # Paste the resized image onto the A4 background
            a4_img.paste(resized_img, (paste_x, paste_y))

            # Ensure the output directory exists
            os.makedirs(output_path, exist_ok=True)

            # Define the output path
            output_path = os.path.join(
                output_path, os.path.basename(photo_path))

            # Save the final image
            a4_img.save(output_path)

        return output_path


if __name__ == '__main__':
    r = Resizer('resizer/output')
    r.resize_photo_to_a4('resizer/photo.jpg')
