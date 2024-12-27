from dataclasses import dataclass

@dataclass
class Prompt:
    @staticmethod
    def article_prompt(topic: str) -> str:
        return (
            f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'.\n"
            "The article must affirm the topic and provide a comprehensive overview of the subject matter.\n"
            "The article must be scholarly, realistic, and well-researched, with a clear structure and logical flow.\n"
            "The sources and authors must be credible, realistic, and authoritative.\n"
            "Authors must have realistic names, institutions, and email addresses. You cannot use generic names like Joe/Jane Doe\n"
            "Also, provide a comma-separated list of 2 sets of keywords to be used for relevant image searches.\n"
            "You must NOT use any characters that will break the JSON structure, such as `, $, %, etc.\n\n"
            "You must NOT use any markdown in your responses.\n\n"
            "Ensure you return valid JSON without any additional text or code fences. \n\n"
            "Do not include any characters or markdown syntax outside the JSON object.\n\n"
            "Please provide the responses in the exact JSON structure shown below.\n\n"
            "Output must be strictly valid JSON. Do not include quotes in the keys if the JSON structure is already shown. \n\n"
            "Any deviation from valid JSON will cause an error.\n\n"
            "JSON Structure:\n"
            '''{
              "journal": "string: the name of the journal",
              "doi": "string: the DOI of the article",
              "title": "string: the title of the article",
              "abstract": "string: brief summary of the article",
              "introduction": "string: introduction to the article",
              "methodology": "string: description of research methods",
              "results": "string: summary of research findings",
              "discussion": "string: discussion of results and implications",
              "conclusion": "string: summary of conclusions",
              "keywords": "[comma-separated list of 3 keywords related to the topic for image search]",
              "citations": [
                  {
                  "content": "string: APA-formatted source 1"
                  },
                  {
                  "content": "string: APA-formatted source 2"
                  },
                  {
                  "content": "string: APA-formatted source 3"
                  }
              ],
              "authors": [
                  {
                  "name": "string: realistic author's name 1",
                  "institution_name": "string: institution name",
                  "institution_address": "string: institution address",
                  "email": "string: author's email"
                  },
                  {
                  "name": "string: realistic author's name 2",
                  "institution_name": "string: institution name",
                  "institution_address": "string: institution address",
                  "email": "string: author's email"
                  }
              ],
              "figures": [
                  {
                  "description": "string: description of the figure",
                  "xaxis_title": "string: title of the x-axis",
                  "yaxis_title": "string: title of the y-axis"
                  }
              ]
            }'''
        )
    
    @staticmethod
    def story_prompt(topic: str) -> str:
         return (
         f"Write a 3000 word realistic newspaper article based on the following topic: '{topic}'.\n"
           "# Rules:\n"
              "- This news report must contain no quotes or interviews. \n"
              "- This needs to be a realistic, well-researched newspaper story. \n"
              "- You must return valid JSON without any additional text or code fences. \n"
              "- You must adhere to the JSON structure provided below. \n"
              "- The journalist info must be realistic and authoritative. \n"
            "JSON Structure:\n"
            '''{
              "headline": "string: headline of the story",
              "subheadline": "string: subheadline of the story",
              "journalist_name": "string: realistic  name of the journalist",
              "journalist_bio": "string: journalist's bio",
              "journalist_email": "string: journalist's email",
              "publication": "string: the publishing newspaper",
              "title": "string: the title of the article",
              "content": "string: entire, 3000 word full-length story. There myst be no interviews here. Do not quote anyone.",
              "keywords": "[string: comma-separated list of 3 keywords related to the topic for image search]",
              ## You can use quotes and breakouts to add more content to the story in the JSON response below
              "quotes": [ 
                  {
                  "content": "string: quote from interviewee 1",
                  "speaker": "string: name of the interviewee"
                  },
                  {
                  "content": "string: quote from interviewee 2",
                  "speaker": "string: name of the interviewee"
                  }             
                ],
                "breakouts": [
                  {
                  "title": "string: stand-alone breakout title",
                  "content": "string: stand-alone breakout content"
                  }
                ]
            }'''
         )