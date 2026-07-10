import {readFile,writeFile,mkdir,readdir} from 'node:fs/promises';
const folders=(await readdir('versions',{withFileTypes:true})).filter(x=>x.isDirectory()).map(x=>x.name).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
const snapshots=Object.fromEntries(await Promise.all(folders.map(async v=>[v,JSON.parse(await readFile(`versions/${v}/snapshot.json`,'utf8'))])));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function compare(from,to){
 const changes=[]; const index=(xs,key)=>new Map(xs.map(x=>[x[key],x]));
 const records=(label,key,oldItems,newItems)=>{const a=index(oldItems,key),b=index(newItems,key);for(const [id,n] of b)if(!a.has(id))changes.push({section:label,type:'added',new:`Added: ${n.method||n.name||id}`});else if(!same(a.get(id),n))changes.push({section:label,type:'modified',old:JSON.stringify(a.get(id)),new:JSON.stringify(n)});for(const [id,o] of a)if(!b.has(id))changes.push({section:label,type:'removed',old:`Removed: ${o.method||o.name||id}`})};
 records('Paper records','slug',from.papers,to.papers); records('Datasets','slug',from.datasets,to.datasets); records('Benchmarks','key',from.benchmarks,to.benchmarks);
 for(const name of new Set([...Object.keys(from.sections),...Object.keys(to.sections)])){const old=from.sections[name],now=to.sections[name];if(old!==now)changes.push({section:name,type:name==='Taxonomy'?'reclassified':'modified',old,new:now})}
 const count=(section,type)=>changes.filter(c=>c.section===section&&(!type||c.type===type)).length;
 return {from:from.version,to:to.version,generated:true,sample:true,summary:{papersAdded:count('Paper records','added'),papersRemoved:count('Paper records','removed'),papersUpdated:count('Paper records','modified'),datasetsAdded:count('Datasets','added'),benchmarksCorrected:count('Benchmarks','modified'),sectionsRevised:changes.filter(c=>!['Paper records','Datasets','Benchmarks'].includes(c.section)).length},changes};
}
await mkdir('data/diffs',{recursive:true});let total=0;
for(let i=0;i<folders.length;i++)for(let j=i+1;j<folders.length;j++){const diff=compare(snapshots[folders[i]],snapshots[folders[j]]);await writeFile(`data/diffs/${folders[i]}--${folders[j]}.json`,JSON.stringify(diff,null,2)+'\n');total++}
console.log(`Generated ${total} static version comparisons from ${folders.length} snapshots.`);
