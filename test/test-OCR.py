from ingestion.image_processor import process_image

response = process_image("data/img.png")
print(response.content)