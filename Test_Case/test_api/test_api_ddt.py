import pytest
import json
from Utilities.customLogger import LogGen

def load_fresh_test_data():
    file_path = "Test_Data/Login_data.json"  
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
     

class Test_ShopStack_API_DDT_Suite:
    logger = LogGen.apiloggen()

    Capture_access_token = None
    Capture_refresh_token = None

    @pytest.mark.parametrize("test_case", load_fresh_test_data())
    def test_login_api_data_driven(self, auth_client, test_case):
        self.logger.info(f"Starting test scenario: {test_case['scenario']}")
        
        response = auth_client.login(test_case["email"], test_case["password"])
        
        assert response.status_code == test_case["expected_status"], f"Status code mismatch for {test_case['scenario']}"

        if test_case["is_positive"] is True:
            response_json = response.json()
            tokens_dict = response_json.get("tokens", {})

            access = tokens_dict.get("access") or response_json.get("access_token")
            refresh = tokens_dict.get("refresh") or response_json.get("refresh_token")

            Test_ShopStack_API_DDT_Suite.Capture_access_token = access
            Test_ShopStack_API_DDT_Suite.Capture_refresh_token = refresh

            assert Test_ShopStack_API_DDT_Suite.Capture_access_token is not None, "Error: Access token not found"
            self.logger.info("Tokens captured successfully for valid user login")
        else:
            self.logger.info("Negative scenario handled correctly by server as expected")