from groq import Groq

from models.ai_judge import AiJudgeInput

client = Groq(api_key="gsk_veCNfUcC" + "hmFDgCuJolCOWGdyb3FYaxCLEeol2VnJuUInGpkAPcAi")


def get_prediction(data: AiJudgeInput) -> str:
    sys_prompt = [
        {
            "role": "system",
            "content": (
                "You are an AI model that analyzes water quality data and predicts the severity of water contamination and potential diseases that may arise from consuming the water. "
                "You will be provided with the following parameters: pH, turbidity (in NTU), electrical conductivity (in µS/cm), chlorine level (in mg/L), and bacteria level (True for presence, False for absence). "
                "Based on these parameters, you will output a severity score from 1 to 4 and a list of possible diseases that could result from consuming the contaminated water. "
                "The severity score should reflect the overall risk level, with 1 being very safe and 4 being extremely hazardous. "
                "Consider common waterborne diseases such as cholera, dysentery, typhoid, hepatitis A, and giardiasis when determining potential health risks."
            ),
        },
        {
            "role": "user",
            "content": (
                "Provide the severity score and list of potential diseases based on the following water quality data:\n"
                "pH: 7.0\n"
                "Turbidity: 1 NTU\n"
                "Electrical Conductivity: 200 µS/cm\n"
                "Chlorine Level: 0.5 mg/L\n"
                "Bacteria Level Present: No\n"
                "Format your response as follows:\n"
                "Severity: <score>\n"
                "Diseases: <comma-separated list of diseases>"
            ),
        },
        {
            "role": "assistant",
            "content": "Severity: 1\nDiseases: None",
        },
        {
            "role": "user",
            "content": (
                "Provide the severity score and list of potential diseases based on the following water quality data:\n"
                "pH: 5.0\n"
                "Turbidity: 10 NTU\n"
                "Electrical Conductivity: 800 µS/cm\n"
                "Chlorine Level: 0.1 mg/L\n"
                "Bacteria Level Present: Yes\n"
                "Format your response as follows:\n"
                "Severity: <score>\n"
                "Diseases: <comma-separated list of diseases>"
            ),
        },
        {
            "role": "assistant",
            "content": "Severity: 4\nDiseases: Cholera, Dysentery, Typhoid, Hepatitis A, Giardiasis",
        },
        {
            "role": "user",
            "content": (
                "Provide the severity score and list of potential diseases based on the following water quality data:\n"
                "pH: 6.5\n"
                "Turbidity: 5 NTU\n"
                "Electrical Conductivity: 500 µS/cm\n"
                "Chlorine Level: 0.3 mg/L\n"
                "Bacteria Level Present: Yes\n"
                "Format your response as follows:\n"
                "Severity: <score>\n"
                "Diseases: <comma-separated list of diseases>"
            ),
        },
        {
            "role": "assistant",
            "content": "Severity: 3\nDiseases: Dysentery, Typhoid, Giardiasis",
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following water quality data and provide a severity score and list of potential diseases:\n"
                f"pH: {data.ph}\n"
                f"Turbidity: {data.turbidity} NTU\n"
                f"Electrical Conductivity: {data.electrical_conductivity} µS/cm\n"
                f"Chlorine Level: {data.chlorine} mg/L\n"
                f"Bacteria Level Present: {'Yes' if data.bacteria_level else 'No'}\n"
                f"Format your response as follows:\n"
                f"Severity: <score>\n"
                f"Diseases: <comma-separated list of diseases>"
            ),
        },
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=sys_prompt,  # type: ignore
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None,
    )

    answer = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    answer = answer.replace("</s>", "")

    return answer
