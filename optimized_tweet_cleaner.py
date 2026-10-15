import re
import time

def clean_tweets_file(input_file, output_file, custom_keywords):
    """
    Efficiently process a large file of tweets (500K+ lines) with no empty lines.
    Optimized for speed when working with large files.
    
    Args:
        input_file (str): Path to the input file containing tweets
        output_file (str): Path to write the cleaned tweets
        custom_keywords (list): Optional list of words to remove
    """
    # Set default for custom_keywords if None
    if custom_keywords is None:
        custom_keywords = []
    
    # Start timing for performance monitoring
    start_time = time.time()
    
    # Compile regex patterns once (major performance boost)
    rt_pattern = re.compile(r'^RT\s+')
    username_pattern = re.compile(r'@(\w+)')
    url_pattern = re.compile(r'http\S+|www\S+|https\S+')
    
    # Process the file in a single pass
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        # Count lines for reporting
        line_count = 0
        
        # Process each tweet
        for tweet in infile:
            # Clean the tweet
            
            # Remove RT at beginning
            tweet = rt_pattern.sub('', tweet)
            
            # Convert @username to username
            tweet = username_pattern.sub(r'\1', tweet)
            
            # Remove URLs
            tweet = url_pattern.sub('', tweet)
            
            # Remove non-ASCII characters (including emojis)
            tweet = ''.join(c for c in tweet if ord(c) < 128)
            
            # Remove custom keywords
            for keyword in custom_keywords:
                tweet = tweet.replace(keyword, '')
            
            # Remove extra whitespace
            tweet = ' '.join(tweet.split())
            
            # Write to output file
            outfile.write(tweet + '\n')
            
            # Increment counter
            line_count += 1
            
            # Optional progress reporting for large files
            if line_count % 50000 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {line_count} tweets in {elapsed:.2f} seconds")
    
    # Final timing report
    total_time = time.time() - start_time
    print(f"Completed processing {line_count} tweets in {total_time:.2f} seconds")
    print(f"Average speed: {line_count/total_time:.2f} tweets/second")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    # Configuration
    input_filepath = "FINAL LIWC/AU/CENTRAL/AUS_pruned_4comm_1000central_tweets.txt"  # Replace with your file path
    output_filepath = "FINAL LIWC/AU/CENTRAL/CLEANED/AUS_pruned_4comm_1000central_tweets.txt"  # Replace with your output path
    
    # Words to remove (add your custom words here)
    custom_keywords = ['coronavirus', 'Coronavirus','covid','CORONAVIRUS','COVID19','CORONA19','amp','nsw','covid19', 'covid-19','nhttps']
    
    # Process the file
    clean_tweets_file(input_filepath, output_filepath, custom_keywords)


