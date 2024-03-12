from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from typing import Union

class PseudoFlowModel:
    def __init__(self, model_id, instructions=None, examples=None):
        self.model_id = model_id
        self.model = AutoModelForSequenceClassification.from_pretrained(model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.instructions = instructions
        self.examples = examples
        self.pipeline = pipeline(task="text-generation", model=self.model, tokenizer=self.tokenizer)

    def set_instructions(self, instructions):
        self.instructions = instructions

    def add_examples(self, examples):
        if not self.examples:
            self.examples = []
        self.examples.extend(examples)

    def add_pipeline(self, task, model=None, tokenizer=None):
        if not model:
            model = self.model
        if not tokenizer:
            tokenizer = self.tokenizer
        self.pipelines[task] = pipeline(task, model=model, tokenizer=tokenizer)

    def run(self, input_text):
        # Preprocess input with instructions and examples
        full_input = f"{self.instructions}"
        for example in self.examples:
            full_input += f"\nExample: {example[0]} Answer: {example[1]}"
        full_input+="\nInput: " + input_text
        
        # Generate response
        output = self.pipeline(full_input)
        return output


    def save(self, path):
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

    @classmethod
    def load(cls, path, instructions=None, examples=None):
        model = AutoModelForSequenceClassification.from_pretrained(path)
        tokenizer = AutoTokenizer.from_pretrained(path)
        model_id = path.split('/')[-1]  # Assuming the path format includes the model_id
        return cls(model_id, instructions, examples, model, tokenizer)

#class PseudoFlowPipeline:
 #   def __init__(self, models=None):
  #      self.models = models if models is not None else []
#
 #   def add_model(self, model):
  #      self.models.append(model)
#
 #   def run(self, input_text):
  #      for model in self.models:
   #         input_text = model.run(input_text)
    #    return input_text

class PseudoFlowFunctionWrapper:
    """
    To pass in a Python function to a pipeline, use a function that takes one input, a list, where [0] is the initial input, [1] is the first component's output, etc., and [-1] is the current string. It should return what the new string should be, do not modify outputs inplace
    """
    def __init__(self, func):
        self.func = func

    def run(self, outputs):
        self.func(outputs)



class PseudoFlowPipeline:
    def __init__(self, components=None):
        """
        Initializes the pipeline with models and/or other pipelines and/or Python functions.
        Look at PseudoFlowFunctionWrapper for details on passing in a Python function

        :param components: A list containing either PseudoFlowModel instances or PseudoFlowPipeline instances.
        """
        try:
            for i in range(len(components)):
                if callable(components[i]):
                    components[i] = PseudoFlowFunctionWrapper(component)
        except Exception as e:
            print(e)
                
        self.components = components if components is not None else []
        self.outputs = []
                

    def add_component(self, component):
        """
        Adds a model or another pipeline or a Python function to the pipeline components.

        :param component: A PseudoFlowModel or PseudoFlowPipeline instance to be added.
        """
        if callable(component):
            self.components.append(PseudoFlowFunctionWrapper(component))
        self.components.append(component)

    def run(self, input_text: str | list):
        """
        Executes the pipeline, passing input through each component in sequence.

        :param input_text: The text input to process through the pipeline.
        :return: The output text after processing through all components.
        """
        
        if isinstance(input_text, str):
            input_text = [input_text]
        outputs = [input_text]
        for component in self.components:
            # Check if the component is a model or another pipeline and call the appropriate run method
            for i in range(len(input_text)):
                if isinstance(component, PseudoFlowModel):
                    input_text.append(component.run(outputs[-1][i]))
                    continue
                elif isinstance(component, PseudoFlowPipeline):
                    input_text.append(component.run_within(outputs[-1][i]))
                    continue
                input_text.append(component.run(input_text))
            outputs.append(input_text)
            input_text = []
        return input_text[-1]

    def run(self, input_text: str | list):
        """
        Executes the pipeline, passing input through each component in sequence.

        :param input_text: The text input to process through the pipeline.
        :return: The output text after processing through all components.
        """

        # Ensure the input is in list format
        if isinstance(input_text, str):
            input_text = [input_text]

        # The 'outputs' list will store the output from each component for each input string
        outputs = [input_text]

        # Iterate over each component in the pipeline
        for component in self.components:
            # Initialize a new list to store the output from this component
            current_output = []
        
            # Process each item in the outputs of the previous component
            for i in range(len(outputs[-1])):
                if isinstance(component, PseudoFlowModel):
                    # Pass the single item to the model's run method
                    processed_item = component.run(outputs[-1][i])
                elif isinstance(component, PseudoFlowPipeline):
                    # Pass the single item to the pipeline's run_within method
                    processed_item = component.run_within(outputs[-1][i])
                else:
                    # If it's a function, we assume it takes the full history (all previous outputs for the item)
                    processed_item = component([result[i] for result in outputs])
                    
                # Append the processed item to the current output list
                current_output.append(processed_item)

            # Append the current output list to the 'outputs' list
            outputs.append(current_output)

        # The final output is the last item in the 'outputs' list for each input
        return [out[-1] for out in outputs[1:]]  # Skip the first list which is the original input


    def run_within(input_text: list):
        if isinstance(input_text, str):
            input_text = [input_text]
        for component in self.components:
            # Check if the component is a model or another pipeline and call the appropriate run method
            if isinstance(component, PseudoFlowModel):
                input_text.append(component.run(input_text[-1]))
                continue
            elif isinstance(component, PseudoFlowPipeline):
                input_text.append(component.run_within(input_text[-1]))
                continue
            input_text.append(component.run(input_text))
        return input_text[-1]
