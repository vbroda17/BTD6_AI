from paddleocr import PaddleOCR
ocr = PaddleOCR(use_gpu=False)
result = ocr.ocr('images/buttons/mapModes/buttonStandard.png', cls=True)
print(result)
