import httpx
from pydantic import RootModel
from typing import Dict,Union
from .config import Config
from .utils import QuestionModel,NoulQuestionModel
class RequestJev:
    def __init__(self):
        self.base_url = Config.JEV_BASE_URL
        self.api_key = Config.JEV_API_KEY
        self.header = {
            "Content-Type": "application/json",
            'Authorization': f'Bearer {Config.JEV_API_KEY}'
        }
        self.model = 'jev'

    async def req(self,state:str,questions:RootModel[Dict[str,Union[QuestionModel,NoulQuestionModel]]]):
        payload = {
            "state":state,
            "model":self.model,
            "questions":questions.model_dump()
        }
        async with httpx.AsyncClient(timeout=30,verify=False,base_url=self.base_url) as client:
            res = await client.post('/systemone',json=payload,headers=self.header)
            res.raise_for_status()
            return res.json()


req = RequestJev()