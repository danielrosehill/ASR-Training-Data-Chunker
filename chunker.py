#!/usr/bin/env python3
"""
ASR Training Data Chunker

This script takes a source text file and chunks it into smaller files based on
the user's speaking speed (WPM) and desired chunk duration.
"""

import os
import re
import math
import argparse
import datetime

def count_words(text):
    """Count the number of words in a text."""
    return len(re.findall(r'\b\w+\b', text))

def find_sentence_breaks(text):
    """Find all sentence break positions in the text."""
    # Look for periods, question marks, or exclamation marks followed by a space or newline
    sentence_breaks = [m.end() for m in re.finditer(r'[.!?][\s\n]', text)]
    
    # Add the end of the text as a break point
    if sentence_breaks and sentence_breaks[-1] != len(text):
        sentence_breaks.append(len(text))
    elif not sentence_breaks:
        sentence_breaks.append(len(text))
        
    return sentence_breaks

def chunk_text(text, wpm, chunk_duration_minutes):
    """
    Chunk the text based on speaking speed and desired chunk duration.
    
    Args:
        text (str): The source text to chunk
        wpm (int): Words per minute speaking speed
        chunk_duration_minutes (float): Desired duration of each chunk in minutes
        
    Returns:
        list: List of text chunks
    """
    # Calculate target words per chunk
    target_words_per_chunk = int(wpm * chunk_duration_minutes)
    
    # Find all sentence breaks
    sentence_breaks = find_sentence_breaks(text)
    
    chunks = []
    start_pos = 0
    current_word_count = 0
    
    # Process the text character by character
    for i, char in enumerate(text):
        # If we encounter a word boundary (space or newline after a word)
        if i > 0 and char in [' ', '\n'] and text[i-1] not in [' ', '\n']:
            current_word_count += 1
            
        # If we've reached a sentence break and have enough words for a chunk
        if i in sentence_breaks and current_word_count >= target_words_per_chunk:
            # Add the chunk from start position to this sentence break
            chunk = text[start_pos:i+1].strip()
            chunks.append(chunk)
            
            # Reset for next chunk
            start_pos = i + 1
            current_word_count = 0
    
    # Add any remaining text as the final chunk
    if start_pos < len(text):
        final_chunk = text[start_pos:].strip()
        if final_chunk:
            chunks.append(final_chunk)
    
    return chunks

def save_chunks(chunks, output_dir):
    """Save chunks to individual files."""
    os.makedirs(output_dir, exist_ok=True)
    
    for i, chunk in enumerate(chunks):
        chunk_file = os.path.join(output_dir, f"chunk{i+1}.txt")
        with open(chunk_file, 'w') as f:
            f.write(chunk)
        print(f"Saved {chunk_file} ({count_words(chunk)} words)")
    
    return len(chunks)

def save_chunking_notes(output_dir, wpm, chunk_duration, total_words, num_chunks, actual_duration, avg_chunk_duration):
    """Save chunking notes to a file."""
    notes_dir = os.path.join(os.path.dirname(output_dir), "notes")
    os.makedirs(notes_dir, exist_ok=True)
    
    notes_file = os.path.join(notes_dir, "chunking-notes.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(notes_file, 'w') as f:
        f.write("ASR Training Data Chunker - Run Summary\n")
        f.write("===================================\n\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Output directory: {output_dir}\n\n")
        f.write("Configuration:\n")
        f.write(f"- Speaking speed: {wpm} words per minute\n")
        f.write(f"- Desired chunk duration: {chunk_duration:.2f} minutes\n\n")
        f.write("Results:\n")
        f.write(f"- Total words processed: {total_words}\n")
        f.write(f"- Number of chunks created: {num_chunks}\n")
        f.write(f"- Estimated total reading time: {actual_duration:.2f} minutes\n")
        f.write(f"- Average chunk duration: {avg_chunk_duration:.2f} minutes\n")
    
    print(f"Chunking notes saved to {notes_file}")
    return notes_file

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Chunk text files for ASR training data')
    parser.add_argument('-s', '--source', help='Source text file path (default: chunker/source/source.txt)')
    parser.add_argument('-o', '--output-dir', help='Output directory (default: auto-generated timestamped directory)')
    parser.add_argument('-w', '--wpm', type=int, help='Speaking speed in words per minute')
    parser.add_argument('-d', '--duration', type=float, help='Desired chunk duration in minutes')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()
    
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle source file
    if args.source:
        source_file = os.path.abspath(args.source)
    else:
        source_dir = os.path.join(script_dir, "chunker", "source")
        source_file = os.path.join(source_dir, "source.txt")
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"Error: Source file not found at {source_file}")
        return
    
    # Create timestamped output directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output_dir:
        base_output_dir = os.path.abspath(args.output_dir)
    else:
        base_output_dir = os.path.join(script_dir, "chunker", "output")
    
    output_dir = os.path.join(base_output_dir, timestamp)
    
    # Read the source text
    with open(source_file, 'r') as f:
        source_text = f.read()
    
    # Get user input or use command line arguments
    print("\nASR Training Data Chunker")
    print("========================\n")
    print(f"Source file: {source_file}")
    print(f"Total words: {count_words(source_text)}\n")
    
    try:
        if args.wpm:
            wpm = args.wpm
        else:
            wpm = int(input("Enter your speaking speed (words per minute): "))
        
        if wpm <= 0:
            raise ValueError("Speaking speed must be positive")
        
        if args.duration:
            chunk_duration = args.duration
        else:
            chunk_duration = float(input("Enter desired chunk duration (minutes): "))
        
        if chunk_duration <= 0:
            raise ValueError("Chunk duration must be positive")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Calculate and display estimated total duration
    total_words = count_words(source_text)
    estimated_total_duration = total_words / wpm
    estimated_chunks = math.ceil(estimated_total_duration / chunk_duration)
    
    print(f"\nEstimated total duration: {estimated_total_duration:.2f} minutes")
    print(f"Estimated number of chunks: {estimated_chunks}")
    print(f"Output directory: {output_dir}")
    
    # Confirm with user unless --yes flag is used
    if not args.yes:
        confirm = input("\nProceed with chunking? (y/n): ").lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return
    
    # Chunk the text and save
    print("\nChunking text...")
    chunks = chunk_text(source_text, wpm, chunk_duration)
    num_chunks = save_chunks(chunks, output_dir)
    
    # Calculate actual statistics
    total_chunk_words = sum(count_words(chunk) for chunk in chunks)
    actual_duration = total_chunk_words / wpm
    avg_chunk_duration = actual_duration / len(chunks) if chunks else 0
    
    # Save chunking notes
    notes_file = save_chunking_notes(
        output_dir, 
        wpm, 
        chunk_duration, 
        total_chunk_words, 
        num_chunks, 
        actual_duration, 
        avg_chunk_duration
    )
    
    # Print summary
    print("\nChunking complete!")
    print(f"Created {num_chunks} chunks in {output_dir}")
    print(f"Total words processed: {total_chunk_words}")
    print(f"Estimated total reading time: {actual_duration:.2f} minutes")
    print(f"Average chunk duration: {avg_chunk_duration:.2f} minutes")
    print(f"Chunking notes saved to {notes_file}")

if __name__ == "__main__":
    main()
