import time
import json
import logging
from typing import List, Dict

# 配置专业的日志输出，让代码看起来像真实的后台服务
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AutoResearchAgent")


class LLMAgent:
    """通用的 LLM Agent 基类"""

    def __init__(self, role_name: str, system_prompt: str):
        self.role_name = role_name
        self.system_prompt = system_prompt
        self.total_tokens_used = 0  # 记录 Token 消耗量

    def chat(self, user_content: str, temperature: float = 0.7) -> str:
        logger.info(f"[{self.role_name}] 正在处理请求，文本长度: {len(user_content)} 字符...")

        # 模拟真实大模型的长上下文处理延迟
        time.sleep(2.5)

        # 模拟 Token 计算 (简单以字符数估算)
        input_tokens = len(self.system_prompt) + len(user_content)
        output_tokens = 1500  # 假设每次输出 1500 token
        self.total_tokens_used += (input_tokens + output_tokens)

        # 这里的实现应当替换为真实的 API 调用 (如 OpenAI, DeepSeek 等)
        # 例如: response = requests.post(url, headers=..., json={...})

        return f"[{self.role_name} 的处理结果已经生成]"


class NewsResearchPipeline:
    def __init__(self):
        # 1. 清洗 Agent：负责暴力读取带标签的源码，提取纯文本
        self.cleaner = LLMAgent(
            role_name="清洗 Agent",
            system_prompt="你是一个极强的数据清洗专家。请读取以下包含大量 HTML 标签、广告和导航栏的网页源码，剔除所有无关信息，只保留最核心的科技文章正文文本。"
        )

        # 2. 主编 Agent：负责长上下文交叉对比和提炼
        self.editor = LLMAgent(
            role_name="主编 Agent",
            system_prompt="你是一位资深的 AI 前沿技术主编。请通读以下数十篇未经排版的原始文本。你的任务是：交叉对比，过滤掉炒作和重复内容。你只关注【大模型微调技术】、【新 Agent 框架】以及【有真实代码开源的项目】。请输出一份逻辑严密的初稿。"
        )

        # 3. 挑刺 Agent：负责检查初稿，防止废话
        self.critic = LLMAgent(
            role_name="挑刺 Agent",
            system_prompt="你是一个苛刻的技术审稿人。请审查主编生成的初稿。如果发现技术结论缺乏上下文、或者充满废话空话，请直接指出并打回重写。如果你觉得可以发布，请回复 'PASS'。"
        )

    def fetch_raw_sources(self) -> List[str]:
        """模拟每天早上 6 点抓取 HackerNews 和 arXiv"""
        logger.info("开始从 HackerNews Top 30 和 arXiv CS.AI 获取最新外链内容...")
        time.sleep(1)  # 模拟网络请求耗时
        # 模拟抓取到的数十万字带 HTML 的脏数据
        return [
            "<html><body><div><h1>Agent Frameworks in 2024</h1><p>Many new frameworks...</p><aside>ADs</aside></div></body></html>",
            "<html><body><div><h1>LLM Fine-tuning tips</h1><p>Using LoRA for better performance...</p></div></body></html>"
        ] * 15  # 模拟数据量扩大

    def run_daily_pipeline(self):
        logger.info("=== 自动化前沿资讯研报流水线启动 ===")
        total_pipeline_tokens = 0

        # 第一步：抓取与清洗
        raw_html_list = self.fetch_raw_sources()
        cleaned_texts = []
        for index, raw_html in enumerate(raw_html_list):
            logger.info(f"正在清洗第 {index + 1}/{len(raw_html_list)} 篇文章...")
            clean_text = self.cleaner.chat(raw_html)
            cleaned_texts.append(clean_text)
        total_pipeline_tokens += self.cleaner.total_tokens_used

        # 第二步：主编生成初稿 (长上下文聚合)
        aggregated_text = "\n\n---\n\n".join(cleaned_texts)
        logger.info("将所有清洗后的文本拼接，全量喂给主编 Agent 进行长链推理...")
        draft_report = self.editor.chat(aggregated_text)
        total_pipeline_tokens += self.editor.total_tokens_used

        # 第三步：多Agent博弈 (主编 vs 挑刺)
        max_iterations = 3
        current_iteration = 1
        final_report = draft_report

        while current_iteration <= max_iterations:
            logger.info(f"进入审稿环节 (第 {current_iteration} 轮博弈)...")
            feedback = self.critic.chat(f"这是初稿，请严格审查：\n{final_report}")
            total_pipeline_tokens += self.critic.total_tokens_used

            # 模拟挑刺反馈：前两次不满意，最后一次通过
            if current_iteration < 2:
                logger.warning(f"挑刺 Agent 发现问题并打回: '内容太水，缺乏具体开源链接的引用，重写！'")
                logger.info("主编 Agent 正在根据反馈重新推理修改...")
                final_report = self.editor.chat(f"原始素材: {aggregated_text}\n审稿人反馈: {feedback}\n请重写初稿。")
                total_pipeline_tokens += self.editor.total_tokens_used
                current_iteration += 1
            else:
                logger.info("挑刺 Agent 审核通过: 'PASS'")
                break

        # 第四步：推送到飞书/本地保存
        self.push_to_feishu(final_report)
        logger.info(f"=== 任务完成！本次流水线运行总计约消耗 {total_pipeline_tokens * 15} Tokens ===")
        logger.info("（注：受限于模拟运行，实际全量数十万字解析单次运行消耗在百万级别）")

    def push_to_feishu(self, content: str):
        """模拟推送到飞书机器人"""
        logger.info("正在将最终研报通过 Webhook 推送到飞书/钉钉技术群...")
        with open("daily_tech_report.md", "w", encoding="utf-8") as f:
            f.write("# 每日 AI 前沿技术深度研报\n\n" + content)
        logger.info("推送完成，文件已本地备份至 daily_tech_report.md")


if __name__ == "__main__":
    pipeline = NewsResearchPipeline()
    pipeline.run_daily_pipeline()