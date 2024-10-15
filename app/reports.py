from decouple import config
from groq import Groq


class Report:
    """Report Model Class"""

    MODELS = {
        "gemini": "gemma2-9b-it",
        "llama": "llama-3.1-70b-versatile",
        "openai": "whisper-large-v3",
    }

    ai_prompt = '''
        These reports are from different Medical Practitioners,
        Summarize the reports by following these instructions.
        1. The products detailed in the reports have been used by those doctors or medical practitioners. 
        2. Give an important summary of the data and provide the key things to note. 
        3. Give an improvement suggestions for the products.
        4. You can mention the practitioner name if necessary or important in the summary
        5. Just go straight to the summary.
        Here is the data: """{}"""
    '''

    def __init__(self, reports) -> None:
        self.client = Groq(api_key=config("MODEL_API_KEY"))
        self.reports = self._clean_report(reports)
        self.prompt = self.ai_prompt.format(self.reports)

    def __repr__(self) -> str:
        return f"Report({self.reports})"

    def summarize(self, model):
        """Summary the reports provided."""

        # create chat completion
        completion = self.client.chat.completions.create(
            model=self.MODELS[model],
            messages=[{"role": "user", "content": self.prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
            # response_format={"type": "json_object"},
        )

        contents = []

        for chunk in completion:
            contents.append(chunk.choices[0].delta.content or "")

        return "".join(contents)  # summary

    def _clean_report(self, reports):
        # get the necessary data from the reports to feed the model
        cleaned_reports = [
            {
                "practitionerDetail": report.get("practitionerDetail", {}),
                "detailedProducts": report.get("detailedProducts", []),
                "notes": report.get("notes", {}),
            }
            for report in reports
        ]
        return cleaned_reports

    # def analyze(self):
    #     return {"totalEntry": len(self.reports)}
