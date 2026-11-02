
import unittest

from metadata_extractor import extract_employment_metadata


class TestMetadataExtractor(unittest.TestCase):

    def test_extract_employment_record(self):
        resume = """
        PROFESSIONAL EXPERIENCE
        ABC Technologies — Senior Software Engineer
        Sydney, Australia | Jan 2022 – Present | Client: Example Corp
        Developed backend microservices.
        """

        records = extract_employment_metadata(resume)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["employer"], "ABC Technologies")
        self.assertEqual(
            records[0]["job_title"],
            "Senior Software Engineer"
        )
        self.assertEqual(records[0]["start_date"], "Jan 2022")
        self.assertEqual(records[0]["end_date"], "Present")
        self.assertEqual(records[0]["client"], "Example Corp")

    def test_multiple_employers(self):
        resume = """
        Company A — Software Engineer
        Sydney | Jan 2020 – Dec 2021

        Company B — Developer
        Melbourne | Jan 2022 – Present
        """

        records = extract_employment_metadata(resume)

        self.assertEqual(len(records), 2)

    def test_certifications_are_not_employment(self):
        resume = """
        AWS Certified AI Practitioner — Amazon Web Services
        """

        records = extract_employment_metadata(resume)

        self.assertEqual(len(records), 0)

    def test_education_is_not_employment(self):
        resume = """
        Bachelor of Engineering — Example University
        """

        records = extract_employment_metadata(resume)

        self.assertEqual(len(records), 0)

    def test_employment_without_client(self):
        resume = """
        ABC Technologies — Backend Developer
        Sydney | Feb 2021 – Mar 2023
        """

        records = extract_employment_metadata(resume)

        self.assertEqual(len(records), 1)
        self.assertIsNone(records[0]["client"])


if __name__ == "__main__":
    unittest.main()
