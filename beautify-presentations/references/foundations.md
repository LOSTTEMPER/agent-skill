# PPT 美化的设计基础

本文件用于解释方法、处理风格争议或判断“为什么这样设计”。实施具体风格时转读 `style-catalog.md`；执行验收时转读 `quality-gates.md`。

## 目录

1. 操作性定义
2. 三种演示模式
3. 六层设计结构
4. 历史谱系带来的原则
5. 认知与可读性证据
6. 常见伪规则与反证
7. 证据边界与来源

## 1. 操作性定义

### 1.1 美化

把美化定义为：

> 围绕观众、目标和播放场景，对叙事结构、信息层级、视觉系统、艺术方向、页面节奏和技术输出进行系统设计。

不要把美化等同于换主题、配色、字体、插画或动效。上述元素只有在共同服务一个认知目标时才构成设计。

### 1.2 设计感

把“有设计感”判断为以下关系是否有意、稳定、可解释：

- 先看什么，再看什么；
- 为什么这些元素对齐或分组；
- 哪些比例、间距和尺寸在全套重复；
- 哪些页面故意打破重复来制造转折；
- 字体、颜色、图像、图表和形状是否属于同一视觉语法；
- 风格是否适合观众需要做出的判断。

设计感来自控制，不来自元素数量。严格网格、巨大留白和受控拼贴都可以有设计感。

### 1.3 艺术性

把“有艺术性”判断为：形式是否在不破坏理解的前提下承载情绪、隐喻、尺度、冲突、节奏或作者立场。

可用手段包括：

- 构图的对称、非对称和张力；
- 图像视角、裁切、色调和材质；
- 字体性格、尺度反差和文字图像化；
- 留白、重复、突变和页面节奏；
- 与主题相关的视觉隐喻；
- 用连续动效表达关系变化。

随机装饰、无关图片、滤镜堆叠和每页都追求“炸裂”不构成艺术性。

### 1.4 风格

把风格定义为一套能跨页执行和验证的视觉语法，至少覆盖：

- 色板及语义职责；
- 拉丁与中文字体、fallback 和字号阶梯；
- 网格、边距、间距和信息密度；
- 图片题材、构图、裁切、调色和禁用项；
- 形状、描边、圆角、阴影、纹理和图标；
- 图表配色、标注、重点和来源；
- 封面、章节、内容、数据、引文、图片和结尾原型；
- 页面节奏和动效边界。

只给“高级感、科技感、艺术感”属于意图词，不是完整风格。

### 1.5 品质模型

使用乘法思维检查整体品质：

> PPT 品质 = 内容可信度 × 叙事连贯性 × 信息清晰度 × 风格一致性 × 场景适配度 × 技术可靠性

任何一项接近零，其他项很难补偿。它不是用于伪精确打分的数学公式，而是用于阻止“漂亮掩盖失败”的检查框架。

## 2. 三种演示模式

### 2.1 现场演讲 `live`

页面是演讲者的视觉搭档，而非完整文档。

- 让页面和口头叙述在时间上同步；
- 减少完整段落，保留主张、关键词、数字和术语；
- 使用更强的尺度变化和页面节奏；
- 将方法、来源和备查数据放进备注或附录；
- 按实际屏幕、最远观看距离、环境光和投影质量测试。

### 2.2 独立阅读 `reading`

页面离开演讲者后仍需成立。

- 保留上下文、定义、图注、来源、页码和导航；
- 允许更高密度，但必须强化分组、层级和阅读路径；
- 使用较稳定的页面原型与交叉引用；
- 避免照搬纸媒小字号与过窄多栏；
- 同时检查屏幕阅读和 PDF 导出。

### 2.3 混合交付 `hybrid`

主叙事服务现场，细节通过备注、附录或单独阅读版补足。

不要让每一页同时承担舞台海报与完整报告两种相反任务。必要时交付主 deck 与阅读附件。

## 3. 六层设计结构

按顺序工作；不要从第五层直接开始。

### 第一层：内容真实性与目标

- 确认观众、决策、时间、场景和成功标准；
- 核对事实、数字、单位、时间窗、口径和来源；
- 区分用户事实、外部材料、推理、假设与未知；
- 不用设计掩盖证据不足。

### 第二层：故事结构与页面任务

- 建立开场、问题、证据、转折、方案、行动的叙事弧；
- 为每页指定一个主要认知任务；
- 使用主张型标题，不只写主题标签；
- 拆分互相竞争的任务，合并无独立价值的碎片。

### 第三层：信息层级与网格

- 只保留一个第一视觉焦点；
- 使用尺度、位置、字重、颜色和留白建立层级；
- 让相关内容靠近，不相关内容分开；
- 使用对齐和共同区域，少用无意义边框；
- 先选择网格，再放置对象。

### 第四层：视觉系统

- 定义字体、颜色、网格、组件、图像和图表规则；
- 使用重复建立一致性；
- 用受控变化表达章节、转折和高潮；
- 让封面、正文、数据页和结尾属于同一系统。

### 第五层：艺术方向

- 选择主风格和必要的辅助风格；
- 让图像、纹理、裁切、材质、构图和动效承载意义；
- 把表现资源集中在关键 Hero 页，不让每页同时争夺注意力；
- 保持视觉表达与行业、语境和品牌承诺一致。

### 第六层：可访问性与输出可靠性

- 检查文字与关键图形对比度；
- 不只用颜色表达状态；
- 确保阅读顺序、替代文本和来源可用；
- 检查字体嵌入、比例、媒体、链接和导出；
- 渲染每页，修复溢出、重叠、裁切和替换字体。

## 4. 历史谱系带来的原则

以下历史不是风格贴纸，而是可执行方法的来源。

### 4.1 投影媒介：演示是一种时间艺术

PowerPoint 之前的魔术幻灯已经组合图像、讲述、声音和转场。由此得出：

- 一套演示必须设计时间顺序和节奏；
- 静态页面漂亮不代表现场叙事成立；
- 转场只在表达连续、因果或空间变化时使用。

### 4.2 Bauhaus：艺术与功能共存

Bauhaus 的重要遗产不是红黄蓝几何，而是：

- 把排版、图像、工业生产和功能放进同一方法；
- 使用非对称、标准化和清晰对比组织信息；
- 让基础形状承担结构、指引和强调。

### 4.3 瑞士国际主义：建立现代信息秩序

网格、无衬线字体、摄影、高对比和非对称构图形成了现代商务演示的基础语法。由此得出：

- 先建立结构，再引入变化；
- “极简”不是少放内容，而是消除无意的竞争；
- 严谨可以具有生命力，不等于机械居中。

### 4.4 企业识别：从单页变成系统

企业视觉识别把 Logo 扩展为跨出版物、环境和媒介的程序。由此得出：

- 一套 PPT 不是许多独立海报；
- 一致性来自规则，不只来自 Logo 和品牌色；
- 可复用页面原型比逐页手工修饰更可靠。

### 4.5 New Wave 与 Memphis：受控破坏也能成为规则

后现代设计通过倾斜、叠层、拼贴、艳色和文化符号反对僵硬秩序。由此得出：

- 艺术性可以来自打破网格；
- 破坏必须保持阅读路径与整体语法；
- 表达性越强，越要支付可读性和场景适配成本。

### 4.6 演示软件：默认模板具有历史偶然性

项目符号、幻灯片排序器和转场继承自实体媒介，不是自然法则。由此得出：

- 不因软件提供某种布局或效果就默认使用；
- 不把页面设计成演讲者提词器；
- 自动布局能修复表面秩序，不能保证内容真实、叙事有效或艺术方向成立。

## 5. 认知与可读性证据

### 5.1 相对稳健的原则

多媒体学习与视觉设计研究通常支持：

- 删除与任务无关的噪声；
- 用标题、重点和结构信号提示组织；
- 让相关文字和图像在空间上靠近；
- 减少同一时间互相竞争的视觉焦点；
- 使用接近性、共同区域和对齐表达分组；
- 让重点系列在图表中可直接识别；
- 通过真实目标设备和受众测试验证。

这些原则主要减少缺陷，不能自动产生优秀设计。

### 5.2 屏幕文字的边界

“屏幕文字和口头讲解重复会增加负担”在部分技术教学研究中成立，但另有课堂研究发现语音加文字可能帮助理解。不要写成“删除所有文字”的硬规则。

根据场景调节：

- 现场、熟悉主题、演讲者稳定：减少完整句；
- 噪声、非母语、无障碍、录播：保留更多关键词或字幕；
- 阅读型：保留完整上下文；
- 专业术语、数字、定义、决策条件：不要只靠口头表达。

### 5.3 美感的价值和风险

情绪化视觉可能提升愉悦、记忆或参与感，但无关装饰也可能造成干扰。美观还可能增加观众对图表的主观信任。

因此：

- 让情绪与主题有关；
- 把艺术表达集中到能够承载意义的位置；
- 页面越精美，越要复核数据真实性和视觉误导；
- 不把“看起来可信”当作“证据充分”。

## 6. 常见伪规则与反证

以下内容只能作为启发式，不能作为无条件硬标准：

- “每页只能有一个观点”；更准确的是一个主要认知任务或视觉焦点。
- “一页不超过六行、每行不超过六字”；密度取决于使用模式和内容。
- “任何 PPT 都必须极简”；独立阅读、技术评审和董事会材料需要更多上下文。
- “字体必须至少 30pt”；可读性取决于观看视角、字体、屏幕和环境。
- “所有文字都不能照读”；关键术语、数字、字幕和无障碍场景需要屏幕文字。
- “黑金就是高级”；高级感来自比例、材质、控制和一致性。
- “动画越流畅越专业”；无意义运动会分散注意力并增加播放风险。
- “有模板就能保持一致”；没有 Token、原型和 QA 的模板仍会失控。

## 7. 证据边界与来源

把下列内容视为【材料】，不是项目事实。检索时间以 2026-07-31 至 2026-08-01 为基准；使用时核对更新。

### 演示与软件历史

- Computer History Museum, [Slide Logic](https://computerhistory.org/blog/slide-logic-the-emergence-of-presentation-software-and-the-prehistory-of-powerpoint/)
- Robert Gaskins, [PowerPoint at 20](https://www.robertgaskins.com/powerpoint-history/documents/gaskins-powerpoint-at-20-cacm-vol50-no12-dec-2007-p15-p17.htm)
- Microsoft, [The evolution of PowerPoint: Designer and Morph](https://www.microsoft.com/en-us/microsoft-365/blog/2015/11/13/the-evolution-of-powerpoint-introducing-designer-and-morph/)
- Apple, [Apple Unveils Keynote](https://www.apple.com/newsroom/2003/01/07Apple-Unveils-Keynote/)

### 设计史

- Bauhaus Archive, [Bauhaus Typography](https://www.bauhaus.de/en/research/publications/bauhaus-typography/)
- Swiss National Library, [The International Style 1950–1970](https://www.nb.admin.ch/en/the-international-style-1950-1970)
- Cooper Hewitt, [A Harmony of Contrasts](https://www.cooperhewitt.org/2018/08/05/aharmonyofcontrasts/)
- Cooper Hewitt, [IBM Corporate Identity](https://www.cooperhewitt.org/2013/01/24/corporate-calico-angelo-testas-fabric-for-ibm/)
- Design Museum, [Memphis](https://designmuseum.org/memphis)
- V&A, [Art Deco Printmakers](https://www.vam.ac.uk/articles/art-deco-printmakers)

### 认知、视觉与演示

- Cambridge Handbook of Multimedia Learning, [Principles for Reducing Extraneous Processing](https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/C98AB3A6CE760DD63C048936EA0B3B44)
- Frontiers in Psychology, [PowerPoint Presentation Flaws and Failures](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2012.00230/full)
- Penn State, [Assertion–Evidence research](https://writing.engr.psu.edu/research.html)
- Liu et al., [Does the redundancy effect exist in electronic slideshow assisted lecturing?](https://www.sciencedirect.com/science/article/pii/S0360131515001153)
- NN/g, [Principles of Visual Design](https://media.nngroup.com/media/articles/attachments/Principles_Visual_Design-A4.pdf)

### 解释规则

- 博物馆、学术出版物与原始软件历史用于解释设计谱系，置信度较高。
- 教学实验主要适用于多媒体学习，迁移到商务演示时保持条件化表述。
- 厂商模板目录只能证明某种视觉语言存在，不能证明它提升业务效果。
- Behance 等作品集用于观察视觉语法，不作为有效性证据，也不直接复制其作品。
- 任何“某种风格普遍更高级或更有效”的说法都应标记为推理，并通过目标观众测试。
