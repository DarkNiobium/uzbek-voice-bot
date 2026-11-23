from typing import List

def split_text(text: str, max_chunk_size: int = 4000) -> List[str]:
    """
    Matnni Telegram xabarlari chegarasi (4096 belgi) dan oshmagan
    bo'laklarga ajratadi.
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    current_chunk = ""

    lines = text.split("\n")
    for line in lines:
        if len(current_chunk) + len(line) + 1 <= max_chunk_size:
            current_chunk += (line + "\n")
        else:
            if current_chunk:
                chunks.append(current_chunk.rstrip("\n"))
                current_chunk = ""

            if len(line) <= max_chunk_size:
                current_chunk = line + "\n"
            else:
                # Qator max_chunk_size dan katta bo'lsa, so'zlar bo'yicha ajratamiz
                words = line.split(" ")
                for word in words:
                    if len(word) > max_chunk_size:
                        # Juda uzun so'z (masalan link yoki probelsiz matn) bo'lsa
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                        for i in range(0, len(word), max_chunk_size):
                            slice_part = word[i:i + max_chunk_size]
                            if len(slice_part) == max_chunk_size:
                                chunks.append(slice_part)
                            else:
                                current_chunk = slice_part + " "
                    elif len(current_chunk) + len(word) + 1 <= max_chunk_size:
                        current_chunk += (word + " ")
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip())
                        current_chunk = word + " "

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
