from llama_cpp import Llama
import time
from config import MODELS_DIR
class PhiAssistant:

    def __init__(self):

        model_path = (
            MODELS_DIR
            / "phi-4-mini-instruct"
            / "test.gguf"
        )
        print("Loading Phi-4 Mini...")

        self.llm = Llama(
            model_path=str(model_path),
            n_ctx=8192,  # if your inputs fit
            n_threads=8,
            n_batch=512,
            use_mmap=True,
           # use_mlock=True,  # if you have enough RAM
            verbose=False
        )

        print("Phi loaded.")

    def ask(self, prompt, max_tokens=500):
        print("Phi is working on the prompt")
        start = time.perf_counter()
        response = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens
        )
        result = response["choices"][0]["message"]["content"]
        print("Phi finished in ", time.perf_counter() - start)
        return result


phi = None


def get_phi():

    global phi

    if phi is None:
        phi = PhiAssistant()

    return phi
