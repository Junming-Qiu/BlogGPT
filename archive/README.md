# AutoGenerateWebGPT
### *AutoGenerateGPT is a proof of concept project showcasing the content creation power of what I call "hierarchical self prompting" (HSP). Using this method, a single prompt can be transformed into a fully complete project with context-specific content. This project focuses primarily on prompt generation and engineering, while also placing emphasis on modular and component-based web design*
---
## Project Requirements

### Task: This project will implement a website which autogenerates its content every hour using GPT and an image diffusion model  
### Website:
- Flask website with custom components implemented using macro functions
    - Components include:
      - Navbar
      - Footer
      - Link back to github
      - Several custom containers which display text and image content
        - **Potential idea is to use ChatGPT to generate and test its own content formats**
        - Current solution: Design a series of these containers to choose from.
    - Components must me easily modifiable by passing in a dictionary into Jinja templates to change titles, links, text content, and image content
    - Website must support multiple page routing
      - Routing will be done with URLS that ChatGPT generates that match the content of the pages they are linked to 
- HSP Graph
  - A prompting model which is defined by the following structures:
    - Random generation
      - Structure: GENERATE A *item* WITH *include* AND WITHOUT *exclude* IN *format*
      - Generating a random idea based on a seed prompt and the format
    - Guided generation
      - Structure: GENERATE A *item* WITH *include* AND WITHOUT *exclude* IN *format* GIVEN *context*
      - Generate an idea about a seed prompt based on context and format
    - Recursive self iteration
      - Structure: EVALUATE *text* AS *model* WITH *include* WITHOUT *exclude*
    - Branch select
      - Structure: SELECT *num branches* GIVEN OPTIONS [*option1*, *option2*, ...] WITH *include* WITHOUT *exclude*
    - Modify
      - Structure: REVISE *item* BY *criteria*
    - Summarize
      - Structure: SUMMARIZE *text* FOR *audience* WITH *include* WITHOUT *exclude* IN *format*
    - Expand
      - Structure: EXPAND *text* FOR *audience* WITH *include* WITHOUT *exclude* AND ADD *new information* IN *format*
     - Format Query
       - Structure: WHAT ARE THE ELEMENTS OF A *item*
    - Extract
       - Structure: EXTRACT *item* FROM *item*
       - Structure: INFER *item* FROM *item*
    - Replace
      - Structure: REPLACE *word/s* WITH *word/s* 
  - Additional information in each node:
    - Complexity
    - Classification
    - Node type
- HSP Graph Parser
  - Labels
- Additional
  - Archives of website content