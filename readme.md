# NDDrone-SDK (原flymode)

基于脑机接口（BCI）的意念无人机控制系统

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## 核心功能

- 🎯 **SSVEP视觉刺激系统**
  - 垂直同步定帧闪烁动画
  - 全屏显示（1920x1080@60Hz）

- 🚁 **无人机智能控制**
  - 支持识别9种SSVEP视觉指令（可自定义搭配飞机动作）
  - NeuroDance脑电采集设备支持
  - RoboMaster无人机平台支持

## 系统架构

```plain
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  视觉刺激显示    │───▶│  脑电信号采集    │───▶│  信号处理算法    │
│  (PsychoPy)     │    │   (ND8)         │    │   (FB-CCA)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
                                            ┌─────────────────┐
                                            │  无人机控制      │
                                            │  (RoboMaster)   │
                                            └─────────────────┘
```

## 快速开始

### 环境要求

- Python 3.x
- Node.js (>=14.x)
- 大疆RMTT无人机
- ND8 (>=Pro)
- Windows (>=10)

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

编辑 `config.ini` 文件，配置以下参数：

```ini
[frames]
count=180 # 闪烁帧总量

[run]
logfile=log.txt # 日志文件名
```

### 运行

你必须先安装yarn（`npm i yarn -g`），然后执行以下命令编译cli脚手架：

```bash
yarn install
yarn build
```

### 编译刺激块

```bash
./drone generate
```

### 启动刺激窗口&飞控

```bash
./drone start
```

## 技术栈

- **信号处理**: NumPy, SciPy, scikit-learn
- **视觉刺激**: PsychoPy
- **无人机控制**: RoboMaster SDK
- **网络通信**: Socket(UDP)
- **生成刺激块帧图**：PIL
- **编译**：PyInstaller

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/Rundll86/NDDrone-SDK/issues)

## 致谢

感谢所有为本项目做出贡献的开发者和研究人员。

---

**用意念控制未来** 🧠✨

Made by 重庆十一中WRC
> Readme written by GPT-4o

</div>
