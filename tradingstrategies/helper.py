import apis
from vwap_model import CaseData
from model import AuthConfig
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

def get_current_tick(auth: AuthConfig):
    case_data = CaseData.model_validate(apis.query_case_status(auth))
    return case_data.tick