
# NekoSdk toolkit

## Overview

This repository contains scripts for extracting text script from nekosdk engine.

## Contents

- `neko_tool.py`: Script for extracting and recompile texts from nekoskd script bin file.
- `nekosdk_advscript2.py`: # This is edited from file generated by kaitai-struct-compiler.

## Requirements

- Python 3.x
- Required Python packages (can be installed via `requirements.txt`)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com:adsf0427/nekosdk_tools.git
   cd nekosdk_tools
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

This project provides scripts for extracting and recompiling text from a bin file. The main script accepts different commands to perform various operations.

### Commands

- `extract`: Extracts text from the bin file and generates JSON output.
- `recompile`: Recompiles the text from JSON into the bin file.
- `test`: Runs tests to verify the extraction and recompilation processes.

### Running the Script

To run the script, use the following command format:

```sh
python neko_tool <command>
```

Replace `<command>` with one of the available commands (`extract`, `recompile`, `test`).