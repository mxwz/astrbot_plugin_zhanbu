<div align="center">

[//]: # (![:name]&#40;https://count.getloli.com/@astrbot_plugin_zhanbu?name=astrbot_plugin_zhanbu&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto&#41;)

# astrbot_plugin_zhanbu

_✨ [astrbot](https://github.com/AstrBotDevs/AstrBot) 占卜起卦插件 ✨_  

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-3.4%2B-orange.svg)](https://github.com/Soulter/AstrBot)
[![GitHub](https://img.shields.io/badge/作者-mxwz-blue)](https://github.com/mxwz)

</div>

## 🤝 介绍

占卜起卦插件，支持塔罗牌、小六壬、梅花易数等多种占卜方式。

## 📦 安装

- 可以直接在astrbot的插件市场搜索`astrbot_plugin_zhanbu`，点击安装，耐心等待安装完成即可
- 也可以手动安装：[astrbot_plugin_zhanbu](https://github.com/mxwz/astrbot_plugin_zhanbu)
- 若是安装失败，可以尝试直接克隆源码：

```
bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/mxwz/astrbot_plugin_zhanbu

# 控制台重启AstrBot
```
## ⌨️ 使用说明

### 塔罗牌占卜命令表

|     命令      |                    说明                    |
|:-------------:|:------------------------------------------:|
| /塔罗牌 塔罗牌阵 [牌阵类型] | 随机选取牌阵进行占卜 |
| /塔罗牌 抽卡              | 得到单张塔罗牌回应 |
| /塔罗牌 查看牌阵           | 查看所有适配的塔罗牌阵型 |

### 小六壬占卜命令表

|     命令      |                    说明                    |
|:-------------:|:------------------------------------------:|
| /小六壬 时辰 [简短/详细] [问题] | 时辰排盘 |
| /小六壬 随机 [时辰] [简短/详细] [问题] | 随机抽取数字排盘 |
| /小六壬 数字 [数字1,数字2,数字3] [时辰] [简短/详细] [问题] | 数字排盘 |
| /小六壬 八卦 [卦名] | 查询八卦内容 |

### 梅花易数占卜命令表

|     命令      |                    说明                    |
|:-------------:|:------------------------------------------:|
| /梅花易数 时间 [问题] [性别] | 以当前农历时间起数 |
| /梅花易数 笔画 [问题] [性别] [汉字1,汉字2,...] [时辰] | 笔画起数（2-6个汉字） |
| /梅花易数 随机 [问题] [性别] [数字2-6] [时辰] | 随机数字起数 |
| /梅花易数 数字 [问题] [性别] [数字1,数字2,...] [时辰] | 自定义数字起数（2-6个数字） |
| /梅花易数 三数 [问题] [性别] [数字1,数字2,数字3] [是/否] [时辰] | 三数起数 |
| /梅花易数 64卦 [卦名] [爻位1-6] | 查看64卦象和对应爻辞 |

## ⚙️ 配置

进入插件配置面板进行配置：

- `enable_sent_picture`: 是否启用发送图片（塔罗牌图片），默认为 `false`
- `enable_repost`: ~~是否启用转发功能，默认为~~ `false` (未支持)

## 📌 注意事项

- 塔罗牌功能需要相应的图片资源文件放在 `resource` 文件夹中
- 插件需要 Python 3.10 或更高版本
- 部分功能可能需要联网获取农历时间等信息

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码
