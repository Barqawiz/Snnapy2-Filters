from intelli.controller.remote_image_model import RemoteImageModel
from intelli.model.input.image_input import ImageModelInput


class Generate:
    def __init__(self, provider: str, api_key: str):
        """
        Initializes the Generate class with the specified provider and API key.

        Parameters:
            provider (str): The provider to use for image generation. Accepted values are 'openai' or 'stability'.
            api_key (str): Your API key
        """

        self.wrapper = RemoteImageModel(api_key, provider)

    def generate_base46_image(self, prompt: str, model_name, width=1024, height=1024):
        """
           Generates an image from a prompt using a specified model, returning it as a base64 string.
           For example, use model_name like 'stable-diffusion-xl-1024-v1-0' or 'dall-e-3'.
        """
        image_input = ImageModelInput(
            prompt=prompt,
            number_images=1,
            width=width,
            height=height,
            response_format="b64_json",
            model=model_name)

        return self.wrapper.generate_images(image_input)
