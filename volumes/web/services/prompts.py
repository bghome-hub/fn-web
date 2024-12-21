from dataclasses import dataclass

@dataclass
class Prompt:
    @staticmethod
    def article_prompt(topic: str) -> str:
        return (
            f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'.\n"
            "The article must affirm the topic and provide a comprehensive overview of the subject matter.\n"
            "The article must be scholarly, realistic, and well-researched, with a clear structure and logical flow.\n"
            "The sources and authors must be credible, realistic, and authoritative. Author data MUST NOT be generic.\n"
            "Also, provide a comma-separated list of 2 sets of keywords to be used for relevant image searches.\n"
            "You must NOT use any characters that will break the JSON structure, such as $, %, etc.\n\n"
            "You must NOT use any markdown in your responses.\n\n"
            "Please provide the responses in the exact JSON structure shown below, ensuring that all fields are populated correctly and that APA sources are properly formatted with author(s), title, journal name, volume, issue, and year.\n\n"
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
              "keywords": : "comma-separated list of 2 sets of keywords related to the topic for image search",
              "citations": [
                  {
                  "content": "string: APA-formatted source 1"
                  },
                  {
                  "content": "string: APA-formatted source 2"
                  },
                  {
                  "content": "string: APA-formatted source 3"
                  },
                  {
                  "content": "string: APA-formatted source 4"
                  },
                  {
                  "content": "string: APA-formatted source 5"
                  }
                }
              ],
              "authors": [
                {
                  "name": "string: <realistic, random name>",
                  "institution_name": "string: <realistic, relevant insitution name>",
                  "institution_address": "string: <realistic, institution address>",
                  "email": "string: <realistic author email>"
                },
                {
                  "name": "string: <realistic, random name>",
                  "institution_name": "string: <realistic, relevant insitution name>",
                  "institution_address": "string: <realistic, institution address>",
                  "email": "string: <realistic author email>"
                }
              ],
              "figures": [
                {
                  "description": "string: description of figure 1 ",
                  "xaxis_title": "string: title of x-axis 1",
                  "xaxis_value": "[numbers: <value of x-axis 1. numeric only, comma-separated, no symbols such as: $, %, etc.>]",],
                  "yaxis_title": "string: title of y-axis 1",
                  "yaxis_value": "[numbers: <value of x-axis 1. numeric only, comma-separated, no symbols such as: $, %, etc.>]",]
                },
                {
                  "description": "string: description of figure 2",
                  "xaxis_title": "string: title of x-axis 2",
                  "xaxis_value": "[numbers: <value of x-axis 2. numeric only, comma-separated, no symbols such as: $, %, etc.>]",],
                  "yaxis_title": "string: title of y-axis 2",
                  "yaxis_value": "[numbers: <value of y-axis 2. numeric only, comma-separated, no symbols such as: $, %, etc.>]",]
                }
              ]
            }'''
            "Please provide the responses in the exact structure shown above, ensuring that the APA sources are properly formatted with author(s), title, journal name, volume, issue, and year."
        )
            