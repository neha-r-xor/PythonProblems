
import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB
INPUT_FILE = "10mb-examplefile-com.txt"
CHUNK_DIR = "chunks"
MERGED_FILE = "merged-10mb-examplefile-com.txt"


def split_file(input_path, chunk_dir, chunk_size):
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        os.makedirs(chunk_dir, exist_ok=True)
        index = 0
        with open(input_path, "rb") as src:
            while True:
                data = src.read(chunk_size)
                if not data:
                    break
                chunk_path = os.path.join(chunk_dir, f"part_{index:05d}.bin")
                with open(chunk_path, "wb") as out:
                    out.write(data)
                index += 1
        return index
    except Exception as e:
        print(f"Error during file split: {e}")
        return 0


def list_chunks(chunk_dir):
    try:
        if not os.path.exists(chunk_dir):
            raise FileNotFoundError(f"Chunk directory not found: {chunk_dir}")
        files = sorted(os.listdir(chunk_dir))
        if not files:
            raise ValueError("No chunks found in directory.")
        return files
    except Exception as e:
        print(f"Error listing chunks: {e}")
        return []


def read_chunk(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading chunk {path}: {e}")
        return b""


def merge_chunks(chunk_dir, output_path, max_workers=8):
    try:
        chunk_files = list_chunks(chunk_dir)
        if not chunk_files:
            raise ValueError("Cannot merge: No chunks available.")

        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {}
            for i, name in enumerate(chunk_files):
                full_path = os.path.join(chunk_dir, name)
                futures[pool.submit(read_chunk, full_path)] = i

            for fut in as_completed(futures):
                idx = futures[fut]
                data = fut.result()
                if data:
                    results[idx] = data
                else:
                    raise IOError(f"Chunk {idx} could not be read.")

        with open(output_path, "wb") as out:
            for i in range(len(chunk_files)):
                if i not in results:
                    raise IOError(f"Missing chunk {i} during merge.")
                out.write(results[i])
    except Exception as e:
        print(f"Error during merge: {e}")


def compute_hash(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                h.update(block)
        return h.hexdigest()
    except Exception as e:
        print(f"Error computing hash for {path}: {e}")
        return None


def verify_integrity(original, merged):
    orig_hash = compute_hash(original)
    merged_hash = compute_hash(merged)
    if orig_hash and merged_hash:
        return orig_hash == merged_hash
    return False


def main():
    try:
        print("Splitting file...")
        num_chunks = split_file(INPUT_FILE, CHUNK_DIR, CHUNK_SIZE)
        if num_chunks == 0:
            print("Split failed. Exiting.")
            return
        print(f"Split into {num_chunks} chunks.")

        print("Merging chunks using producer threads...")
        merge_chunks(CHUNK_DIR, MERGED_FILE)

        print("Verifying integrity...")
        if verify_integrity(INPUT_FILE, MERGED_FILE):
            print("Verification successful: Files are identical.")
        else:
            print("Verification failed: Files differ.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()