
import unittest

from text_chunker import split_text_into_chunks


class TestResumeChunker(unittest.TestCase):

    def test_resume_without_headings(self):
        resume = """
        John Smith
        Software Engineer
        Worked with Java and Spring Boot.
        Built REST APIs and microservices.
        """

        chunks = split_text_into_chunks(
            resume, chunk_size=500, overlap=0
        )

        self.assertGreater(len(chunks), 0)
        self.assertTrue(
            all(chunk["section"] == "Other" for chunk in chunks)
        )

    def test_resume_with_one_section(self):
        resume = """
        EXPERIENCE
        Worked with Java and Spring Boot.
        """

        chunks = split_text_into_chunks(
            resume, chunk_size=500, overlap=0
        )

        self.assertEqual(chunks[0]["section"], "Experience")

    def test_resume_with_multiple_sections(self):
        resume = """
        PROFILE
        Software Engineer with backend experience.

        EDUCATION
        Bachelor of Computer Science.

        CERTIFICATIONS
        AWS Certified Developer.
        """

        chunks = split_text_into_chunks(
            resume, chunk_size=500, overlap=0
        )

        sections = {chunk["section"] for chunk in chunks}

        self.assertEqual(
            sections,
            {"Summary", "Education", "Certifications"}
        )

    def test_unknown_heading_is_preserved(self):
        resume = """
        Career Highlights
        Delivered enterprise software projects.
        """

        chunks = split_text_into_chunks(
            resume, chunk_size=500, overlap=0
        )

        self.assertEqual(chunks[0]["section"], "Other")
        self.assertIn("Career Highlights", chunks[0]["text"])


if __name__ == "__main__":
    unittest.main()
