class ContextData:
    def __init__(self):
        self._context = ""  # Notice the underscore, it denotes a private attribute
        self._counter = 1

    @property
    def context(self):
        """The context property."""
        return self._context

    @context.setter
    def context(self, value):
        if isinstance(value, str):
            self._context = value  # Set the private attribute, not the property itself
        else:
            raise ValueError("Context must be a string")

    @context.deleter
    def context(self):
        self._context = None

    @property
    def counter(self):
        """The counter property."""
        return self._counter

    @counter.setter
    def counter(self, value):
        if isinstance(value, int) and value >= 0:
            self._counter = value  # Set the private attribute, not the property itself
        else:
            raise ValueError("Counter must be a non-negative integer")

    def increment_counter(self):
        """Increment the counter property by 1."""
        self._counter += 1



def clean_code_snippet(snippet):
    # Split the snippet into lines
    lines = snippet.strip().split('\n')
    
    # Remove the first and last lines if they contain the backticks and language identifier
    if lines[0].strip().startswith("```python"):
        lines = lines[1:]
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    
    # Join the lines back into a single string
    clean_snippet = '\n'.join(lines)
    
    return clean_snippet