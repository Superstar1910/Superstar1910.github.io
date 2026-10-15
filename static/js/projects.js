/* Public project catalogue. Only explicitly listed public links are displayed. */
(async function(){
const el=document.getElementById('project-directory');
const filter=document.getElementById('project-filter');
if(!el)return;
try{
 const response=await fetch('/static/data/public-projects.json');
 if(!response.ok)throw Error('Catalogue unavailable');
 const data=await response.json();
 const draw=()=>{
  el.replaceChildren();
  const items=data.projects.filter(p=>filter.value==='all'||p.category===filter.value);
  for(const p of items){
   const article=document.createElement('article');article.className='project-item';
   const category=document.createElement('span');category.className='project-category';category.textContent=p.category;
   const heading=document.createElement('h3');heading.textContent=(p.title||p.name).replaceAll('_',' ').replaceAll('-',' ');
   const note=document.createElement('p');note.textContent=p.description||'Explore this public project.';
   const actions=document.createElement('div');actions.className='project-actions';
   if(p.viewUrl){const view=document.createElement('a');view.href=p.viewUrl;view.textContent=p.viewLabel||'Explore project ↗';view.rel='noopener noreferrer';if(new URL(view.href,location.href).origin!==location.origin){view.target='_blank';}actions.append(view);}
   const source=document.createElement('a');source.href=p.url;source.textContent=p.viewUrl?'Source & project details ↗':'Project overview & source ↗';source.rel='noopener noreferrer';source.target='_blank';actions.append(source);
   article.append(category,heading,note,actions);el.append(article);
  }
  if(!items.length)el.textContent='No public projects in this category.';
 };
 filter.addEventListener('change',draw);draw();
}catch(e){console.error('Project catalogue could not load:',e);el.insertAdjacentHTML('afterbegin','<p>Project catalogue temporarily unavailable. Browse the public repositories using the GitHub profile link above.</p>');}
})();