import json
from pathlib import Path
from typing import Literal
from typing_extensions import TypedDict
from pydantic import BaseModel


class QuestionModel(BaseModel):
    type:Literal['choice','score']
    instructions:str
    criteria:list[str]

class  NoulCriteria(TypedDict):
    true:str
    false:str

class NoulQuestionModel(BaseModel):
    type:Literal['noul']
    instructions:str
    criteria:NoulCriteria

def build_choice_question(instructions: str, criteria: list[str]):
    """
    Choice 是 TypeSafe 的一种 System One（系统一）问题类型，用于从一个预定义的选项集合中选出唯一一项。

    Choice的请求体是3个字段:
        | 字段 | 说明 |
        |------|------|
        | **`state`** | 要被评估的内容（如一段工单文本、一段代码等） |
        | **`model`** | 选择处理请求的模型（如 `'jev-latest'`） |
        | **`questions`** | 一个 map，从**你自己起的 question id** 映射到问题对象 |
        question字段:
            | 字段 | 说明 |
            |------|------|
            | **`type`** | 固定为 `"choice"` |
            | **`instructions`** | 模型要回答的问题（提示语） |
            | **`criteria`** | 答案选项，也是一个 map——每个 key 是选项名称，每个 value 是对该选项的描述 |

    Choice 的答案包含三部分：
        choice：被选中的选项（概率最高的那个）
        probabilities：每个选项的完整概率分布（总和为 1）
        confidence：0 到 1 之间的置信度，由概率分布的“扁平程度”计算而来——概率分散在多个选项上则置信度低，集中在单一选项上则置信度高
    """
    return QuestionModel.model_validate({
        'type': 'choice',
        'instructions': instructions,
        'criteria': criteria,
    })


def build_score_question(instructions: str, criteria: list[str]):
    """
    Score 是 TypeSafe 的一种 System One 问题类型，用于在有序的、分级的描述（levels）上对内容进行打分/评级。
    E.G.:bug 有多严重、客户有多满意、某个候选人的 Python 经验有多少

    question 请求体:
    | 字段 | 说明 |
    |------|------|
    | **`type`** | 固定为 `"score"` |
    | **`instructions`** | 模型要回答的问题（它要评什么） |
    | **`criteria`** | **一个有序数组**，是从刻度低端到高端的 level 描述。至少 2 个 level，最多 10 个 |

    Score 的答案包含四部分：
        score：在 levels 光谱上的位置，可以在两级之间取小数
        probabilities：每个 level 的概率（总和为 1）
        legend：把每个 level 编号映射回它的描述
        confidence：0~1，由概率分布的扁平程度决定（集中在单一级别则高，分散则低）
    """

    return QuestionModel.model_validate({
        'type': 'score',
        "instructions": instructions,
        "criteria": criteria,
    })

def build_noul_question(instructions: str, criteria: NoulCriteria):
    """
    Noul 是 TypeSafe 的一种 System One 问题类型，用于评估一个 yes/no 问题，并返回“答案为是”的概率。
    Noul 的答案是一个单独的数字 noul，表示“答案为是”的概率：0 表示否，1 表示是。

    Questions说明:
         | 字段 | 说明 |
        |------|------|
        | **`type`** | 固定为 `"noul"` |
        | **`instructions`** | 模型要回答的是/否问题，或要它判断的一个陈述 |
        | **`criteria`** | **可选**。一个对象，包含 `true` 和 `false` 分别描述“是”和“否”意味着什么 |

    """
    return NoulQuestionModel.model_validate({
        'type': 'noul',
        'instructions': instructions,
        'criteria': criteria,
    })

def extract_python_skills():
    file = Path(__file__).resolve().parent.parent.parent / "data"/"python_skills"/"registry.json"
    data = json.load(open(file,encoding='utf-8'))
    return [x.get('name') for x in data if x.get('type')=='operator']

def extract_cpp_skill():
    file = Path(__file__).resolve().parent.parent.parent / "data" / "cpp_skills" / "registry.json"
    data = json.load(open(file, encoding='utf-8'))
    return [x.get('name') for x in data if x.get('type') == 'operator']

def choose_question(file_name:str,problem_id:str):
    file = Path(__file__).resolve().parent.parent.parent / "data"/"stage2"/file_name
    with open(file,encoding='utf-8') as f:
        for line in f:
            if problem_id in line and r'"status": "ok"' in line:
                return json.loads(line)
    return None


if __name__ == '__main__':
    print(extract_cpp_skill())
    print(choose_question('cpp_llama_runs.jsonl','abc388c'))