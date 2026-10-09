# gangmu-aibom-rules

[English](#english)

纲目 (Gangmu) 的 AIBOM 规则库，**目前还没有规则**，是占位仓库。

AI 清单的检测现在在工具本体里：`gangmu aibom` 扫描固件目录，认出模型文件（TFLite、ONNX、GGUF、safetensors 等）、
嵌在 C 数组里的 TFLite 模型和推理运行时（TFLite Micro、ONNX Runtime、CMSIS-NN 等），输出 CycloneDX 1.6 的
`machine-learning-model` 组件，见[使用指南](https://github.com/GANGMU-SBOM/gangmu/blob/main/docs/guides/aibom.md)。

计划：把模型格式识别与公开模型哈希做成数据放到这里，与 [gangmu-cbom-rules](https://github.com/GANGMU-SBOM/gangmu-cbom-rules)
同样的规则包方式分发。在规则格式定下来之前，这里不接受规则 PR；有想法请开 issue。

## English

The AIBOM rule base for gangmu. **It has no rules yet**; this repository is a placeholder.

Detection currently lives in the tool: `gangmu aibom` scans a firmware tree for model files (TFLite, ONNX, GGUF,
safetensors, ...), TFLite models embedded as C arrays and inference runtimes, and writes CycloneDX 1.6
`machine-learning-model` components. See the
[guide](https://github.com/GANGMU-SBOM/gangmu/blob/main/docs/guides/aibom.md).

Plan: move model-format recognition and public model hashes here as data, distributed as a rule pack like
[gangmu-cbom-rules](https://github.com/GANGMU-SBOM/gangmu-cbom-rules). Until the format is settled this repo does not
take rule PRs; open an issue with ideas.
