# 纲目 AIBOM 规则库 · gangmu-aibom-rules

**免费的 AI 清单规则库：`gangmu aibom` 在固件和源码里找哪些模型文件格式、哪些推理库，都写在这里，社区共同维护。**

[纲目 Gangmu](https://github.com/GANGMU-SBOM/gangmu) 的 `gangmu aibom` 命令列出目录里的机器学习模型和推理运行时，输出 CycloneDX 1.6 的 AIBOM。
识别表原来写在工具代码里；现在它是数据，可以用规则包补充或覆盖，新增一个推理库就是提一个小 YAML 的 PR，不用改工具、不用等工具发版。

[English](README.en.md) · [贡献规则](CONTRIBUTING.md) · [AIBOM 指南](https://github.com/GANGMU-SBOM/gangmu/blob/main/docs/guides/aibom.md)

## 安装

```bash
# 尚未发布到 PyPI：先从源码安装（gangmu 需 0.9.0 或更高，发布前用 git main）
pip install git+https://github.com/GANGMU-SBOM/gangmu.git@main
pip install git+https://github.com/GANGMU-SBOM/gangmu-aibom-rules.git
gangmu aibom firmware/                 # 自动读取已安装的 kind 为 aibom 的规则包
gangmu aibom firmware/ --rules rules/  # 或者指定目录，便于本地改规则
```

## 里面有什么

| 文件 | 内容 |
| --- | --- |
| `rules/formats/model-formats.yaml` | 模型文件格式：TFLite、GGUF、ExecuTorch、ONNX、safetensors、PyTorch、Keras/HDF5、Core ML、RKNN、MNN |
| `rules/runtimes/inference-runtimes.yaml` | 推理运行时：TFLite Micro、TFLite、ONNX Runtime、CMSIS-NN、Edge Impulse、microTVM、NNoM、ExecuTorch、llama.cpp、ncnn、MNN、ESP-DL、STM32Cube.AI、RKNN、TensorFlow C |

这两个文件是 gangmu 内置识别表的原样导出，`tests/test_rules.py` 会逐项比对，防止两边悄悄分叉。同名 `key` 替换内置项，新 `key` 新增。

## 规则格式

**模型格式**（`formats/*.yaml`，列表放在 `formats:` 下）：

```yaml
formats:
  - key: edgeimpulse-eim          # 小写字母、数字、连字符
    name: Edge Impulse Linux model
    suffixes: ['.eim']            # 扩展名，带点
    magic: {offset: 4, ascii: 'TFL3'}   # 可选；也可以写 hex: '54464c33'。文件头对上就算“按签名认出”
    note: 可选，会出现在输出里的提示
```

`suffixes` 和 `magic` 至少写一个。只靠扩展名认出的模型，输出里标 `by extension`。

**推理运行时**（`runtimes/*.yaml`，列表放在 `runtimes:` 下）：

```yaml
runtimes:
  - key: acme-rt
    name: ACME runtime
    patterns: ['acme_infer\w*', 'acme/rt\.h']   # 标识符的正则；扫描会在前面加标识符边界
```

运行时在 `.c .cc .cpp .h .hpp .ino .py` 等源码里按标识符认，**不代表它编进了固件**。
编进 C 数组的 TFLite 模型、GGUF 头里的架构这类需要读内容的识别仍在工具里。

## 许可

规则：CDLA-Permissive-2.0；打包代码：Apache-2.0。
