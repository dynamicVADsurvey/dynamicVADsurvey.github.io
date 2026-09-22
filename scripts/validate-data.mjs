import { readFile, stat } from 'node:fs/promises';
const load=async p=>JSON.parse(await readFile(p,'utf8')); const papers=await load('data/papers.json'), datasets=await load('data/datasets.json'), versions=await load('data/versions.json'), stats=await load('data/statistics.json');
const unique=(items,key)=>new Set(items.map(x=>x[key])).size===items.length;
if(!unique(papers,'slug')) throw new Error('Paper slugs must be unique'); if(!unique(datasets,'slug')) throw new Error('Dataset slugs must be unique');
for(const p of papers) for(const key of ['slug','method','title','paradigm','summary','status']) if(!p[key]) throw new Error(`${p.slug||'paper'} missing ${key}`);
const current=versions.filter(v=>v.status==='Current');
if(current.length!==1||versions[0]!==current[0]) throw new Error('Exactly one version must be Current and it must be first');
if(stats.version!==current[0].version) throw new Error('data/statistics.json must match the Current entry in data/versions.json');
for(const version of versions.filter(v=>v.status==='Planned')) if(await stat(`versions/${version.version}/release.json`).catch(()=>null)) throw new Error(`Planned ${version.version} must not have a frozen release directory`);
for(const version of versions.filter(v=>v.status!=='Planned')){
  const release=await load(`versions/${version.version}/release.json`),frozenStats=await load(`versions/${version.version}/data/statistics.json`);
  if(release.version!==version.version||frozenStats.version!==version.version) throw new Error(`Frozen metadata for ${version.version} is inconsistent`);
  if(release.status!=='Released') throw new Error(`${version.version} release.json status must be the immutable value Released`);
}
console.log(`Validated ${papers.length} papers, ${datasets.length} datasets, and ${versions.length} versions.`);
