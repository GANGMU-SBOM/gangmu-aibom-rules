# 贡献规则 · Contributing

最容易的第一个 PR：给 `rules/runtimes/` 里的某个推理库补一个标识符，或新增一个推理库、一种模型文件格式。

1. 改或加一条 YAML（格式见 README）。运行时的 `patterns` 写标识符的正则，不要自己加 `\b` 或前缀边界。
2. 新增运行时或格式时在 `tests/test_rules.py` 的参数列表里加一行：一段会命中的真实标识符，或一个文件头。
3. `pip install -e '.[dev]' && pytest -q` 通过。
4. 在 PR 里写明标识符出自哪个库的哪个文件，格式的文件头出自哪份规范（链接即可）。

提交请带 `Signed-off-by`（`git commit -s`）。
