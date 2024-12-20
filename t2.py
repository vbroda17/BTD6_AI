from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_gpu=True)  # Use CPU
result = ocr.ocr('images/buttons/mapModes/buttonReverse.png')
print(result)
