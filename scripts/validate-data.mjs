import { readFile } from 'node:fs/promises';
const load=async p=>JSON.parse(await readFile(p,'utf8')); const papers=await load('data/papers.json'), datasets=await load('data/datasets.json'), versions=await load('data/versions.json');
const unique=(items,key)=>new Set(items.map(x=>x[key])).size===items.length;
if(!unique(papers,'slug')) throw new Error('Paper slugs must be unique'); if(!unique(datasets,'slug')) throw new Error('Dataset slugs must be unique');
for(const p of papers) for(const key of ['slug','method','title','paradigm','summary','status']) if(!p[key]) throw new Error(`${p.slug||'paper'} missing ${key}`);
if(versions[0].status!=='Current') throw new Error('Newest version must be Current'); console.log(`Validated ${papers.length} papers, ${datasets.length} datasets, and ${versions.length} versions.`);
