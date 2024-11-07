from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary
import os
from typing import Tuple

information = """
Ayrton Senna da Silva (Brazilian Portuguese: [aˈiʁtõ ˈsẽnɐ dɐ ˈsiwvɐ] ⓘ; 21 March 1960 – 1 May 1994) was a Brazilian racing driver, who competed in Formula One from 1984 to his death in 1994. Senna won three Formula One World Drivers' Championship titles with McLaren, and—at the time of his death—held the record for most pole positions (65), among others; he won 41 Grands Prix across 11 seasons.

Senna began his motorsport career in karting, moved up to open-wheel racing in 1981 and won the 1983 British Formula Three Championship. He made his Formula One debut with Toleman in 1984, before moving to Team Lotus for the 1985 season and winning six Grands Prix over the next three seasons. In 1988, he joined Frenchman Alain Prost at McLaren. Between them, they won all but one of the 16 Grands Prix that year, and Senna claimed his first World Championship. Prost claimed the championship in 1989, and Senna his second and third championships in the 1990 and 1991 seasons. In 1992, the Williams-Renault combination began to dominate Formula One. Senna managed to finish the 1993 season as runner-up, winning five races and negotiating a move to Williams in 1994.

Senna was recognised for his qualifying speed over one lap and the ability to push his car to the very limit. He was also acclaimed for his wet weather performances, such as the 1984 Monaco Grand Prix, the 1985 Portuguese Grand Prix, and the 1993 European Grand Prix. He holds a record six victories at the Monaco Grand Prix, is the sixth-most successful driver of all time in terms of most Grand Prix wins, and has won more races for McLaren than any other driver. Senna courted controversy throughout his career, particularly during the turbulent Prost–Senna rivalry. In the Japanese Grands Prix of 1989 and 1990, each of which decided the championship of that year, collisions between Senna and Prost determined the eventual winner.

During the 1994 San Marino Grand Prix, Senna died as a result of an accident whilst leading the race, driving for Williams. His state funeral was attended by an estimated three million people. Following subsequent safety reforms, he was the last fatality in the Formula One World Championship until Jules Bianchi in 2015. Senna was inducted into the International Motorsports Hall of Fame in 2000.
"""


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username, mock=True
    )

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    # llm = ChatOllama(model="llama3")

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/lucasdeavila", mock=True
    )
    res: Summary = chain.invoke(input={"information": linkedin_data})
    print(res)

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter!")
    ice_break_with(name="Lucas de Ávila Moreira Linkedin Profile")
