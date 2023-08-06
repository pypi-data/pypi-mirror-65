import os
from pathlib import Path
import unittest
import logging
from pmworker import get_settings
from pmworker.endpoint import Endpoint
from pmworker.tasks import ocr_page

logger = logging.getLogger(__name__)

test_dir = Path(__file__).parent
test_data_dir = test_dir / Path("data")
abs_path_input_pdf = test_data_dir / Path("input.de.pdf")


class TestTask(unittest.TestCase):

    def test_ocr_page(self):

        settings = get_settings()
        ocr_page(
            user_id=1,
            document_id=1,
            file_name="input.de.pdf",
            page_num=1,
            lang="deu",
            s3_upload=False,
            s3_download=False,
            test_local_alternative=abs_path_input_pdf
        )
        # Test if ocr_page created jpg, txt and hocr files
        pages = os.path.join(
            Endpoint(settings.local_storage).dirname,
            "results",
            "user_1",
            "document_1",
            "pages",
        )

        page_1_txt = os.path.join(
            pages,
            "page_1.txt"

        )
        page_1_100_jpg = os.path.join(
            pages,
            "page_1",
            "100",
            "page-1.jpg"

        )
        page_1_100_hocr = os.path.join(
            pages,
            "page_1",
            "100",
            "page-1.hocr"

        )

        self.assertTrue(
            os.path.exists(pages)
        )
        self.assertTrue(
            os.path.exists(page_1_txt)
        )
        self.assertTrue(
            os.path.exists(page_1_100_jpg)
        )
        self.assertTrue(
            os.path.exists(page_1_100_hocr),
            f"File {page_1_100_hocr} does not exists."
        )
