"""
Minimal wrapper around spineController for use in Docker container
"""
import os
import logging
from argparse import ArgumentParser
from abcCore.abc.spine.app import spineApp

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(process)s] [%(threadName)s] [%(levelname)s] (%(name)s:%(lineno)d) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True
    )

def init_app():
    """
    Initialise the spine app
    """
    app_dir = os.path.dirname(__file__)
    studies =  "https://127.0.0.1:8989" #Just points to an empty address - needed for monaiLabelApp
    config = {
        "models": "find_spine,find_vertebra",
        "preload": "false",
        "use_pretrained_model": "true"
    }   
    return spineApp(app_dir, studies, config)

def json_to_mask(json):
    """
    Convert the json output with levels into a mask.
    Not ideal for storage but better integration with XNAT and reduces transform-related errors
    """
    logger.info(f"Output JSON: {json}")

def handle_response(res):
    """
    Handle the reply from inference 
    """
    label = res["file"]
    label_json = res["params"]

    if label is None and label_json is None:
        #* This is the case if no centroids were detected
        logger.error(f"Inference failed. Could not find any centroids.")
        
    elif label is None and label_json is not None:
        logger.info(f"Converting JSON output into a mask")
        json_to_mask(label_json)
    else:
        logger.error("Vertebra mask detected - HOW TF HAS THAT HAPPENED?")
        # This should never happen... Would like to add this though

def main(input_path, output_path):
    app = init_app()

    # Filter dicom 
    dcm_files = [x for x in os.listdir(input_path) if x.endswith('.dcm')]
    if len(dcm_files) == 0:
        logger.error("No dicom files! Aborting...")
        exit()

    logger.info(f"Detected {len(dcm_files)} DICOM files")
    
    # +++++ INFERENCE +++++
    response = app.infer(
        requets = {"model": "vertebra_pipeline", "image": input_path}
    )

    handle_response(response)


if __name__ == '__main__':
    ap = ArgumentParser(description="Minimal wrapper around ABC spine controller")

    ap.add_argument('-i', '--input_path', help="Path to input scan")
    ap.add_argument('-o', '--output_path', help="Path to write output")

    args = ap.parse_args()
    main(args.input_path, args.output_path)
    