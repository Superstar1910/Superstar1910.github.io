"use strict";
(function(){
 const form=document.getElementById("planner"),out=document.getElementById("results");
 if(!form||!out)return;
 function money(value,currency){return currency+" "+value.toLocaleString("en-US",{maximumFractionDigits:2});}
 form.addEventListener("submit",function(event){
  event.preventDefault();
  const value=id=>Number(document.getElementById(id).value);
  const expenses=value("expenses"),months=value("months"),saved=value("saved"),contribution=value("contribution"),currency=document.getElementById("currency").value;
  if(![expenses,months,saved,contribution].every(Number.isFinite)||[expenses,saved,contribution].some(x=>x<0)||!Number.isInteger(months)||months<1||months>24){
   out.replaceChildren();const p=document.createElement("p");p.textContent="Enter non-negative finite amounts and a whole-number coverage period of 1–24 months.";out.append(p);return;
  }
  const target=expenses*months,gap=Math.max(0,target-saved),duration=gap===0?0:contribution===0?null:Math.ceil(gap/contribution);
  if(!Number.isFinite(target)||!Number.isFinite(gap)||!Number.isSafeInteger(duration===null?0:duration)){out.textContent="Values are too large to calculate reliably.";return;}
  out.replaceChildren();const heading=document.createElement("h2");heading.textContent="Your plan";out.append(heading);
  for(const [label,result] of [["Target reserve",money(target,currency)],["Funding gap",money(gap,currency)],["Months to target",duration===null?"Not achievable at zero monthly contribution":String(duration)]]){
   const p=document.createElement("p"),strong=document.createElement("strong");p.append(document.createTextNode(label+": "));strong.textContent=result;p.append(strong);out.append(p);
  }
 });
 form.requestSubmit();
})();