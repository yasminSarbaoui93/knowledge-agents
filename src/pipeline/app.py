# NOTE: The following packages must be installed in your Python environment for this script to work:
#   - docling
#   - docling_core
#   - azure-identity
#   - python-dotenv
# Install them using pip if you have not already:
#   pip install docling docling_core azure-identity python-dotenv

from pathlib import Path
from typing import Iterable, Optional
from dataclasses import dataclass
import uuid
import os

# Attempt to import dotenv if available
try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    print("python-dotenv is not installed. Skipping .env loading.")

# Attempt to import docling modules, handle import errors gracefully
try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.datamodel.base_models import FigureElement, InputFormat, Table
    from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
    from docling.datamodel.pipeline_options import (
        AcceleratorDevice,
        AcceleratorOptions,
    )
    from docling.chunking import HybridChunker
    from docling.datamodel.document import ConversionResult, ConversionStatus
except ImportError as e:
    print(f"ImportError: {e}. Please ensure the 'docling' and 'docling_core' packages are installed and available.")

try:
    from azure.identity import DefaultAzureCredential
except ImportError:
    print("azure-identity is not installed. Some Azure features may not work.")

IMAGE_RESOLUTION_SCALE = 2.0
OUTPUT_DIR = Path("output")
DOCUMENT_CONTAINER = "documents"
PROCESSED_DOCUMENT_CONTAINER = 'processed-documents'
MAX_TOKENS = 64

input_file = "EFSA Supporting Publications - 2018 -  - Outcome of the public consultation on the draft Scientific Opinion on Listeria.pdf"
input_folder = "."

@dataclass
class Document:
    id: str
    page_content: str
    metadata: dict

def main():
    # Check if docling imports succeeded
    if 'DocumentConverter' not in globals():
        print("Critical: docling modules not available. Exiting.")
        return

    accelerator_options = AcceleratorOptions(
        num_threads=8, device=AcceleratorDevice.CPU)

    options = PdfPipelineOptions()
    options.images_scale = IMAGE_RESOLUTION_SCALE
    options.generate_picture_images = True
    options.generate_page_images = True
    options.accelerator_options = accelerator_options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=options),
        },
    )

    dir = Path(OUTPUT_DIR)
    dir.mkdir(parents=True, exist_ok=True)

    # Use Path for file operations
    input_path = Path(input_folder) / input_file
    if not input_path.exists():
        print(f"Input file {input_path} does not exist.")
        return

    conversion_result = convert_file(input_path, converter)

    if conversion_result.status == ConversionStatus.SUCCESS:
        converted_results_path = store_result_locally(conversion_result)
        print(f"Converted {input_file} to {converted_results_path}")
    else:
        print(f"Conversion failed for {input_file}")

def convert_file(path: Path, converter) -> 'ConversionResult':
    return converter.convert(path, raises_on_error=False)

def store_result_locally(result) -> Optional[Path]:
    if result.status == ConversionStatus.SUCCESS:
        dir = Path(OUTPUT_DIR / Path(result.document.origin.filename).stem)
        dir.mkdir(parents=True, exist_ok=True)
        md_filename = dir / f"result.md"
        result.document.save_as_markdown(md_filename, image_mode=ImageRefMode.REFERENCED)
        return dir
    else:
        # Use a safer error message
        print(f"Failed to convert document: {getattr(result, 'document', None)}")
        return None

def delete_file(file_name: str):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found for deletion.")
    except Exception as e:
        print(f"Error deleting file {file_name}: {e}")

if __name__ == "__main__":
    main()