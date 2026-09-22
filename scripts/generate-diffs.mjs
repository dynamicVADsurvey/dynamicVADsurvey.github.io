import {readFile,writeFile,mkdir,readdir,rm} from 'node:fs/promises';
import path from 'node:path';

const candidates=(await readdir('versions',{withFileTypes:true})).filter(x=>x.isDirectory()).map(x=>x.name);
const folders=(await Promise.all(candidates.map(async name=>{
  try { await readFile(`versions/${name}/release.json`); return name; }
  catch (error) { if(error.code==='ENOENT') return null; throw error; }
}))).filter(Boolean).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
async function readTree(directory,prefix=''){
  const result={};
  for(const entry of await readdir(directory,{withFileTypes:true})){
    const relative=path.join(prefix,entry.name);
    if(entry.isDirectory()) Object.assign(result,await readTree(path.join(directory,entry.name),relative));
    else if(entry.name.endsWith('.md')) result[relative]=await readFile(path.join(directory,entry.name),'utf8');
  }
  return result;
}
async function loadRelease(version){
  const base=`versions/${version}`;
  const [release,papers,datasets,benchmarks,sections]=await Promise.all([
    readFile(`${base}/release.json`,'utf8').then(JSON.parse),
    readFile(`${base}/data/papers.json`,'utf8').then(JSON.parse),
    readFile(`${base}/data/datasets.json`,'utf8').then(JSON.parse),
    readFile(`${base}/data/benchmarks.json`,'utf8').then(JSON.parse),
    readTree(`${base}/content`)
  ]);
  return {...release,papers,datasets,benchmarks,sections};
}
const releases=Object.fromEntries(await Promise.all(folders.map(async v=>[v,await loadRelease(v)])));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const benchmarkKey=b=>b.key||[b.group,b.method,b.dataset,b.metric,b.protocol].join('|');
function compare(from,to){
 const changes=[];
 const records=(label,keyOf,oldItems,newItems)=>{const a=new Map(oldItems.map(x=>[keyOf(x),x])),b=new Map(newItems.map(x=>[keyOf(x),x]));for(const [id,n] of b)if(!a.has(id))changes.push({section:label,type:'added',new:`Added: ${n.method||n.name||id}`});else if(!same(a.get(id),n))changes.push({section:label,type:'modified',old:JSON.stringify(a.get(id)),new:JSON.stringify(n)});for(const [id,o] of a)if(!b.has(id))changes.push({section:label,type:'removed',old:`Removed: ${o.method||o.name||id}`})};
 records('Paper records',x=>x.slug,from.papers,to.papers);records('Datasets',x=>x.slug,from.datasets,to.datasets);records('Benchmarks',benchmarkKey,from.benchmarks,to.benchmarks);
 for(const name of new Set([...Object.keys(from.sections),...Object.keys(to.sections)])){const old=from.sections[name],now=to.sections[name];if(old!==now)changes.push({section:name,type:'modified',old,new:now})}
 const count=(section,type)=>changes.filter(c=>c.section===section&&(!type||c.type===type)).length;
 return {from:from.version,to:to.version,generated:true,summary:{papersAdded:count('Paper records','added'),papersRemoved:count('Paper records','removed'),papersUpdated:count('Paper records','modified'),datasetsAdded:count('Datasets','added'),benchmarksCorrected:count('Benchmarks','modified'),sectionsRevised:changes.filter(c=>!['Paper records','Datasets','Benchmarks'].includes(c.section)).length},changes};
}
await mkdir('data/diffs',{recursive:true});
for(const file of (await readdir('data/diffs')).filter(x=>x.endsWith('.json')))await rm(`data/diffs/${file}`);
let total=0;
for(let i=0;i<folders.length;i++)for(let j=i+1;j<folders.length;j++){const diff=compare(releases[folders[i]],releases[folders[j]]);await writeFile(`data/diffs/${folders[i]}--${folders[j]}.json`,JSON.stringify(diff,null,2)+'\n');total++}
console.log(`Generated ${total} static version comparisons from ${folders.length} frozen releases.`);
