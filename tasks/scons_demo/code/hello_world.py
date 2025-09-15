"""
Shih-Hsuan Hsu
July 30, 2024
Write a simple "Hello, World!" to a file '../output/hello_world.txt'.
"""

with open("../output/hello_world.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
