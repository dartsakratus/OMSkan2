import re
from pathlib import Path

from pypdf import  PdfReader, PdfWriter
import pypdfium2 as pdfium
import zxingcpp


def get_pattern(stage:int):
    if stage == 1:
        return re.compile(r"[A-Z]{2}_[0-9]+_[1-5]")
    elif stage == 2:
        return re.compile(r"[A-Z]{2}_[0-9]+_[1-6]")
    elif stage == 3:
        return re.compile(r"[0-9]+_[1-6]")
    else:
        raise ValueError("Etap powinien być wartością całkowitą z przedziału [1,3]")

def process(
    input_path: Path, output_dir: Path, stage: int, report=lambda msg: None
) -> list[Path]:
    report("Wczytywanie pliku...")
    reader = PdfReader(str(input_path))     # for copying pages into new PDFs
    pdf = pdfium.PdfDocument(str(input_path))  

    created: list[Path] = []

    student_id = None
    problem_id = None

    writer = PdfWriter()

    for i in range(len(pdf)):

        image = pdf[i].render(scale=2).to_pil()  # if the QR code is missed often you can bump this up to 3 or 4
        results = zxingcpp.read_barcodes(image, formats=zxingcpp.BarcodeFormat.QRCode)

        if len(results)>1:
            raise ValueError(f"Wykryto więcej niż jeden kod QR na stronie {i}.")

        if len(results) == 1:
            result = results[0].text.strip()
            PATTERN = get_pattern(stage)
            if not PATTERN.fullmatch(result):
                raise ValueError(f"Niepoprawny kod QR: {result!r}")

            report(f"Zapisywanie pracy ucznia {student_id}, zadanie {problem_id}...")
            if len(writer.pages)>0:
                out_file = output_dir / f"{stage}_{student_id}_{problem_id}.pdf"
                with open(out_file, "wb") as f:
                    writer.write(f)
                created.append(out_file)
            writer = PdfWriter()
            
            
            _, student_id, problem_id = result.split("_")
            continue

        if (not student_id) or (not problem_id):
            raise ValueError("Brakuje strony z kodem QR.") 
        writer.add_page(reader.pages[i])       

    if len(writer.pages)>0:
        out_file = output_dir / f"{stage}_{student_id}_{problem_id}.pdf"
        with open(out_file, "wb") as f:
            writer.write(f)
        created.append(out_file)
        
    return created