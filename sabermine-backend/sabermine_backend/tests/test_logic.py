import string
import sabermine_backend.api.logic as logic
from unittest.mock import patch
from fastapi import UploadFile
from io import BytesIO


class TestGenerateShortCode:

    def test_generate_short_code_default_length(self):
        code = logic.generate_short_code()
        assert len(code) == 7
        assert all(c in string.ascii_letters + string.digits for c in code)

    def test_generate_short_code_custom_length(self):
        length = 10
        code = logic.generate_short_code(length)
        assert len(code) == length
        assert all(c in string.ascii_letters + string.digits for c in code)


class TestIsCodeUnique:

    def test_is_code_unique_true(self, dynamodb_mock):
        code = "uniqueCode123"
        result = logic.is_code_unique(code)
        assert result is True

    def test_is_code_unique_false(self, dynamodb_mock):
        code = "existingCode123"
        dynamodb_mock.put_item(Item={"short_code": code})
        result = logic.is_code_unique(code)
        assert result is False


class TestGenerateUniqueCode:

    def test_generate_unique_code(self, dynamodb_mock):
        code = logic.generate_unique_code()
        assert len(code) == 7
        assert all(c in string.ascii_letters + string.digits for c in code)
        assert logic.is_code_unique(code) is True

    def test_generate_unique_code_with_existing_codes(self, dynamodb_mock):
        existing_codes = {"code1", "code2", "code3"}
        for code in existing_codes:
            dynamodb_mock.put_item(Item={"short_code": code})
        code = logic.generate_unique_code()
        assert len(code) == 7
        assert all(c in string.ascii_letters + string.digits for c in code)
        assert code not in existing_codes
        assert logic.is_code_unique(code) is True

    @patch('sabermine_backend.api.logic.generate_short_code')
    def test_generate_unique_code_mocked(self, mock_generate_short_code, dynamodb_mock):
        existing_codes = ["code1", "code2", "code3"]
        for code in existing_codes:
            dynamodb_mock.put_item(Item={"short_code": code})
        mock_generate_short_code.side_effect = existing_codes + ["uniqueCode123"]
        code = logic.generate_unique_code()
        assert code == "uniqueCode123"
        assert logic.is_code_unique(code) is True


class TestGetDynamoDBTable:

    def test_get_dynamodb_table(self, dynamodb_mock):
        table = logic.get_dynamodb_table()
        assert table.table_name == "ShortenedURLs"


class TestShortenURL:

    def test_shorten_url(self, dynamodb_mock):
        original_url = "https://example.com"
        short_code = logic.shorten_url(original_url)
        assert len(short_code.split('/')[-1]) == 7
        assert all(c in string.ascii_letters + string.digits for c in short_code.split('/')[-1])
        response = dynamodb_mock.get_item(Key={"short_code": short_code.split('/')[-1]})
        assert "Item" in response
        assert response["Item"]["original_url"] == original_url


class TestRetrieveURL:

    def test_retrieve_url_existing(self, dynamodb_mock):
        short_code = "existingCode123"
        original_url = "https://example.com"
        dynamodb_mock.put_item(Item={"short_code": short_code, "original_url": original_url})
        retrieved_url = logic.retrieve_url(short_code)
        assert retrieved_url == original_url

    def test_retrieve_url_non_existing(self, dynamodb_mock):
        short_code = "nonExistingCode123"
        retrieved_url = logic.retrieve_url(short_code)
        assert retrieved_url is None


class TestGetS3Bucket():

    def test_get_s3_bucket(self, s3_mock):
        bucket = logic.get_s3_bucket()
        assert bucket.name == logic.S3_BUCKET


class TestUploadFile():

    def test_upload_file(self, tmpdir, s3_mock):
        test_file = UploadFile(
            filename="test.txt",
            file=BytesIO(b"Hello, this is a test file!"),
        )

        file_url = logic.upload_file(test_file)

        assert file_url == f"https://{s3_mock.name}.s3.{logic.AWS_REGION}.amazonaws.com/{test_file.filename}"


class TestGetAllShortUrls:

    def test_get_all_short_urls_default_limit(self, dynamodb_mock):
        for i in range(15):
            dynamodb_mock.put_item(Item={"short_code": f"code{i}", "original_url": f"https://example{i}.com"})

        result = logic.get_all_short_urls()
        assert result["count"] == 10
        assert len(result["short_urls"]) == 10
        assert result["next_key"] is not None

    def test_get_all_short_urls_custom_limit(self, dynamodb_mock):
        for i in range(15):
            dynamodb_mock.put_item(Item={"short_code": f"code{i}", "original_url": f"https://example{i}.com"})

        result = logic.get_all_short_urls(limit=5)
        assert result["count"] == 5
        assert len(result["short_urls"]) == 5
        assert result["next_key"] is not None

    def test_get_all_short_urls_with_last_evaluated_key(self, dynamodb_mock):
        for i in range(15):
            dynamodb_mock.put_item(Item={"short_code": f"code{i}", "original_url": f"https://example{i}.com"})

        first_result = logic.get_all_short_urls(limit=5)
        second_result = logic.get_all_short_urls(limit=5, last_evaluated_key=first_result["next_key"])

        assert first_result["count"] == 5
        assert len(first_result["short_urls"]) == 5
        assert first_result["next_key"] is not None

        assert second_result["count"] == 5
        assert len(second_result["short_urls"]) == 5
        assert second_result["next_key"] is not None

    def test_get_all_short_urls_no_data(self, dynamodb_mock):
        result = logic.get_all_short_urls()
        assert result["count"] == 0
        assert len(result["short_urls"]) == 0
        assert result["next_key"] is None
