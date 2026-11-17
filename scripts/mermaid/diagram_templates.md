# 轻量级科研流程图 Mermaid 模板库 (Mermaid Diagram Templates)

本模板专为科研草稿、GitHub 文档、Notion 知识库与学术论文 Supplementary Information 设计。支持快速渲染，语法简明，原生兼容 Markdown 预览环境。

---

## 模板 1：临床实验与样本处理标准流水线 (Linear Protocol)

适用于技术路线总览、队列入组与样本处理流：

```mermaid
flowchart LR
    %% 节点定义
    A["Patient Cohort<br/>(n = 120 Subjects)"] --> B["Peripheral Blood<br/>PBMC Isolation"]
    B --> C{"Quality Control<br/>Viability > 90%?"}
    
    C -- Yes --> D["Single-Cell RNA-seq<br/>(10x Genomics 3')"]
    C -- No --> E["Sample Excluded<br/>(Re-isolation)"]
    
    D --> F["Cell Clustering<br/>& Marker Annotation"]
    F --> G["Mechanistic Validation<br/>(In Vitro Assay)"]

    %% 顶刊低饱和样式配色
    style A fill:#F8F9FA,stroke:#4E79A7,stroke-width:1.5px,color:#262626
    style B fill:#F8F9FA,stroke:#4E79A7,stroke-width:1.5px,color:#262626
    style C fill:#FFF3CD,stroke:#F28E2B,stroke-width:1.5px,color:#262626
    style D fill:#E8F4F8,stroke:#76B7B2,stroke-width:1.5px,color:#262626
    style E fill:#F8D7DA,stroke:#E15759,stroke-width:1.5px,color:#721C24
    style F fill:#E8F4F8,stroke:#76B7B2,stroke-width:1.5px,color:#262626
    style G fill:#FDE8E8,stroke:#E15759,stroke-width:2px,color:#262626
```

---

## 模板 2：生物信息学与多组学数据分析管线 (Bioinformatics Pipeline)

适用于生信算法、转录组/突变检测与功能注释分析：

```mermaid
flowchart TD
    subgraph RawData ["阶段 1: 原始数据获取与质控"]
        R1["Raw FASTQ Reads"] --> QC["FastQC & Trimming<br/>(fastp)"]
    end

    subgraph Align ["阶段 2: 比对与定量"]
        QC --> AL["Genome Alignment<br/>(STAR / HISAT2)"]
        AL --> CNT["Read Quantification<br/>(featureCounts / Salmon)"]
    end

    subgraph DiffAnalysis ["阶段 3: 差异与功能挖掘"]
        CNT --> DEG["Differential Expression<br/>(DESeq2 / edgeR)"]
        DEG --> ENR["Functional Enrichment<br/>(GO / KEGG / GSEA)"]
        DEG --> NET["Protein-Protein Interaction<br/>(STRING Network)"]
    end

    subgraph KeyOutput ["阶段 4: 关键候选靶标"]
        ENR --> LEAD["Lead Therapeutic Candidates<br/>(Core Hub Genes)"]
        NET --> LEAD
    end

    style RawData fill:#F8F9FA,stroke:#CED4DA,stroke-width:1px
    style Align fill:#F8F9FA,stroke:#CED4DA,stroke-width:1px
    style DiffAnalysis fill:#F8F9FA,stroke:#CED4DA,stroke-width:1px
    style KeyOutput fill:#FEF2F2,stroke:#FCA5A5,stroke-width:1px
    style LEAD fill:#EF4444,stroke:#B91C1C,stroke-width:1.5px,color:#FFFFFF
```

---

## 模板 3：临床研究入组与筛选流程图 (CONSORT Flowchart)

医学顶刊（Lancet, NEJM, JAMA）投稿必备的标准受试者纳入/排除流：

```mermaid
flowchart TD
    S["Assessed for Eligibility<br/>(n = 640)"]
    
    EX1["Excluded (n = 210)<br/>- Not meeting inclusion criteria (n = 145)<br/>- Declined to participate (n = 45)<br/>- Other reasons (n = 20)"]
    
    R["Randomized<br/>(n = 430)"]
    
    A1["Allocated to Treatment Arm A<br/>Standard of Care + Drug (n = 215)"]
    A2["Allocated to Control Arm B<br/>Standard of Care + Placebo (n = 215)"]
    
    L1["Lost to follow-up (n = 8)<br/>Discontinued intervention (n = 7)"]
    L2["Lost to follow-up (n = 5)<br/>Discontinued intervention (n = 9)"]
    
    F1["Analyzed for Primary Outcome<br/>(n = 200)"]
    F2["Analyzed for Primary Outcome<br/>(n = 201)"]
    
    S --> EX1
    S --> R
    R --> A1
    R --> A2
    A1 --> L1 --> F1
    A2 --> L2 --> F2

    style S fill:#F8F9FA,stroke:#4E79A7,stroke-width:1.5px
    style R fill:#E0F2FE,stroke:#0284C7,stroke-width:1.5px
    style EX1 fill:#FEE2E2,stroke:#EF4444,stroke-width:1px
    style F1 fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px
    style F2 fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px
```

---

## 模板 4：前馈与负反馈调控机制回路 (Feedback Signaling Loop)

适用于展示生物网络中的自抑制环路与稳态调节：

```mermaid
flowchart LR
    Stimulus["External Stress / Ligand"] --> |Activation| Receptor["Receptor Tyrosine Kinase"]
    Receptor --> |Phosphorylation| Kinase["MAPK Cascade<br/>(ERK1/2)"]
    Kinase --> |Nuclear Translocation| TF["Transcription Factor<br/>(p-STAT3)"]
    
    TF --> |Gene Induction| Target["Target Gene Expression<br/>(Proliferation & Survival)"]
    TF --> |Induction| Phosphatase["Dual-Specificity Phosphatase<br/>(DUSP6)"]
    
    Phosphatase -.-> |Negative Feedback Inactivation| Kinase

    style Stimulus fill:#FEF3C7,stroke:#D97706,stroke-width:1px
    style Receptor fill:#E0E7FF,stroke:#4338CA,stroke-width:1.5px
    style Kinase fill:#FDE8E8,stroke:#E15759,stroke-width:1.5px
    style TF fill:#DC2626,stroke:#991B1B,stroke-width:2px,color:#FFFFFF
    style Phosphatase fill:#E5E7EB,stroke:#4B5563,stroke-width:1px,stroke-dasharray: 5 5
    style Target fill:#D1FAE5,stroke:#059669,stroke-width:1.5px
```
