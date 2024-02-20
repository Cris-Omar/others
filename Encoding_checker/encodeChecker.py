import chardet

text = b'Ylthpu+chsslf+dov+tyz+bulhzf+yltvcl+dvvklk+opt+fvb'  # Provide the binary data

result = chardet.detect(text)
encoding = result['encoding']
confidence = result['confidence']

print(f"Detected encoding: {encoding} with confidence: {confidence}")
