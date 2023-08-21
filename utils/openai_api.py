import os
import json
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

system = """
Je bent de virtuele assistent van een applicatieadviseur gespecialiseerd in bedrijfssoftware. Je beantwoordt en genereert e-mails gericht aan collega's.

    Taal en Toon: Direct en zakelijk. Gebruik 'jij'. Leg technisch jargon uit waar nodig. Taalniveau B1.
    Antwoorden en Initiële E-mails: Zonder beleefdheden of vleierij. Ga direct naar de kern van de zaak
    Voor initiële e-mails, voeg een duidelijke call-to-action toe indien nodig. 
    Begroeting: Gebruik alleen de voornaam van de afzender of ontvanger in combinatie met Beste of Hallo.
    Afsluiting: Sluit standaard af met 'Met vriendelijke groet, Johan'.

Belangrijk: Geen opmerkingen over persoonlijke omstandigheden. Wees zakelijk, feitelijk maar ook vriendelijk, dankbaar en positief.
"""
#  en gebruik alleen feitelijke en geverifieerde informatie.

# Weder-vragen: Als de ontvangen e-mail geen vraag bevat, stel dan geen weder-vraag.
# initial_inquiry = "What is the salary for this position?"
# initial_response = "come on..."
# number_of_sentences = 2



def response_generator(emails_to_respond_to, response_instructions, model="gpt-3.5-turbo"):
    gpt_4_prompt = f"""Emails om op te reageren:\n{emails_to_respond_to}\n\nInstructies voor de te genereren email:\n{response_instructions}\n\nGeef als output een JSON met de volgende twee keys: Email_1, Email_2.\n\nvoorbeeld formaat:\n{{\\"Email_1\\": \\"Beste Klaas,\\\\n\\\\nDit is een voorbeeld email.\\\\n\\\\nGroeten,\\\\nJohan\\", \\"Email_2\\": \\"Hallo Klaas,\\\\n\\\\nDit is een andere voorbeeld email.\\\\n\\\\nVriendelijke groet,\\\\nJohan\\"}}"""
    gpt_3_prompt = f"""Emails om op te reageren:\n{emails_to_respond_to}\n\nInstructies voor de te genereren email:\n{response_instructions}\n\nGeef als output een JSON met de volgende twee keys: Email_1, Email_2.\n\nvoorbeeld formaat:\n{{\\"Email_1\\": \\"Beste Klaas,\\\\n\\\\nDit is een voorbeeld email.\\\\n\\\\nGroeten,\\\\nJohan\\", \\"Email_2\\": \\"Hallo Klaas,\\\\n\\\\nDit is een andere voorbeeld email.\\\\n\\\\nVriendelijke groet,\\\\nJohan\\"}}"""

    prompt = gpt_3_prompt
    if model == "gpt-4": prompt = gpt_4_prompt

    response_dict = None  # Initialize to None or some default value

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": prompt

            }
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        print(response["usage"])
        print(response["choices"][0]["message"]["content"])
        response_dict = json.loads(response["choices"][0]["message"]["content"])
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("Raw response:", response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return response_dict
