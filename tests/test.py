import os
import glob

from PIL import Image
from mask_the_face.runner import Runner


def save_image(masked, out_fn):
    if len(masked) == 0:
        print("No face detected ...")
        return
    masked[0].save(out_fn)
    return


def main(raw_args=None):
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./assets")
    dlib_model_dir = os.path.join(assets_dir, "dlib")
    inputs_dir = os.path.join(assets_dir, "inputs")
    output_dir = os.path.join(assets_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    test_images = glob.glob(os.path.join(inputs_dir, "*.jpg"))

    runner = Runner(dlib_model_dir=dlib_model_dir)
    for fn in test_images:
        fn_only = os.path.basename(fn)
        out_fn1 = os.path.join(output_dir, f"{fn_only}_masked_file.jpg")
        out_fn2 = os.path.join(output_dir, f"{fn_only}_masked_byte.jpg")
        out_fn3 = os.path.join(output_dir, f"{fn_only}_masked_pil.jpg")

        print(f"running: {fn_only}")

        # 1. file
        masked1, _, __, ___ = runner.run(fn)
        masked1 = runner.postprocess(masked1)
        save_image(masked1, out_fn1)

        # 2. bytes
        with open(fn, "rb") as f:
            image_bytes = f.read()
        masked2, _, __, ___ = runner.run(image_bytes)
        masked2 = runner.postprocess(masked2)
        save_image(masked2, out_fn2)

        # 3. pillow
        masked3, _, __, ___ = runner.run(Image.open(fn).convert("RGB"))
        masked3 = runner.postprocess(masked3)
        save_image(masked3, out_fn3)

    return


if __name__ == "__main__":
    main()
