# ASR-Training-Data-Chunker

A Python tool for chunking text files into smaller segments based on speaking speed and desired duration, optimized for ASR (Automatic Speech Recognition) training data preparation.

## Purpose

This tool helps you split large text files into smaller chunks that:
- Take a specific amount of time to read aloud based on your speaking speed
- Break at logical sentence boundaries to maintain context
- Can be used for recording voice samples for ASR training

## Installation

No installation required. Simply clone this repository:

```bash
git clone https://github.com/danielrosehill/ASR-Training-Data-Chunker.git
cd ASR-Training-Data-Chunker
```

## Usage

1. Place your source text file in the `chunker/source/` directory as `source.txt`
2. Run the chunker script:

```bash
python chunker.py
```

3. Follow the prompts to enter:
   - Your speaking speed in words per minute (WPM)
   - Desired chunk duration in minutes

4. The script will create chunked files in the `chunker/chunked/` directory

## Determining Your Speaking Speed

You can measure your speaking speed using online tools like:
- [Typing Master Speech Speed Test](https://www.typingmaster.com/speech-speed-test/#speechtest)

Average speaking speeds:
- Slow: ~120 WPM
- Average: ~150 WPM
- Fast: ~180+ WPM

## Example

For a text with 9000 words:
- Speaking speed: 150 WPM
- Desired chunk duration: 2 minutes

The script will create approximately 30 chunks, each containing around 300 words and taking about 2 minutes to read aloud.

## License

MIT