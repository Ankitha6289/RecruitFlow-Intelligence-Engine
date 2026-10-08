from io import BytesIO

import pandas as pd

from app.models.candidate import Candidate


class ExcelService:

    @staticmethod
    def export_candidates():

        candidates = Candidate.query.all()

        data = []

        for candidate in candidates:

            data.append({

                "Candidate ID": candidate.candidate_id,

                "Full Name": candidate.full_name,

                "Email": candidate.email,

                "Phone": candidate.phone,

                "LinkedIn": candidate.linkedin,

                "GitHub": candidate.github,

                "Portfolio": candidate.portfolio,

                "Address": candidate.address

            })

        df = pd.DataFrame(data)

        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:

            df.to_excel(

                writer,

                index=False,

                sheet_name="Candidates"

            )

        output.seek(0)

        return output