#!/usr/bin/env python
# coding: utf-8

# In[19]:


import re
from pathlib import Path
import pandas as pd


file_name = '/Users/joannakochel/repositories/personal/pretix/src/pretix/locale/pl/LC_MESSAGES/djangojs.po'


# In[20]:


input_text = Path(file_name).read_text()
input_text[:100]


# In[21]:


translations = re.findall('msgid (?:\".*?\"\s*(?:\n|$))+\s*msgstr (?:\".*?\"\s*(?:\n|$))+', input_text, flags=re.MULTILINE)
to_translate_list = []
for t in translations:
    regexp_match = re.search(r'msgid ((?:\".*?\"\s*(?:\n|$))+\s*)msgstr ((?:\".*?\"\s*(?:\n|$))+)', t)
    english = regexp_match.group(1).strip().splitlines()
    polish = regexp_match.group(2).strip().splitlines()
    if not [i for i in polish if i != '""']:
        for i in english:
            i = i.strip('"')
            if i != '':
                to_translate_list.append(f'{i}')

print(len(to_translate_list))
Path('translation_input.txt').write_text("\n".join(to_translate_list))


# In[22]:


corrected = pd.read_clipboard().dropna()
corrected


# In[23]:


corrected = corrected[corrected['done?'] & ~corrected['Backend']]
corrected


# In[24]:


translations_dict = {}
for row in corrected.to_dict('records'):
    translations_dict[row['input']] = row['corrected translation']
    if "Don't forget to set the correct fees above!" in row['input']:
        print(row)


# In[25]:


# for row in corrected.to_dict('records'):
#     print(re.findall(f"{row["input"], input_text))

input_text = Path(file_name).read_text()
input_text[:100]

translated = []
translations = re.findall('msgid (?:\".*?\"\s*(?:\n|$))+\s*msgstr (?:\".*?\"\s*(?:\n|$))+', input_text, flags=re.MULTILINE)
for t in translations:
    regexp_match = re.search(r'msgid ((?:\".*?\"\s*(?:\n|$))+\s*)msgstr ((?:\".*?\"\s*(?:\n|$))+)', t)
    english = regexp_match.group(1).strip().splitlines()
    polish = regexp_match.group(2).strip().splitlines()
    old_text = regexp_match.group(0)
    if not [i for i in polish if i != '""']:
        if len(english) == 1:
            try:
                new_text = old_text.replace('msgstr ""', f'''msgstr "{translations_dict[english[0].strip('"')]}"''')
                translated.append(english[0].strip('"'))
            except KeyError:
                continue
        else:
            new_text = 'msgstr ""'
            found = True
            for i in english:
                i = i.strip('"')
                if i != '':
                    try:
                        translation = translations_dict[i.strip()]
                        if i.endswith('.') and not translation.endswith('.'):
                            translation += '.'
                        if i.endswith(' ') and not translation.endswith(' '):
                            translation += ' '
                        translation = translation.replace('\ n', '\\n')
                        new_text += f'\n"{translation}"'
                        translated.append(i.strip())
                    except KeyError:
                        found = False
                        break
            if found:
                new_text = old_text.replace('msgstr ""', new_text)
            else:
                continue
        input_text = input_text.replace(regexp_match.group(0), new_text)
    
            
Path(file_name).write_text(input_text)


# In[26]:


len(translated)


# In[27]:


for eng, pol in translations_dict.items():
    if eng not in translated:
        print(eng)


# In[ ]:




