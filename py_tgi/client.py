from typing import TYPE_CHECKING, Any, Dict, List, Union
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from huggingface_hub import InferenceClient

if TYPE_CHECKING:
    from huggingface_hub.inference._text_generation import TextGenerationResponse


LOGGER = getLogger("tgi-llm-client")

LLMClientOutput = Union[
    str, List[str], "TextGenerationResponse", List["TextGenerationResponse"]
]


class LLMClient:
    def __init__(self, url: str) -> None:
        LOGGER.info("\t+ Creating InferenceClient")
        self.tgi_client = InferenceClient(model=url)

    def generate(
        self, prompt: Union[str, List[str]], **kwargs: Dict[str, Any]
    ) -> LLMClientOutput:
        if isinstance(prompt, str):
            return self.tgi_client.text_generation(prompt=prompt, **kwargs)

        elif isinstance(prompt, list):
            with ThreadPoolExecutor(max_workers=len(input["prompt"])) as executor:
                futures = [
                    executor.submit(
                        self.tgi_client.text_generation, prompt=prompt[i], **kwargs
                    )
                    for i in range(len(prompt))
                ]

            output = []
            for i in range(len(input["prompt"])):
                output.append(futures[i].result())
            return output
