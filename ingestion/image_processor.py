import base64
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from app.config import llm 


def process_image(image_path):
    try:
        # Read image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        message = HumanMessage(
            content=[
                {"type": "text", "text": "Extract structured information from this image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ]
        )

        response = llm.invoke([message])

        #  Convert to Document (FIX)
        return Document(
            page_content=response.content,
            metadata={
                "source": image_path,
                "type": "image"
            }
        )

    except Exception as e:
        print(f"Image processing failed: {e}")

        # fallback to empty doc (prevents pipeline crash)
        return Document(
            page_content="",
            metadata={
                "source": image_path,
                "type": "image",
                "error": str(e)
            }
        )


# response = process_image("data/img.png")
# print(response.content)
