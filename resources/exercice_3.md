# REGESTA

# General overview

This proposal presents the development of an advanced data pipeline aimed at
automating the summarization and extraction of key information from archival
series of the Ancien Régime. The focus is on full-text, non-tabular documents
primarily composed in early modern Dutch and French. By employing
state-of-the-art HTR and NLP technologies, the pipeline seeks to convert
historically rich yet frequently inaccessible serial documents into structured,
contextualized, searchable data. The project adopts an iterative development
methodology, with distinct phases encompassing data selection and preparation,
pipeline construction, integration of human oversight, and advanced application
of LLMs. A pivotal aspect of this initiative is the involvement of human
archivists in a 'human-in-the-loop' framework [(Wu et al., 2022\)](https://www.zotero.org/google-docs/?8ISjbv),
ensuring quality assurance and data refinement.

Parallel efforts will focus on the creation of an annotated dataset tailored
for fine-tuning LLMs, which will subsequently be integrated into the pipeline
to enhance automated corrections and improve overall performance. Expert
citizen scientists will also participate in manual data correction processes.
The pipeline will output extracted entities (names, locations, dates), concise
summaries, classifications by form and topic, and contextual perspectives on
individual pieces and the overall series.These outputs will be systematically
linked to AGATHA, the Belgian State Archives’ search engine. 


# Overall Strategy

In order to achieve these ambitious – yet realistic – objectives while paying
close attention to the cost-efficiency of our method, we propose to adopt the
following strategy:

1. a market survey of state-of-the-art HTR, NLP tools (benchmark), 
    and multimodal Language Models 
    [(Gemma Team, 2025; Li et al., 2019; Radford et al., 2021; Tan & Bansal, 2019\)](https://www.zotero.org/google-docs/?4xqQYE), 
    based on the needs and capabilities of the Belgian State Archives;

2. the development of a cognitive architecture 
    [(Sumers et al., 2024\)](https://www.zotero.org/google-docs/?JPERiL) 
    [(Ridnik et al., 2024\)](https://www.zotero.org/google-docs/?gQzBIv) 
    (graph of semi-autonomous agents) capable of automatically extracting 
    information from the source documents. Depending on the technological 
    choices made in \[1\], the scope of this cognitive architecture might 
    involve: analysis of that transcription, contextualization of the 
    transcribed text against other sources from an evolving knowledge base, 
    and the production of machine processable meta-data & summaries that can 
    be ingested in search engines. This step will likely require fine-tuning 
    one or several specialized LLMs through to consistently yield quality 
    output.

3. an human assessment of the overall pipeline performance (end to end 
    \+ broken down at each step of the architecture pipelines). 
    Based on these human evaluations, a curated list of high quality samples 
    will be created. The purpose of this dataset of high quality examples is 
    twofold: 

      * a subset of it will serve as a ground truth benchmark against which 
          the performance of later enhancements to our architecture can be 
          measured. 
      * the rest of the dataset will be exploited to perform model finetuning[^1].

4. the integration of an intuitive evaluation tool to integrate human quality 
    control to the aforementioned cognitive architecture. This 
    “human-in-the-loop” approach will enable the refinement and improvement 
    of the whole chain, eventually providing even better quality results. 
    The results from this phase could – for instance – be integrated to the 
    overall architecture through “few shot prompting“, or lead to a further 
    round of reinforcement learning (RL) finetuning based on the human preferences 
    [(Brown et al., 2020; DeepSeek-AI et al., 2025; Madaan et al., n.d.; Shinn et al., n.d.)](https://www.zotero.org/google-docs/?eFXRiP).

# Project Breakdown

## Wp1: Setting the foundations

The goal of this work package is to establish a clear foundation for the rest
of the project by creating a clear map of the tasks that need to be completed
as part of the document processing workflows. And to define an agreed upon,
historically relevant set of documents that will be used as a baseline to
assess the overall workflow performance.

Examples of tasks that have already been identified are the following:

* Automated text transcription (HTR)  
* Document segmentation ( that is, split documents that are logically separated despite following one another on the register paper).  
* Named Entity Recognition (Automated Extraction of names, dates, and places from the original text).  
* Text summarization  
* Contextualization which we break down as follows:  
  * Retrieval (find similar documents)  
  * Topic modeling (semantic clustering of documents \+ emergence of the most prevalent terms to describe them).  
  * Contextualized text generation (might be the same as 'Text summarization', but not necessarily).  
* Interaction with AGATHA

*Benchmark AI tools*

To achieve the creation of sound and strong foundations for this project, the
researcher will consider both commercial and open-source AI tools for HTR and
NLP, including LLMs (Romein et al., 2025). In recent years, there has been a
significant proliferation of AI tools, platforms, and applications relevant to
document processing and data extraction. While some tools are specifically
tailored for historical documents and text, others show great promise in this
domain [(*Enterprise Document AI & OCR | Mistral AI*, n.d.)](https://www.zotero.org/google-docs/?8cTOPY). 
Given the rapid pace of these developments, it is essential to create a 
comprehensive overview of the available tools.

Building on existing literature (e.g., AlKendi, 2024), the benchmarking process
will evaluate tools based on several parameters, including performance,
user-friendliness, customizability (e.g., the investment required to train
models effectively), machine vision capabilities, installation time, processing
time, and environmental impact. Since this project aims to contribute to
cost-efficient archival accessibility, particular emphasis will be placed on
relative costs, recognizing the precarious financial situation of the Belgian
State Archives. 

The benchmarking will enable the selection of the most appropriate tools for
the pipeline, taking into account the financial and infrastructural context of
the State Archives.

*Create a dataset for testing*

The second part of this initial work package consists of the creation of an
agreed upon, historically relevant dataset of documents that will be used
throughout the project. A wealth of options exists for that purpose as numerous
archival series from the Ancien Régime remain largely unexplored or
uncatalogued. To enhance the relevance and impact of REGESTA, we will therefore
align with ongoing and future research and inventorying projects at the State
Archives (e.g., ACCESS, the Great Council of Mechelen project led by Dirk
Leyder) and leverage recently completed datasets (e.g., PARDONS). Furthermore,
we will solicit input from fellow archivists (including those in the provincial
State Archives) and archive users (who are reached via newsletters, our
website, and social media) through a simple online survey (Google Forms). This
approach ensures that REGESTA generates data pertinent to other projects and
valuable to users.

*Difficulty measuring*

To estimate the relevance of the considered series, they will be examined and
scored according to various parameters. We will develop a measurement table and
scoring system to determine the difficulty and feasibility for each series. The
following criteria will be considered: material condition (damaged or not?
already digitised? time investment for digitisation? possibility of
digitisation automation? filing? bound or loose?), layout (presence of
marginalia? draft version/'between the lines' \+ erasures etc.? mixed reading
order?), handwriting (type, number of hands), language variation (different
languages?), and period. The score will provide insight into the complexity of
an archival series and the feasibility of IDP. 

*Digitization*

Series that have already been digitised will be prioritised, but REGESTA will
also undertake additional digitisation. As digitisation can be time and
labour-intensive, we will be selective in this regard, guided by utility. To
limit the workload, only three small series of varying difficulty will be
digitised in their entirety; for other series, we will digitise only a
representative sample (e.g., 1 register) suitable as test material. Using the
Transkribus ScanTent and a suitable camera, additional scans can be made
efficiently (independently of the digitisation service's workload), which can
also be downloaded as autonomous files via the DocScan app.

### Deliverable

#### Historian

* A curated dataset of documents that are logically grouped and organised in a machine ready repository.  
* A thorough characterisation of the dataset.  
* A ranking scheme to assess the difficulty/urgency and relevance of IDP  
* A list of tasks, entities, and contextual information that are considered to be usually relevant.  
* (in conjunction with comp. scientist) A set of prompts to inject in the models to accomplish the desired outcomes.

#### Computer scientist

* A state of the art survey regarding the completion of the tasks that have been identified. This survey will comprise both commercial and non commercial tools. At the end of this survey, the CS will recommend the utilisation of one or several tools for the implementation of the architecture.  
* The definition of a provisional infrastructure to run the architecture.

## WP2: Initial prototype

*Drafting the architecture*  

The goal of this work package is to create a first "draft" version of the
toolchain. This version of the system is not meant to be 'perfect', highly
performant or even to be totally 'feature complete'. It should however sketch
the general behavior of the various agents and their orchestration. It should
be sufficient for one to get an idea of where the system is headed at.

*Dataset annotation*

Modern AI-based applications often require fine-tuning LLM as a critical step
for enhancing the system performance
[(*Continued Fine-Tuning of LLMs: A Technical Deep Dive*, n.d.)](https://www.zotero.org/google-docs/?JBNeC5).
processing of historical texts, specifically aimed at improving transcription
correction and summarization accuracy. This process necessitates a two-fold
approach: the creation of a high-quality, domain-specific annotated dataset and
the subsequent fine-tuning of a suitable LLM. The foundation of this
fine-tuning effort lies in a meticulously constructed annotated dataset. This
dataset will be derived by leveraging a subset of human-corrected data
generated by the main processing pipeline, significantly augmented by
incorporating existing high-quality datasets such as PARDONS and ACCESS
transcriptions. The annotation process will strategically focus on identifying
and rectifying specific error types prevalent in historical texts, including
common HTR inaccuracies, inconsistencies in summarization, and subtle
contextual nuances unique to archaic language. A crucial element of this phase
is the active involvement of archivists in the annotation process, ensuring the
development of a robust "gold standard" dataset that guarantees the highest
level of quality and accuracy for the historical content. This dataset will be
specifically tailored to historical Dutch and French, incorporating necessary
adaptations to accommodate archaic linguistic forms. The goal is to curate a
representative sample of approximately 10,000 items for detailed manual
annotation, encompassing transcriptions, summaries, and relevant classification
labels.

*Fine-tuning LLM*

Following the dataset preparation, the subsequent step involves selecting and
fine-tuning an appropriate LLM. The selection will prioritize pre-trained,
preferably smaller open-source models like Llama 3 [(Dubey et al.,
2024\)](https://www.zotero.org/google-docs/?OH66t3), Mistral [(Jiang et al.,
2023, 2024\)](https://www.zotero.org/google-docs/?D0ycOJ), BLOOM, Gemma [(Gemma
Team, 2025\)](https://www.zotero.org/google-docs/?Eb7y8b), Qwen [(Bai et al.,
2023\)](https://www.zotero.org/google-docs/?Buco58) or DeepSeek R1
[(DeepSeek-AI et al., 2025\)](https://www.zotero.org/google-docs/?HrqYJU) that
demonstrate proficiency in handling both Dutch and French. While commercial API
options may be considered contingent on budgetary constraints, the primary
focus remains on open-source solutions to ensure flexibility and control. The
chosen LLM will undergo fine-tuning using the newly created annotated dataset.
Advanced techniques such as LoRA (Low-Rank Adaptation) or QLoRA will be
employed to effectively adapt the model's inherent linguistic capabilities to
the specific nuances of historical archival language and the designated
correction tasks. This targeted fine-tuning is essential for enabling the LLM
to accurately understand and process archaic language. The fine-tuned LLM will
then be seamlessly integrated into the existing processing pipeline,
functioning as a dedicated service. Its primary function will be to provide
post-hoc assistance in correcting HTR errors and refining NLP outputs. This
encompasses enhancing the coherence and accuracy of generated summaries,
validating the extraction of named entities, contributing to general error
correction, and ensuring consistency across metadata. Ultimately, the LLM will
serve as a powerful tool capable of reranking or correcting outputs from the
initial HTR and NLP stages, thereby substantially improving the overall quality
and reliability of the historical text processing workflow.

### Deliverables

#### Computer Scientist

Overall structure of the cognitive architecture and orchestration. The role of
the CS is to collaborate with the historian to establish and implement the
infrastructure and the major steps of the cognitive architecture. CS will also
be in charge of establishing a protocol shared amongst the various agents for
when the steps required the creation of structured output.

If time allows, the CS will also perform a first fine tuning of the model.

#### Historian

In parallel with the implementation work by the CS, the historian will refine a
set of prompts to instruct agents into doing the expected task. He will also
contribute in the form of the creation of a curated set of annotated data.

## WP3: Error analysis

The third wp, is one that will be highly demanding in terms of human brain
power. The goal of this wp will be to go over the results (global and stepwise)
of the prototype architecture using the dataset that has been created during
wp1. During this step, humans will work together to identify the cases where
the system gave wrong/unsatisfactory results and to understand why those
results are subpar.

### Deliverables

An extensive error analysis of the system. To complete this analysis, the
historian will craft a set of high quality representative examples of the
expected inputs and outputs at each step of the workflow. This dataset should
embody the business knowledge of an historian, as well as it should account for
the linguistic subtlety that are observed in those ancient documents.

In this context, the role of the CS would be to: 1\) guide the historian
through the process of an in depth error analysis (which he/she might not be
familiar with). Understand the findings of the historian and propose mitigation
approaches: e.g. definition of extra steps, creation of new agents, training of
fine tuned models (QLoRA adapters for extra cost efficiency), few shots
prompting and so on...

## WP4: Refinement

The goal of this wp would be to significantly enhance the performance of the
system by implementing the mitigation methods proposed in WP3. In addition to
those improvements, the final missing features will be implemented in the
system (e.g. connection with AGATHA).

### Deliverables

A working prototype whose behavior should be more closely aligned with the
desired outcome.

As both parties will have been learning from interacting with one another
throughout the WP1-3, it is expected that CS and Hist be able to share the
burden of finalizing this refined version of the prototype. For instance, Hist
could focus on polishing the prompts & measuring the impact of changes brought
at that level while CS prepares the scripts to conduct finetuning.

## WP5: Final touch

The goal of this fifth and final WP would be to further enhance the behavior of
the system by letting it incorporate the actual preferences of its intended
users. For that purpose, the CS would implement a mechanism to let users
express their preferences (e.g. presentation of two alternative outputs
combined with "like"/"dont like" buttons that help track and record users
preferences). The historian would gather a group of expert users who would be
able to express informed preferences about the behavior of the system.

### Deliverable

An improved system adopting the human in the loop paradigm.

* An UX/usability study about the system in its current version.  
* A series of propositions to further improve the system based on user feedback
(with possibly scripts to conduct reinforcement learning finetuning of some
agents to better align with the users expectations).  
* An a posteriori user study to measure the degree of improvements brought by
those latest changes.  
* A finalized version of the prototype is deployed in production.

1. *Tool benchmarking*

The initial step involves benchmarking both commercial and open-source AI tools
for HTR and NLP, including LLMs (Romein et al., 2025). In recent years, there
has been a significant proliferation of AI tools, platforms, and applications
relevant to document processing and data extraction. While some tools are
specifically tailored for historical documents and text, others show great
promise in this domain 
[(*Enterprise Document AI & OCR | Mistral AI*, n.d.)](https://www.zotero.org/google-docs/?nuXphw).
Given the rapid pace of these developments, it is essential to create a 
comprehensive overview of the available tools.

Building on existing literature (e.g., AlKendi, 2024), the benchmarking process
will evaluate tools based on several parameters, including performance,
user-friendliness, customizability (e.g., the investment required to train
models effectively), machine vision capabilities, installation time, processing
time, and environmental impact. Since this project aims to contribute to
cost-efficient archival accessibility, particular emphasis will be placed on
relative costs, recognizing the precarious financial situation of the Belgian
State Archives. 

The benchmarking will enable the selection of the most appropriate tools for
the pipeline, taking into account the financial and infrastructural context of
the State Archives.

2. *Sample selection*

The second step involves identifying suitable test sets. A wealth of options
exists, as numerous archival series from the Ancien Régime remain largely
unexplored or uncatalogued. To enhance the relevance and impact of REGESTA, we
will therefore align with ongoing and future research and inventorying projects
at the State Archives (e.g., ACCESS, the Great Council of Mechelen project led
by Dirk Leyder) and leverage recently completed datasets (e.g., PARDONS).
Furthermore, we will solicit input from fellow archivists (including those in
the provincial State Archives) and archive users (who are reached via
newsletters, our website, and social media) through a simple online survey
(Google Forms). This approach ensures that REGESTA generates data pertinent to
other projects and valuable to users.

We will commence with relatively straightforward sets before progressively
processing more complex series. To estimate the degree of difficulty, suggested
series will be examined and scored according to various parameters \[cf. also
Claude's text on selection\]. We will develop a measurement table and scoring
system to determine the difficulty and feasibility of IDP for each series. The
following criteria will be considered: material condition (damaged or not?
already digitised? time investment for digitisation? possibility of
digitisation automation? filing? bound or loose?), layout (presence of
marginalia? draft version/'between the lines' \+ erasures etc.? mixed reading
order?), handwriting (type, number of hands), language variation (different
languages?), and period. The score will provide insight into the complexity of
an archival series and the feasibility of IDP. The series suggested by
stakeholders in WP2 will now be visually examined and scored. The scores of the
examined sets will be plotted in a graph, and we will divide the sets into x
clusters: categories 1-x.

Series that have already been digitised will be prioritised, but REGESTA will
also undertake additional digitisation. As digitisation can be time and
labour-intensive, we will be selective in this regard, guided by utility. To
limit the workload, only three small series of varying difficulty will be
digitised in their entirety; for other series, we will digitise only a
representative sample (e.g., 1 register) suitable as test material. Using the
Transkribus ScanTent and a suitable camera, additional scans can be made
efficiently (independently of the digitisation service's workload), which can
also be downloaded as autonomous files via the DocScan app. 

3. *Building an historical LLM*

Fine-tuning a LLM is a critical step for enhancing the processing of historical
texts, specifically aimed at improving transcription correction and
summarization accuracy. This process necessitates a two-fold approach: the
creation of a high-quality, domain-specific annotated dataset and the
subsequent fine-tuning of a suitable LLM. The foundation of this fine-tuning
effort lies in a meticulously constructed annotated dataset. This dataset will
be derived by leveraging a subset of human-corrected data generated by the main
processing pipeline, significantly augmented by incorporating existing
high-quality datasets such as PARDONS and ACCESS transcriptions. The annotation
process will strategically focus on identifying and rectifying specific error
types prevalent in historical texts, including common HTR inaccuracies,
inconsistencies in summarization, and subtle contextual nuances unique to
archaic language. A crucial element of this phase is the active involvement of
archivists in the annotation process, ensuring the development of a robust
"gold standard" dataset that guarantees the highest level of quality and
accuracy for the historical content. This dataset will be specifically tailored
to historical Dutch and French, incorporating necessary adaptations to
accommodate archaic linguistic forms. The goal is to curate a representative
sample of approximately 10,000 items for detailed manual annotation,
encompassing transcriptions, summaries, and relevant classification labels.

Following the dataset preparation, the subsequent step involves selecting and
fine-tuning an appropriate LLM. The selection will prioritize pre-trained,
preferably smaller open-source models like Llama 3 [(Dubey et al.,
2024\)](https://www.zotero.org/google-docs/?OknS37), Mistral [(Jiang et al.,
2023, 2024\)](https://www.zotero.org/google-docs/?cycyWV), BLOOM, Gemma [(Gemma
Team, 2025\)](https://www.zotero.org/google-docs/?fUhsQO), Qwen [(Bai et al.,
2023\)](https://www.zotero.org/google-docs/?mRj1DZ) or DeepSeek R1
[(DeepSeek-AI et al., 2025\)](https://www.zotero.org/google-docs/?EOWpWG) that
demonstrate proficiency in handling both Dutch and French. While commercial API
options may be considered contingent on budgetary constraints, the primary
focus remains on open-source solutions to ensure flexibility and control. The
chosen LLM will undergo fine-tuning using the newly created annotated dataset.
Advanced techniques such as LoRA (Low-Rank Adaptation) or QLoRA will be
employed to effectively adapt the model's inherent linguistic capabilities to
the specific nuances of historical archival language and the designated
correction tasks. This targeted fine-tuning is essential for enabling the LLM
to accurately understand and process archaic language. The fine-tuned LLM will
then be seamlessly integrated into the existing processing pipeline,
functioning as a dedicated service. Its primary function will be to provide
post-hoc assistance in correcting HTR errors and refining NLP outputs. This
encompasses enhancing the coherence and accuracy of generated summaries,
validating the extraction of named entities, contributing to general error
correction, and ensuring consistency across metadata. Ultimately, the LLM will
serve as a powerful tool capable of reranking or correcting outputs from the
initial HTR and NLP stages, thereby substantially improving the overall quality
and reliability of the historical text processing workflow.

4. *HITL and data control*

Ensuring the quality of the processed historical texts requires a robust
validation process that combines automated methods with essential human
expertise. This will be achieved through the implementation of a
Human-in-the-Loop (HITL) validation framework [(Wu et al.,
2022\)](https://www.zotero.org/google-docs/?Lul30C), supported by an intuitive
interface and integrated with the fine-tuned LLM.

A key component of this framework is the design and development of a web-based
interface specifically for archivists and expert citizen scientists. This
interface will serve as the primary tool for data quality assurance, allowing
archivists to efficiently review, correct, and validate the outputs generated
by the HTR and NLP components of the pipeline. The interface will provide a
side-by-side view of the original document images and their corresponding HTR
transcriptions, enabling easy comparison and identification of errors.
Archivists will be equipped with an intuitive text editor to correct HTR
inaccuracies directly. Furthermore, the interface will facilitate the
validation or modification of extracted entities (NER), the review and
refinement of generated summaries to ensure accuracy and coherence, and the
confirmation or correction of document classifications. The interface will also
include functionality to flag particularly challenging documents or sections
for further review by subject matter experts, ensuring that complex cases
receive appropriate attention. The workflow within the interface will support
the flagging of uncertain entries, enable batch review for efficiency, and
maintain a comprehensive history of all corrections made, providing
transparency and traceability.

The data corrected and validated by archivists through this interface will be
strategically fed back into the system. This feedback loop is crucial for
implementing an active learning paradigm, where the models incrementally learn
from human corrections. This continuous learning process will lead to a
progressive improvement in the performance of both the HTR and NLP models over
time, adapting them more effectively to the specific characteristics and
challenges of the historical documents being processed.

The fine-tuned LLM will play a significant role in augmenting the correction
process. It will be applied post-HTR to automatically suggest corrections for
transcription outputs identified as having low confidence scores or exhibiting
common error patterns. For summary refinement, the LLM will be utilized to
enhance the coherence, conciseness, and factual accuracy of the generated
summaries, potentially exploring more abstractive summarization techniques
where appropriate. In terms of entity validation and expansion, the LLM will be
employed to cross-reference extracted entities with contextual information
within the text, helping to reduce the incidence of false positives and
suggesting related entities that might have been missed by the initial NER
process. This integrated approach, combining the strengths of automated
processing with expert human review and LLM-driven assistance, is designed to
ensure the highest possible quality and reliability of the final processed
historical data.

**Building the pipeline**

Building upon the foundational methodologies for HTR, layout analysis, and
sophisticated text segmentation, the next critical phase involves the setup and
rigorous testing of the complete data extraction pipeline. This pipeline is
designed to transform raw historical document images into structured,
searchable, and semantically enriched data. The core elements of this pipeline
are the sequential integration of text recognition (HTR), text segmentation,
and data extraction (NLP) components. The implementation strategy will involve
an iterative process, beginning with the independent testing and evaluation of
each tool and module to ensure optimal performance in isolation. Subsequently,
these components will be integrated onto a dedicated platform, allowing for
comprehensive end-to-end testing of the entire pipeline workflow. A commitment
to permanent evaluation and continuous data curation is central to this phase,
serving as a vital mechanism to guarantee the highest possible quality and
reliability of the processed data. Furthermore, the active and ongoing
involvement of archivists throughout the setup and testing process is not only
essential but paramount, leveraging their domain expertise to validate outputs,
refine processes, and ensure the pipeline meets the specific needs and
standards of archival research and access.

1. *HTR*

HTR, including sophisticated layout analysis, constitutes a vital component of
this project, serving as the initial step in transforming historical document
images into machine-readable text. The approach to implementing HTR involves
evaluating two primary options: integrating established commercial or
platform-based solutions via their APIs, or integrating open-source
alternatives. The first option entails leveraging platforms such as
Transkribus, e-Scriptorium, or Teklia. While these platforms typically incur
costs, utilizing their APIs can significantly reduce expenses, as observed with
Transkribus offering a 50% reduction when accessed programmatically. The State
Archives possess valuable prior experience with Transkribus, having already
developed specific layout and text recognition models tailored to historical
documents. However, the project remains open to exploring other established
solutions if they demonstrate the potential for better outcomes, considering
both performance and cost-effectiveness. Integration of such platforms would
necessitate the use of the project's own server infrastructure. The second
option involves integrating open-source solutions like Loghi or Kraken. The
primary advantage of this approach is the lower cost compared to commercial
platforms. Conversely, the main disadvantages lie in the increased programming
effort required for implementation and problem-solving, often without the
extensive community support and readily available public models that
characterize established platforms. The project will carefully assess both
integration strategies, weighing the benefits and drawbacks of each in terms of
accuracy, efficiency, cost, and the level of technical expertise required for
implementation and maintenance, ultimately selecting the approach that best
aligns with the project's goals and resources while building upon existing
institutional knowledge.

\[The output of this step : XML files\]

2. *Text segmentation*

A critical initial step in processing serial historical documents within a data
extraction pipeline, following the initial stages of HTR and layout analysis,
is the accurate segmentation of the continuous text output into distinct,
coherent items. These items could be individual letters, administrative acts,
diary entries, or other logical units depending on the nature of the serial
document. Accurate segmentation is paramount because subsequent NLP tasks, such
as summarization, entity extraction, and classification, are designed to
operate on these discrete document units, and incorrect segmentation can
significantly degrade the quality of downstream results. Several methodologies
can be employed for this text segmentation task, ranging from purely rule-based
approaches to more sophisticated hybrid methods incorporating machine learning.
The choice of methodology is largely dictated by the complexity and variability
of the structural markers that delineate item boundaries within the serial
documents. One fundamental methodology relies on a Rule-Based Approach, often
implemented using powerful pattern matching tools like regular expressions.
This method is particularly effective when the boundaries between documents are
marked by consistent and recognizable text patterns, such as recurring headers,
footers, specific keywords, or signature blocks that follow a relatively
uniform structure. As demonstrated in a previous code artifact, a Python script
can utilize a carefully crafted regular expression pattern
(document\_delimiter\_regex) to identify these markers within the concatenated
text output from the HTR stage. The script then splits the text based on these
identified patterns, saving each resulting segment as a separate file. The
strength of this approach lies in its simplicity, efficiency, and transparency
when patterns are clear. However, its limitation becomes apparent when boundary
markers exhibit significant variability in phrasing, spacing, or format that is
difficult to capture with a fixed set of rules. For documents where boundary
markers are recognizable but not always exactly the same, exhibiting variations
that challenge purely rigid rule-based systems, a Hybrid Rule-Based \+
ML-Driven Segmentation methodology offers a more robust solution. This approach
combines the precision of defined rules with the flexibility of machine
learning models to identify item boundaries. The Rule-Based Component still
plays a vital role by applying patterns (which can be more complex than simple
regular expressions) to propose candidate boundaries or identify strong
indicators. This provides an initial layer of detection and can handle
straightforward cases efficiently. The ML-Driven Component complements this by
training a machine learning model (such as a sequence labeling model) on an
annotated dataset where item boundaries have been manually marked. This model
learns to recognize more subtle or variable patterns and contextual cues
associated with boundaries, potentially incorporating features beyond just the
text itself, such as formatting or structural information derived from the
layout analysis. The combination can work by using rules to suggest candidates
that the ML model then verifies, or by using the ML model to predict boundaries
which are then validated or reinforced by rules. This hybrid approach requires
the creation of a high-quality annotated dataset for training but results in a
more adaptable system capable of handling the inherent variability often found
in historical serial documents, leading to more accurate and reliable
segmentation outcomes.

In summary, the selection of a text segmentation methodology depends on the
characteristics of the serial documents. Simple, consistent patterns can be
effectively handled with rule-based methods like regular expressions in a
Python script. However, for documents with variable or complex boundary
markers, a hybrid approach combining rule-based techniques with machine
learning provides the necessary flexibility and robustness to achieve accurate
segmentation, thereby ensuring the quality of data for subsequent NLP tasks in
the pipeline.

3. *Data extraction with NLP tools*

The third stage of the pipeline will focus on extracting meaningful information
from the transcribed texts, including generating summaries and identifying key
entities like actors, dates, and locations. 

For these tasks we will instrumentalize the fine-tuned LLM. 

3.1. Automatic text summarization (ATS)

Following the segmentation of documents, the pipeline will proceed to the
crucial step of text summarization, significantly enhanced by the capabilities
of a fine-tuned LLM. The project will explore and experiment with two primary
approaches to summarization: abstractive and generic. The methodology for this
stage will involve feeding the segmented document texts into the fine-tuned
LLM. For generic summarization, the LLM will be tasked with identifying and
extracting the most important sentences or phrases directly from the source
text to form a concise summary. This approach ensures factual accuracy by
sticking closely to the original wording. For abstractive summarization, the
LLM will generate entirely new sentences and phrases that capture the core
meaning of the document, potentially rephrasing and synthesizing information.
This method aims for greater fluency and conciseness but requires careful
evaluation to ensure fidelity to the original content. The project will conduct
experiments to determine which summarization approach, or perhaps a combination
thereof, yields the most useful and accurate summaries for historical
documents, taking into account the specific characteristics of the source
material and the needs of researchers. Evaluation metrics will likely include
ROUGE scores for assessing overlap with reference summaries and human
evaluation by archivists to judge coherence, relevance, and factual
correctness. The fine-tuned LLM's domain-specific knowledge, acquired during
its training on historical texts, is expected to significantly improve the
quality and relevance of the generated summaries compared to using a
general-purpose LLM.

3.2. Named-Entity Recognition (NER)

Subsequent to text summarization, the pipeline will extract core structured
data from the corrected transcriptions using NER tools. This phase is
specifically designed to identify and extract three key categories of
information: persons, placenames, and the date or period associated with the
document. No other entity types will be targeted at this stage.

The methodology for this NER component will leverage the capabilities of the
fine-tuned LLM, potentially in conjunction with specialized NER models trained
for historical languages. The input for this stage will be the high-quality,
corrected transcriptions that have passed through the HTR, text segmentation,
and initial LLM-driven correction and summarization phases. The NER models will
process these texts to pinpoint and classify the specified entities.

A significant challenge in this process is the inherent variability and archaic
nature of historical language, as well as potential ambiguities in entity
references. The fine-tuned LLM, with its domain-specific linguistic
understanding, will play a crucial role in enhancing the accuracy of entity
extraction. It can assist in resolving ambiguities, distinguishing between
similar-sounding entities, and potentially even inferring implicit dates or
periods based on contextual clues. For instance, the LLM can be employed to
cross-reference extracted entities with contextual information, thereby
reducing false positives and ensuring the precision of the extracted data.

The output of the NER process will be structured data, typically in formats
such as JSON or XML, where each extracted entity is clearly identified,
categorized (e.g., "PERSON," "PLACENAME," "DATE"), and linked back to its
original position in the text. Evaluation of the NER performance will be
rigorous, employing standard metrics such as Precision, Recall, and F1-score
against a gold-standard annotated dataset. Crucially, human validation by
archivists will be integrated into the process to ensure the factual
correctness and archival relevance of the extracted entities, providing
essential feedback for iterative model refinement and guaranteeing the utility
of the extracted core data for research and archival purposes.

3.3. Topic modelling / Document classification

The final stage in the data extraction pipeline involves the automated
classification of documents according to their typology. This process aims to
assign a predefined category (e.g., "letter," "decree," "inventory," "account
book entry") to each segmented document, thereby providing essential metadata
for organization, search, and analysis. While the goal is to automate this
classification as much as possible, a robust human-in-the-loop (HITL) mechanism
will be integrated to ensure accuracy and allow for expert intervention.

The methodology for automated document classification will primarily leverage
the fine-tuned LLM, which has been exposed to a wide range of historical
document characteristics during its training and fine-tuning phases. The LLM
will analyze the content, and potentially structural cues, of each segmented
document to predict its most probable typology. This will involve feeding the
cleaned and processed text of each document into the LLM, which will then
output a classification label from a predefined set of typologies relevant to
the archival collection. To enhance the accuracy of this automated process, the
LLM can be further fine-tuned on a specific dataset of historical documents
that have been manually classified by archivists, allowing it to learn the
subtle linguistic and structural features indicative of different document
types.

Despite the automation, manual correction via a human-in-the-loop approach is
critical. Archivists, with their deep domain knowledge and understanding of
historical document conventions, will review the automated classification
outputs. A dedicated interface, similar to the one used for HTR and NER
correction, will be provided, allowing archivists to:

* View the document text and its assigned typology.  
* Confirm the correctness of the automated classification.  
* Correct misclassified documents by selecting the appropriate typology from the predefined list.  
* Flag documents that are ambiguous or require further expert discussion for classification.

The data from these manual corrections will be fed back into the system in an
active learning loop. This continuous feedback mechanism will serve to
incrementally improve the LLM's classification performance, making it more
accurate and reliable over time. This iterative refinement, driven by expert
human input, is essential to achieve a high level of confidence in the
automated document typology classification, ultimately enhancing the
discoverability and usability of the digitized historical collection.

**Testing pipeline performance** 

Test three series

Upscale

**Data output and transfer**

Establish protocol to link data to AGATHA

**Training archivists**

[^1]:  For LLM, Embedding models, and Rerankers as needed.
