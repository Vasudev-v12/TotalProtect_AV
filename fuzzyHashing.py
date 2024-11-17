from collections import defaultdict

ratio_taken = 0.45

def create_ngrams(data, n=3):
    ngrams = defaultdict(int)
    for i in range(len(data) - n + 1):
        ngram = data[i:i + n]
        ngrams[ngram] += 1
    return ngrams

def fuzzy_hash(data):
    ngrams = create_ngrams(data)
    hash_str = ','.join(f"{ngram}:{count}" for ngram, count in sorted(ngrams.items()))
    return hash_str

def compare_hashes(hash1, hash2):
    set1 = set(hash1.split(','))
    set2 = set(hash2.split(','))
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()
    
def scanFile(file_path):
    file1 = 'D:\\OS project\\malFiles\\pyMalV1.py'
    data1 = read_file(file1)
    data2 = read_file(file_path)

    hash1 = fuzzy_hash(data1)
    hash2 = fuzzy_hash(data2)

    print(f"Fuzzy Hash 1: {hash1}")
    print(f"Fuzzy Hash 2: {hash2}")

    similarity = compare_hashes(hash1, hash2)
    print(f"Similarity Score: {similarity:.2f}")
    if(similarity >= ratio_taken):
        print("The file "+file_path+" was identified as a malicious file")
    else:
        print("The file was not identified as a potential malware")

    

if __name__ == "__main__":
    
    file2 = 'D:\\OS project\\malFiles\\pyMalV2.py'
    scanFile(file2)
    
    
    

# with ssdeep library#
# pip install ssdeep

# import ssdeep

# def fuzzy_hash(data):
#     """Generate a fuzzy hash for the given data."""
#     return ssdeep.hash(data)

# def compare_hashes(hash1, hash2):
#     """Compare two fuzzy hashes and return a similarity score."""
#     return ssdeep.compare(hash1, hash2)

# if __name__ == "__main__":
#     # Example strings to hash
#     data1 = "This is a test string."
#     data2 = "This is a test string with some extra content."

#     # Generate fuzzy hashes
#     hash1 = fuzzy_hash(data1)
#     hash2 = fuzzy_hash(data2)

#     print(f"Fuzzy Hash 1: {hash1}")
#     print(f"Fuzzy Hash 2: {hash2}")

#     # Compare the hashes
#     similarity = compare_hashes(hash1, hash2)
#     print(f"Similarity Score: {similarity}")

