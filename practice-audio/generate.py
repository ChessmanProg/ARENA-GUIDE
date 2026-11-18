#!/usr/bin/env python3
"""Build original synthetic speech assets. No real evaluation data."""
import json, pathlib, subprocess
root=pathlib.Path(__file__).parent
cases=json.loads((root/'cases.json').read_text())
for i,c in enumerate(cases):
    lang='id' if i==2 else 'en-us'
    for role, texts in [('U',c['questions']),('A',c['A']),('B',c['B'])]:
        for n,txt in enumerate(texts):
            # Indonesian phonetic voice approximates Tagalog, not native speech.
            if i==2:
                txt=txt.replace('exam','eksam').replace('review','rebyu').replace('notes','nots').replace(' ng ',' nang ').replace(' mga ',' manga ')
            path=root/f'case{i}-{role}{n}.wav'
            subprocess.run(['espeak','-v',lang+('+f2' if role=='U' else '+m2' if role=='A' else '+m3'),'-s', '155' if role=='A' else '165','-p', '62' if role=='U' else '48' if role=='A' else '55','-w',str(path),txt],check=True)
            assert path.stat().st_size>1000
print('Built',len(list(root.glob('case*.wav'))),'audio files')
