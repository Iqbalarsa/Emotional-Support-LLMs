# Emotional Support LLMs: Improving Spanish and Indonesian Cultural Sensitivity

This repository contains the data and source code for the Final Project of the Natural Language Processing for Social Good course at Leiden University. This project extends the *CultureCare* framework to explore and enhance culturally sensitive emotional support generation, specifically tailored for Spanish- and Indonesian-speaking online forums.

## Repository Structure

The repository is organized into three main directories:

### 1. `Data Collection/`
This folder contains scripts for raw data scraping and automated filtering from Reddit.
*   **Scraping:** Scripts to fetch data via the Reddit API from culture-specific subreddits (e.g., `r/indonesia`, `r/Espana`) and mental health subreddits using translated keywords.
*   **LLM Filtering:** Scripts utilizing the `Qwen2.5-7B-Instruct` model to automatically filter thousands of raw posts. The filter ensures the selected candidate posts contain both explicit cultural signals and personal emotional distress messages.

### 2. `Dataset/`
This folder contains the human-annotated dataset used for our experiments.
*   Comprises 40 high-quality post-response pairs (20 from the Spanish cultural context and 20 from the Indonesian cultural context).
*   The data features fine-grained annotations by in-culture annotators, including labels for: emotional distress messages and their intensity, cultural signals and their categories, and emotional support strategies.
*   The dataset is stored in `JSONL` format to facilitate seamless integration as Large Language Model (LLM) inputs.

### 3. `Model/`
This folder includes the full NLP pipeline implementation in Python, from text generation to automatic evaluation.
*   **Response Generation:** Scripts to run the **Cohere Aya-Expanse-8B** model for generating peer-support responses. This module implements 5 cultural adaptation prompting strategies: 
    *   `redditor` (Baseline)
    *   `profile` (Culture-informed role-play / `+culture`)
    *   `guided_without_profile` (Cross-cultural guidelines / `+guided`)
    *   `annotation_without_profile` (Explicit data annotations / `+annotation`)
    *   `guided_annotation` (Combined strategy / `+cga`)
*   **Automatic Evaluation (G-Eval):** Scripts to execute the *LLM-as-a-Judge* evaluation using the **GPT-o3-mini** model (via OpenAI API). The evaluator uses step-by-step rubric-based prompts to score the generated responses on a 1-5 Likert scale. Evaluated metrics include:
    *   *Emotional Supportiveness* (Empathy, Helpfulness)
    *   *Cultural Awareness* (Socio-political influence, Knowledge, Cultural context)
    *   *Language Quality* (Fluency, Communication)

## System Requirements
The code in this repository was developed and executed in a Google Colab Pro environment equipped with an NVIDIA A100 (80GB) GPU. To run the scripts in the `Model` folder, please ensure the following libraries are installed:
*   `transformers`
*   `torch`
*   `openai`
*   `pandas`
*   `tqdm`

## Team Members
*   Jesus Elenes
*   Santiago Moreno Mercado
*   Muhamad Iqbal Arsa
*   Maftukhatul Qomariyah Virati

*(This project references and builds upon the methodology introduced in the "CultureCare" study by Liu et al., 2026.*
