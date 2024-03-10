from transformers import pipeline

def separate_problems(separation_model, instructions):
    pipeline = pipeline('text-generation', model=separation_model, tokenizer=separation_model.tokenizer)
    examples = [
        """Prompt:
        Instructions:
        Use the provided document ID to access the content of the document via the function "get_document_content".
        Read the document carefully to understand the main themes and messages.
        Generate a concise summary, aiming for approximately 150-200 words.
        Ensure the summary captures the key points and arguments without any personal interpretation or additional information not present in the text.
        Maintain the original tone and intent of the document.
        Avoid disclosing sensitive information found in the document.
        Deliver the summary in clear, coherent, and neutral language.

        Tools:
        {
            "description": "",
            "type": "function",
            "function": {
                "name": "get_document_content",
                "parameters": {
                    type:"object200~ 
                    document_id": {
                     
                    }
                }
            }
            
        }
        
        
        Response:
        Access document 
        """
    ]
    prompt = "Your goal is to simplify these LLM instructions into a set of possible tasks. These tasks will be used to generate sample prompt response pairs that will cover the extent of this LLM's intended capabilities. Do not worry about capabilities that are not mentioned in the instructions. Here are some example of good outputs, keeping in mind that the prompt and instructions are not for you, they are simply examples. Your instructions have been previously stated. For the following examples, 'Prompt:' is instructions to create a specific LLM, and it is the input you will receive. 'Response:' is the output you would give if given this prompt. \n"
    [prompt += example + "\n" for example in examples]
    return pipeline(prompt)

def generate_example(pipeline, prompt):
    return pipeline(prompt)

def dataset_generator(teacher_model, task, num_examples):
    pipeline = pipeline('text-generation', model=teacher_model, tokenizer=teacher_model.tokenizer, max_length=200)
    prompt = 'Generate a prompt response pair for the LLM task described below. The model is less advanced than you and as such must be taught what a good response for this particular task is.\n' + task + 'The pair should be formatted as such: {prompt}\n{response}. Here are some examples of good outputs:\n'
    examples = []
    [prompt += example + "\n" for example in examples]
    for i in range(examples):
        yield generate_example(prompt)



    
