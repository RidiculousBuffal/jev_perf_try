import json
import logging

from pydantic import RootModel

from .req import req
from .utils import choose_question, extract_cpp_skills, extract_python_skills, skill_id_to_name, build_choice_question, \
    build_noul_question, NoulCriteria


class JEV:
    def __init__(self, file_name: str, mode: str):
        self.file_name = file_name
        self.req = req
        self.logger = logging.getLogger('JEV')
        self.python_skills = extract_python_skills()
        self.cpp_skills = extract_cpp_skills()
        self.mode = mode

    async def call(self, problem_id):
        question = choose_question(self.file_name, problem_id)
        statement = question.get('statement')
        slow_code = question.get('slow_code')
        self.logger.info("题目\n%s\n慢代码:\n%s \n", statement, slow_code)
        skill_sets = question.get('skill_sets')
        skills = [x.get('selected_skills') for x in skill_sets if x.get('confidence') == 'high']
        if len(skills) > 0:
            skills = skills[0]
            self.logger.info('原始的skill 分别是:\n')
            for skill in skills:
                self.logger.info(skill_id_to_name(skill.get('skill_id'), self.mode))

        # state = 被评估的内容（输入的数据/素材）
        # instructions = 要模型回答的问题（针对这份内容提的问题）
        choices = build_choice_question("which skill should be selected to make the code faster",
                                        self.python_skills if self.mode == 'python' else self.cpp_skills)
        noul = build_noul_question(
            'Based on the problem description, do you think this code still has room for optimization?',
            NoulCriteria(true='Yes, there is still room for optimization in this code.',
                         false='No, this code is already optimal, and there is very little room for optimization.'))
        state = f"""
Problem: {statement}
CurrentCode: {slow_code}
"""
        res = await self.req.req(state, RootModel.model_validate({"which_skill_should_use": choices, "room_for_optimize": noul}))
        self.logger.info(json.dumps(res, indent=4, ensure_ascii=False))
