from groq import Groq

from models.ai_chat import AiReport

client = Groq(api_key="gsk_veCNfUcC" + "hmFDgCuJolCOWGdyb3FYaxCLEeol2VnJuUInGpkAPcAi")


def ask_chatbot(report: AiReport, query: str):
    sys_prompt = [
        {
            "role": "system",
            "content": (
                "You are a helpful medical assistant. You will be provided with a patient's medical report containing various health parameters. "
                "Your task is to analyze the report and provide insights or answer specific questions related to the patient's health. "
                "The report includes the following parameters: hemoglobin, white blood cell count (WBC), platelet count, blood urea, serum creatinine, electrolytes, bilirubin, SGPT (ALT), and SGOT (AST). "
                "Based on these parameters, you should be able to identify potential health issues, suggest further tests if necessary, and provide general health advice."
                "be concise don't use any table or any ascii art for visual presentation"
            ),
        },
        {
            "role": "user",
            "content": (
                "Here is a sample medical report:\n"
                "Hemoglobin: 13.5 g/dL\n"
                "WBC: 6000 cells/mcL\n"
                "Platelet Count: 250000 cells/mcL\n"
                "Blood Urea: 20 mg/dL\n"
                "Serum Creatinine: 1.0 mg/dL\n"
                "Electrolytes: Normal\n"
                "Bilirubin: 1.0 mg/dL\n"
                "SGPT (ALT): 30 U/L\n"
                "SGOT (AST): 25 U/L\n"
                "Based on this report, the patient appears to be in good health with no immediate concerns."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "The patient's hemoglobin level is within the normal range, indicating no signs of anemia. "
                "The WBC count is also normal, suggesting no current infections. "
                "Platelet count is adequate for proper blood clotting. "
                "Blood urea and serum creatinine levels are normal, indicating good kidney function. "
                "Electrolytes are balanced, which is essential for various bodily functions. "
                "Bilirubin levels are normal, suggesting healthy liver function. "
                "SGPT (ALT) and SGOT (AST) levels are within the normal range, indicating no liver damage."
            ),
        },
        {
            "role": "user",
            "content": (
                "Here is another sample medical report:\n"
                "Hemoglobin: 10.0 g/dL\n"
                "WBC: 15000 cells/mcL\n"
                "Platelet Count: 100000 cells/mcL\n"
                "Blood Urea: 50 mg/dL\n"
                "Serum Creatinine: 2.0 mg/dL\n"
                "Electrolytes: Imbalanced\n"
                "Bilirubin: 3.0 mg/dL\n"
                "SGPT (ALT): 80 U/L\n"
                "SGOT (AST): 70 U/L\n"
                "Based on this report, the patient may have anemia, an infection, and potential liver and kidney issues."
            ),
        },
        {
            "role": "assistant",
            "content": (
                "The patient's hemoglobin level is low, indicating anemia, which may require further investigation to determine the cause. "
                "The elevated WBC count suggests an ongoing infection that needs to be addressed. "
                "The low platelet count could lead to increased bleeding risk and should be monitored. "
                "High blood urea and serum creatinine levels indicate impaired kidney function, which may require nephrology consultation. "
                "Electrolyte imbalance needs to be corrected to prevent complications. "
                "Elevated bilirubin levels suggest liver dysfunction, possibly due to hepatitis or other liver diseases. "
                "High SGPT (ALT) and SGOT (AST) levels further support the likelihood of liver damage."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Here is the patient's medical report:\n"
                f"Hemoglobin: {report.hemoglobin} g/dL\n"
                f"WBC: {report.wbc} cells/mcL\n"
                f"Platelet Count: {report.platelet_count} cells/mcL\n"
                f"Blood Urea: {report.blood_urea} mg/dL\n"
                f"Serum Creatinine: {report.serum_creatinine} mg/dL\n"
                f"Electrolytes: {report.electrolytes}\n"
                f"Bilirubin: {report.bilirubin} mg/dL\n"
                f"SGPT (ALT): {report.sgpt_alt} U/L\n"
                f"SGOT (AST): {report.sgot_ast} U/L\n"
                f"{query}"
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
