'''
LLM Client for Tactical Strategy Generation

Uses TinyLlama (small, fast model) for CPU-friendly inference.
'''

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


class LLMClient:
    '''Wrapper for local Hugging Face LLM optimized for CPU.'''

    def __init__(self, model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'):
        '''Initialize the LLM client.'''
        self.model_name = model_name
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.pipe = None
        print(f'LLMClient initialized. Device: {self.device}')
        print(f'Model: {self.model_name}')

    def load_model(self):
        '''Download and load the model.'''
        print(f'Loading model: {self.model_name}')
        print('First-time download takes 2-5 minutes...')

        self.pipe = pipeline(
            'text-generation',
            model=self.model_name,
            torch_dtype=torch.float32,
            device_map=self.device,
        )
        print('Model loaded successfully!')

    def generate(self, prompt, max_new_tokens=150):
        '''Generate text from a prompt.'''
        if self.pipe is None:
            raise RuntimeError('Model not loaded. Call load_model() first.')

        messages = [
            {'role': 'system', 'content': 'You are a football tactics expert.'},
            {'role': 'user', 'content': prompt},
        ]

        formatted_prompt = self.pipe.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        outputs = self.pipe(
            formatted_prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.pipe.tokenizer.eos_token_id,
        )

        full_response = outputs[0]['generated_text']
        response = full_response.split('<|assistant|>')[-1].strip()
        return response


if __name__ == '__main__':
    client = LLMClient()
    client.load_model()
    response = client.generate('What is a 4-3-3 formation in football?')
    print('Response:', response)
