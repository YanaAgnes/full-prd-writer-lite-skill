#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_prd_quality.py")


class ValidatePrdQualityTest(unittest.TestCase):
    def run_validator(self, final_text: str, manifest_text: str | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            final = workspace / "FULL-PRD.md"
            final.write_text(textwrap.dedent(final_text).strip() + "\n", encoding="utf-8")
            cmd = [sys.executable, str(SCRIPT), "--final", str(final)]
            if manifest_text is not None:
                manifest = workspace / "ASSEMBLY-MANIFEST.md"
                manifest.write_text(textwrap.dedent(manifest_text).strip() + "\n", encoding="utf-8")
                cmd.extend(["--manifest", str(manifest)])
            return subprocess.run(cmd, text=True, capture_output=True)

    def test_rejects_placeholder_numbering_and_repeated_chapters(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            ### 2.x 临时概述
            # 2. 系统概述
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            # 7. 功能需求说明
            # 8. 外部系统协同需求说明
            # 9. 待确认事项
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("placeholder numbering", result.stderr)
        self.assertIn("duplicate chapter", result.stderr)

    def test_rejects_process_terms_and_vague_substitutes(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            本轮候选正文块后续确认。
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            # 7. 功能需求说明
            按功能权限配置的适用角色，按具体功能判断。
            # 8. 外部系统协同需求说明
            # 9. 待确认事项
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("process wording", result.stderr)
        self.assertIn("vague substitute", result.stderr)

    def test_rejects_internal_block_markers_in_final_output(self):
        result = self.run_validator(
            """
            <!-- PRD-BLOCK:B-0001 START -->
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            # 7. 功能需求说明
            # 8. 外部系统协同需求说明
            # 9. 待确认事项
            <!-- PRD-BLOCK:B-0001 END -->
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("internal marker", result.stderr)

    def test_rejects_scaffold_or_all_functions_manifest(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            # 7. 功能需求说明
            # 8. 外部系统协同需求说明
            # 9. 待确认事项
            """,
            """
            <!-- ASSEMBLY-MANIFEST:START -->
            | block_id | requirement_unit | source_file | state | order | sha256 | final_location |
            | --- | --- | --- | --- | --- | --- | --- |
            | B-DOC-CH07-SOURCE | ALL-FUNCTIONS | chapters/scaffold.md | 已冻结 | 10 | 0000000000000000000000000000000000000000000000000000000000000000 | 7 |
            <!-- ASSEMBLY-MANIFEST:END -->
            """,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scaffold source", result.stderr)
        self.assertIn("ALL-FUNCTIONS", result.stderr)

    def test_rejects_extra_formal_chapters(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            # 7. 功能需求说明
            # 8. 外部系统协同需求说明
            # 9. 待确认事项
            # 11. 风险与依赖
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("extra chapter", result.stderr)

    def test_rejects_wrong_chapter_titles(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 背景与目标
            # 3. 需求范围
            # 4. 用户角色与权限
            # 5. 名词解释
            # 6. 业务流程
            # 7. 功能需求详情
            # 8. 页面与交互规范
            # 9. 附录
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("chapter title", result.stderr)

    def test_rejects_shallow_requirement_sections(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            # 1. 文档信息
            # 2. 系统概述
            # 3. 文档覆盖范围
            # 4. 用户角色与权限
            # 5. 业务流程
            # 6. 用户故事与使用路径
            用户可以使用系统。
            # 7. 功能需求说明
            系统提供账户管理。
            # 8. 外部系统协同需求说明
            系统对接外部服务。
            # 9. 待确认事项
            无。
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requirement depth", result.stderr)

    def test_rejects_raw_requirement_unit_second_level_headings(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            建立正式基线。
            # 1. 文档信息
            示例文档。
            # 2. 系统概述
            示例后台系统用于统一管理账户。
            # 3. 文档覆盖范围
            覆盖账户列表。
            # 4. 用户角色与权限
            系统管理员可访问。
            # 5. 业务流程
            管理员进入账户管理并查看列表。
            # 6. 用户故事与使用路径
            ## F-ACCOUNT-001 账户列表
            | 故事编号 | 用户目标 | 关联功能 |
            | --- | --- | --- |
            | US-ACCOUNT-001 | 管理员查看账户列表。 | F-ACCOUNT-001 |
            # 7. 功能需求说明
            ## 7.1 功能结构总览
            ## F-ACCOUNT-001 账户列表
            **功能定位**
            - 角色：系统管理员。
            **入口与前置条件**
            - 入口：后台菜单。
            **页面、区域与字段**
            - 字段：账户名。
            **功能与交互规则**
            - 规则编号：ACCOUNT-R-001，查询列表。
            **异常、失败与补偿**
            - 异常：无权限隐藏。
            **验收口径**
            - AC-ACCOUNT-001：仅展示授权账户。
            # 8. 外部系统协同需求说明
            ## 8.1 外部系统协同总览
            无外部协同。
            # 9. 待确认事项
            无。
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("presentation structure", result.stderr)

    def test_rejects_empty_required_chapter_body(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            | 版本 | 日期 | 说明 |
            | --- | --- | --- |
            | V1.0 | 2026-06-09 | 建立正式基线。 |
            # 1. 文档信息
            | 项目 | 内容 |
            | --- | --- |
            | 系统名称 | 示例后台系统 |
            # 2. 系统概述
            # 3. 文档覆盖范围
            本文覆盖账户列表查询、账户查看和统一身份协同。
            # 4. 用户角色与权限
            系统管理员可查看授权范围内账户，普通用户不进入后台账户管理。
            # 5. 业务流程
            系统管理员进入账户管理后筛选账户、查看列表，并由系统校验身份权限。
            # 6. 用户故事与使用路径
            ## 6.1 用户故事总览
            | 故事编号 | 用户目标 | 关联功能 |
            | --- | --- | --- |
            | US-ACCOUNT-001 | 管理员查看账户列表。 | F-ACCOUNT-001 |
            # 7. 功能需求说明
            ## 7.1 功能结构总览
            ## 7.2 账户管理
            ### 7.2.1 F-ACCOUNT-001 账户列表
            **功能定位**
            - 角色：系统管理员。
            **入口与前置条件**
            - 入口：后台菜单“账户管理”。
            **页面、区域与字段**
            - 字段：账户名、状态、创建时间。
            **功能与交互规则**
            - 规则编号：ACCOUNT-R-001，支持查询、筛选、查看详情。
            **异常、失败与补偿**
            - 异常：无权限时隐藏入口。
            **验收口径**
            - AC-ACCOUNT-001：管理员只能看到授权范围内账户。
            # 8. 外部系统协同需求说明
            ## 8.1 外部系统协同总览
            | 外部系统 | 关联功能 |
            | --- | --- |
            | 统一身份 | F-ACCOUNT-001 |
            ## 8.2 统一身份
            ### 8.2.1 EXT-IAM-001 统一身份协同
            - 本系统职责：展示账户列表并传递用户标识。
            - 外部系统职责：返回账户身份与权限结果。
            # 9. 待确认事项
            无。
            """
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty chapter", result.stderr)

    def test_accepts_clean_formal_prd(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            | 版本 | 日期 | 说明 |
            | --- | --- | --- |
            | V1.0 | 2026-06-09 | 建立正式基线。 |
            # 1. 文档信息
            | 项目 | 内容 |
            | --- | --- |
            | 系统名称 | 示例后台系统 |
            # 2. 系统概述
            示例后台系统用于统一管理账户、权限与基础运营数据。
            # 3. 文档覆盖范围
            本文覆盖账户列表查询、账户查看和统一身份协同。
            # 4. 用户角色与权限
            系统管理员可查看授权范围内账户，普通用户不进入后台账户管理。
            # 5. 业务流程
            系统管理员进入账户管理后筛选账户、查看列表，并由系统校验身份权限。
            # 6. 用户故事与使用路径
            ## 6.1 用户故事总览
            | 故事编号 | 用户目标 | 关联功能 |
            | --- | --- | --- |
            | US-ACCOUNT-001 | 管理员查看账户列表。 | F-ACCOUNT-001 |
            # 7. 功能需求说明
            ## 7.1 功能结构总览
            ## 7.2 账户管理
            ### 7.2.1 F-ACCOUNT-001 账户列表
            **功能定位**
            - 角色：系统管理员。
            **入口与前置条件**
            - 入口：后台菜单“账户管理”。
            **页面、区域与字段**
            - 字段：账户名、状态、创建时间。
            **功能与交互规则**
            - 规则编号：ACCOUNT-R-001，支持查询、筛选、查看详情。
            **异常、失败与补偿**
            - 异常：无权限时隐藏入口。
            **验收口径**
            - AC-ACCOUNT-001：管理员只能看到授权范围内账户。
            # 8. 外部系统协同需求说明
            ## 8.1 外部系统协同总览
            | 外部系统 | 关联功能 |
            | --- | --- |
            | 统一身份 | F-ACCOUNT-001 |
            ## 8.2 统一身份
            ### 8.2.1 EXT-IAM-001 统一身份协同
            - 本系统职责：展示账户列表并传递用户标识。
            - 外部系统职责：返回账户身份与权限结果。
            # 9. 待确认事项
            无。
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("QUALITY_PASSED", result.stdout)

    def test_accepts_official_narrative_chapter_7_without_fixed_leaf_template(self):
        result = self.run_validator(
            """
            # 0. 修订记录
            | 版本 | 日期 | 说明 |
            | --- | --- | --- |
            | V1.0 | 2026-06-24 | 建立正式基线。 |
            # 1. 文档信息
            | 项目 | 内容 |
            | --- | --- |
            | 系统名称 | 智能搜索系统 |
            # 2. 系统概述
            智能搜索系统为用户提供统一搜索、资源发现和知识问答能力。
            # 3. 文档覆盖范围
            本文覆盖智能搜索首页、对话结果页和历史会话。
            # 4. 用户角色与权限
            登录用户可访问智能搜索，超级用户可查看管理入口。
            # 5. 业务流程
            用户从首页输入问题，系统生成结果并允许追问或回放历史会话。
            # 6. 用户故事与使用路径
            ## 6.1 用户故事总览
            | 故事编号 | 用户目标 | 关联功能 |
            | --- | --- | --- |
            | US-SEARCH-001 | 登录用户从首页提交问题并查看结果。 | F-SEARCH-001 |
            # 7. 功能需求说明
            ## 7.1 功能结构总览
            | 功能编号 | 层级 | 功能名称 | 类型 | 上级节点 | 定位/说明 | 详述位置 |
            | --- | --- | --- | --- | --- | --- | --- |
            | F-SEARCH-001 | 叶子功能 | 智能搜索首页 | 页面功能 | M-SEARCH | 用户提交搜索问题的首页入口。 | 7.2.1 |
            ## 7.2 智能搜索
            ### 7.2.1 F-SEARCH-001 智能搜索首页
            #### 页面路径与入口
            页面路径为智能搜索 / 首页。入口包括左侧导航“智能搜索”和登录后默认首页。
            #### 页面整体布局说明
            左侧固定站点壳展示导航，主区域居中展示欢迎语、搜索框、模式按钮和推荐内容。
            #### 页面交互说明
            用户在搜索框输入问题后点击发送进入对话结果页；输入为空时按钮保持灰色并阻断提交。搜索问题字段必填，长度为 1-200 字，超过限制时提示“限制输入200个字符”。
            #### 字段与数据规则
            | 字段名称 | 字段 key | 规则 |
            | --- | --- | --- |
            | 搜索问题 | question | 必填，1-200 字。 |
            | 搜索模式 | category | 综合、找数据、找组件、找应用、知识问答。 |
            #### 权限与异常说明
            登录用户可访问并提交搜索；未登录用户无入口。无结果时展示空状态，服务超时时提示用户稍后重试。
            #### 验收口径
            - AC-SEARCH-001：用户输入 1-200 字问题后可进入结果页。
            # 8. 外部系统协同需求说明
            ## 8.1 外部系统协同总览
            无外部协同。
            # 9. 待确认事项
            无。
            """
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("QUALITY_PASSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
