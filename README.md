# Miss Gracy Baby - YouTube Content Generation System

**Project Status:** Actively under development.

This repository contains a comprehensive suite of tools designed to automate and streamline the content creation process for the "Miss Gracy Baby" YouTube channel. The system leverages the Gemini AI to generate content ideas, video scripts, and metadata, all managed through a user-friendly graphical interface.

## Table of Contents

- [System Overview](#system-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Download](#download)
  - [Installation](#installation)
  - [Usage](#usage)
- [System Components](#system-components)
  - [Video Generator](#video-generator)
  - [Content Idea Generator](#content-idea-generator)
  - [Video Script Generator](#video-script-generator)
  - [Metadata Generator](#metadata-generator)
  - [Quality Control](#quality-control)
  - [Batch Processor](#batch-processor)
  - [Workflow Manager](#workflow-manager)
- [Content Blueprint](#content-blueprint)
- [Contributing](#contributing)
- [License](#license)

## System Overview

The Miss Gracy Baby content generation system is a Python-based application with a simple web interface that automates the entire YouTube video production pipeline. From ideation to a final, downloadable video, this system is designed to be a powerful assistant for content creators.

## Features

- **Graphical User Interface**: A user-friendly interface to control the content generation process.
- **Automated Video Creation**: Generates complete, downloadable `.mp4` video files.
- **Text-to-Speech Voiceover**: Automatically generates a voiceover from the script.
- **Content Idea Generation**: Automatically generate content ideas based on predefined content pillars and themes.
- **Video Script Generation**: Create detailed and engaging video scripts using the Gemini AI.
- **Metadata Generation**: Generate SEO-optimized titles, descriptions, and tags for YouTube videos.
- **Quality Control**: Ensure that all generated content adheres to a set of quality standards.
- **Workflow Management**: A centralized workflow manager to orchestrate the entire content creation process.

## Project Structure
```
/
├── .gitignore
├── gemini-config.json
├── gui.py
├── idea
├── install.sh
├── Miss Gracy Baby Content Blueprint.md
├── README.md
├── requirements.txt
├── start.sh
├── .git/
├── prompt-templates/
│   ├── content-pillar-templates.json
│   ├── quality-standards.json
│   └── video-structure-template.json
├── scripts/
│   ├── batch_processor.py
│   ├── content_idea_generator.py
│   ├── generate_video_script.py
│   ├── metadata_generator.py
│   ├── quality_control.py
│   ├── video_generator.py
│   ├── workflow_manager.py
│   └── __pycache__/
└── venv/
    ├── bin/
    ├── include/
    └── lib/
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Download

You can download the project from its GitHub repository.

1.  **Clone the Repository:**
    Open your terminal and run the following command:
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    ```
    Replace `your-username` and `your-repository-name` with the actual GitHub username and repository name.

2.  **Navigate to the Project Directory:**
    ```bash
    cd your-repository-name
    ```

### Installation

The installation process is automated with the `install.sh` script.

1.  **Make the Install Script Executable:**
    Open your terminal and run the following command once:
    ```bash
    chmod +x install.sh
    ```

2.  **Run the Install Script:**
    ```bash
    ./install.sh
    ```
    The script will automatically install all necessary libraries.

### Usage

1.  **Configure Your API Key:**
    Before you begin, you must add your Gemini API key to the `gemini-config.json` file:
    ```json
    {
      "api_key": "YOUR_GEMINI_API_KEY"
    }
    ```

2.  **Run the Application:**
    Execute the `gui.py` script:
    ```bash
    python3 gui.py
    ```

3.  **Use the GUI:**
    The application window will open, and you can use the buttons to generate content.

## System Components

### Video Generator

- **File:** `scripts/video_generator.py`
- **Purpose:**  The core of the video creation process. It generates a voiceover, fetches images, and assembles everything into a final `.mp4` video file.

### Content Idea Generator

- **File:** `scripts/content-idea-generator.py`
- **Purpose:** Generates content ideas based on the `content-pillar-templates.json` and the `Miss Gracy Baby Content Blueprint.md`.

### Video Script Generator

- **File:** `scripts/generate-video-script.py`
- **Purpose:** Uses the Gemini AI to generate a full video script.

### Metadata Generator

- **File:** `scripts/metadata-generator.py`
- **Purpose:** Creates SEO-friendly titles, descriptions, and tags.

### Quality Control

- **File:** `scripts/quality-control.py`
- **Purpose:**  Analyzes generated scripts against a set of predefined quality standards.

### Batch Processor

- **File:** `scripts/batch-processor.py`
- **Purpose:**  Handles the batch processing of content ideas and scripts.

### Workflow Manager

- **File:** `scripts/workflow-manager.py`
- **Purpose:** Orchestrates the entire content creation process.

## Content Blueprint

The `Miss Gracy Baby Content Blueprint.md` is the foundational document that guides the entire content strategy. It outlines the channel's content pillars, target audience, video structure, and more.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or suggestions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
