from dotenv import load_dotenv
load_dotenv()

from langchain import FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

import prompts.cairo

MAX_TOKENS = 2750

code_snippet_template = """
Snippet: {snippet}
"""

snippet_prompt = PromptTemplate(
    input_variables=["snippet"],
    template=code_snippet_template
)

# now break our previous prompt into a prefix and suffix
# the prefix is our instructions
prefix = """
Assistant is a large language model trained to aide in writing correct and concise code in a wide range of programming languages. Assistant can infer semantics of a languge given a set of snippets.

Assistant outputs concise outputs, wrapping code blocks in triple ticks (```).

Following is some additional context on the programming language and some example code snippets. The snippets are not meant to be run, but are provided as succinct examples of correct code.
"""
# and the suffix our user input and output indicator
suffix = """
User: {query}
AI: """

example_selector = LengthBasedExampleSelector(
    examples=prompts.cairo.examples,
    example_prompt=snippet_prompt,
    max_length=MAX_TOKENS
)

dynamic_prompt_template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=snippet_prompt,
    prefix=prefix + prompts.cairo.prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n"
)

chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
chain = LLMChain(llm=chat, prompt=dynamic_prompt_template)
print(chain.run("Provide a function to count the number of odd integers in an array."))
# print(len(prompt))
