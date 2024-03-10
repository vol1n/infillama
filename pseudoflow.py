from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

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


class PseudoFlowPipeline:
    def __init__(self, components=None):
        """
        Initializes the pipeline with either models or other pipelines.

        :param components: A list containing either PseudoFlowModel instances or PseudoFlowPipeline instances.
        """
        self.components = components if components is not None else []

    def add_component(self, component):
        """
        Adds a model or another pipeline to the pipeline components.

        :param component: A PseudoFlowModel or PseudoFlowPipeline instance to be added.
        """
        self.components.append(component)

    def run(self, input_text):
        """
        Executes the pipeline, passing input through each component in sequence.

        :param input_text: The text input to process through the pipeline.
        :return: The output text after processing through all components.
        """
        for component in self.components:
            # Check if the component is a model or another pipeline and call the appropriate run method
            input_text = component.run(input_text)
        return input_text
