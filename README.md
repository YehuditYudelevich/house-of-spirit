House of Spirit is a heap exploitation technique used in binary exploitation. 
It targets the memory management of dynamic memory allocators like malloc.
The attacker manipulates a dangling pointer to point to a fake chunk of memory controlled by them.
When the program attempts to free or reallocate this fake chunk, the attacker gains control over the program’s execution flow. 
This technique is commonly used to achieve arbitrary code execution or privilege escalation in vulnerable software.

![image](https://github.com/user-attachments/assets/9fade459-28b4-4169-ab34-a0726a371e53)
