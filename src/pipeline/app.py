from docling.document_converter import DocumentConverter, PdfFormatOption
from pathlib import Path
from typing import Iterable
from dataclasses import dataclass
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import FigureElement, InputFormat, Table
from docling_core.types.doc import ImageRefMode, PictureItem, TableItem
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
)
from docling.chunking import HybridChunker
from docling.datamodel.document import ConversionResult, ConversionStatus
from azure.identity import DefaultAzureCredential
import uuid
import os
import dotenv

dotenv.load_dotenv()

IMAGE_RESOLUTION_SCALE = 2.0
OUTPUT_DIR = Path("output")
DOCUMENT_CONTAINER = "documents"
PROCESSED_DOCUMENT_CONTAINER = 'processed-documents'
MAX_TOKENS = 64

input_file = "ISO 527-1_2012-02.pdf"
input_folder = "../../data/"

@dataclass
class Document:
    id: str
    page_content: str
    metadata: dict

def main():
    accelerator_options = AcceleratorOptions(
        num_threads=8, device=AcceleratorDevice.CPU)

    options = PdfPipelineOptions()
    options.images_scale = IMAGE_RESOLUTION_SCALE
    options.generate_picture_images = True
    options.generate_page_images = True
    options.accelerator_options = accelerator_options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF:PdfFormatOption(pipeline_options=options),
        },
    )

    dir = Path(OUTPUT_DIR)
    dir.mkdir(parents=True, exist_ok=True)


    conversion_result = convert_file(input_folder + input_file, converter)

    if conversion_result.status == ConversionStatus.SUCCESS:
        converted_results_path = store_result_locally(conversion_result)
        print(f"Converted {input_file} to {converted_results_path}")      


def convert_file(path: Path, converter: DocumentConverter) -> ConversionResult:
    return converter.convert(path, raises_on_error=False)

def store_result_locally(result: ConversionResult) -> Path:
    if result.status == ConversionStatus.SUCCESS:
        dir = Path(OUTPUT_DIR / Path(result.document.origin.filename).stem)
        dir.mkdir(parents=True, exist_ok=True)
        md_filename = dir / f"result.md"
        result.document.save_as_markdown(md_filename, image_mode=ImageRefMode.REFERENCED)
        return dir
    else:
        print(f"Failed to convert {result.stem}")
        return None

def delete_file(file_name: str):
    os.remove(file_name)

if __name__ == "__main__":
    main()